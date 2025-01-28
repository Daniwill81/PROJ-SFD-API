import pandas as pd

from app.models import RekonData, Sfd, ThirdCrekonData


async def upload_rekonData(upload_file, sfd: Sfd) -> list[RekonData]:
    xls = pd.ExcelFile(upload_file)
    donnees_traitees = []

    for feuille in xls.sheet_names:
        if feuille.endswith("_DEV"):
            df = pd.read_excel(xls, sheet_name=feuille)
            if df.empty:
                continue

            df.columns = df.columns.str.lower()
            code_col = None
            net_cols = []

            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, str) and "code" in x.lower()).any():
                    code_col = col
                elif df[col].apply(lambda x: isinstance(x, str) and "net" in x.lower()).any():
                    net_cols.append(col)

            if code_col is None:
                continue

            idx_code = df.columns.get_loc(code_col)
            description_col = df.columns[idx_code + 1] if idx_code + 1 < len(df.columns) else None

            for i, code in enumerate(df[code_col]):
                if isinstance(code, str) and "code" in code.lower():
                    continue

                if pd.notna(code):
                    description = df[description_col].iloc[i] if description_col is not None else ""
                    valeur_net = sum(
                        df[col].iloc[i]
                        for col in net_cols
                        if pd.notna(df[col].iloc[i]) and isinstance(df[col].iloc[i], (int, float))
                    )

                    if pd.notna(code) and valeur_net > 0:
                        donnees_traitees.append(
                            {
                                "account_number": code,
                                "description": description or "",
                                "amount": int(valeur_net),
                            }
                        )

    # Insérer les données dans la collection
    saved_data = []
    for data in donnees_traitees:
        rekon_data = RekonData(
            sfd=sfd, account_number=data["account_number"], description=data["description"], amount=data["amount"]
        )
        await rekon_data.save()
        saved_data.append(rekon_data)

    return saved_data


async def upload_third_crekondata_file(upload_file, sfd: Sfd) -> list[ThirdCrekonData]:
    # Charger le fichier Excel
    xls = pd.ExcelFile(upload_file)

    # Vérifier si la feuille "ANNEXES_AU_RAPPORT_ANNUEL" existe
    if "ANNEXES_AU_RAPPORT_ANNUEL" not in xls.sheet_names:
        raise ValueError("La feuille 'ANNEXES_AU_RAPPORT_ANNUEL' est introuvable.")

    # Charger la feuille
    df = pd.read_excel(xls, sheet_name="ANNEXES_AU_RAPPORT_ANNUEL", header=None)

    # Convertir en chaînes pour faciliter la recherche
    df = df.fillna("").astype(str)

    # Préparer les données
    donnees_traitees = []

    # --- Extraction des données "Y03301" ---
    ligne_code = df[df.apply(lambda row: row.astype(str).str.contains("Y03301").any(), axis=1)]
    if not ligne_code.empty:
        row_code = ligne_code.iloc[0]
        col_indices = row_code[row_code != ""].index.tolist()

        if len(col_indices) >= 4:
            col_deposants = col_indices[1]  # La colonne juste après "Y03301"
            col_annee_n = col_indices[2]  # La colonne Année (n)
            col_annee_n1 = col_indices[3]  # La colonne Année (n-1)

            # Récupérer les valeurs
            annee_n = pd.to_numeric(row_code[col_annee_n].replace(" ", ""), errors="coerce")
            annee_n1 = pd.to_numeric(row_code[col_annee_n1].replace(" ", ""), errors="coerce")

            if pd.notna(annee_n) and pd.notna(annee_n1):
                donnees_traitees.append(
                    {
                        "account_number": "Y03301",
                        "n_year": int(annee_n),
                        "n_1_year": int(annee_n1),
                        "net_asset": 0,
                        "total_loan_amount": 0,
                    }
                )

    # --- Extraction des données "Actif net" et "Montant total des emprunts" ---
    net_asset = 0
    total_loan_amount = 0

    ligne_actif_net = df[df.apply(lambda row: row.astype(str).str.contains("Actif net").any(), axis=1)]
    if not ligne_actif_net.empty:
        row_actif_net = ligne_actif_net.iloc[0]
        montant_col_index = row_actif_net[row_actif_net != ""].index[-1]
        net_asset = pd.to_numeric(row_actif_net[montant_col_index], errors="coerce")
        if pd.isna(net_asset):
            net_asset = 0

    ligne_emprunts = df[df.apply(lambda row: row.astype(str).str.contains("Montant total des emprunts").any(), axis=1)]
    if not ligne_emprunts.empty:
        row_emprunts = ligne_emprunts.iloc[0]
        montant_col_index = row_emprunts[row_emprunts != ""].index[-1]
        total_loan_amount = pd.to_numeric(row_emprunts[montant_col_index], errors="coerce")
        if pd.isna(total_loan_amount):
            total_loan_amount = 0

    # Mettre à jour les valeurs pour Y03301 si elles existent
    if donnees_traitees:
        donnees_traitees[0]["net_asset"] = int(net_asset)
        donnees_traitees[0]["total_loan_amount"] = int(total_loan_amount)

    # Insérer les données dans la collection
    saved_data = []
    for data in donnees_traitees:
        third_rekon_data = ThirdCrekonData(
            sfd=sfd,
            account_number=data["account_number"],
            n_year=data["n_year"],
            n_1_year=data["n_1_year"],
            net_asset=data["net_asset"],
            total_loan_amount=data["total_loan_amount"],
        )
        await third_rekon_data.save()
        saved_data.append(third_rekon_data)

    return saved_data
