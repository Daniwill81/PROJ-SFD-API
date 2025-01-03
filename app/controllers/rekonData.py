import pandas as pd
from app.models import RekonData, Sfd


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
                        df[col].iloc[i] for col in net_cols 
                        if pd.notna(df[col].iloc[i]) and isinstance(df[col].iloc[i], (int, float))
                    )

                    if pd.notna(code) and valeur_net > 0:
                        donnees_traitees.append({
                            "account_number": code,
                            "description": description or "",
                            "amount": int(valeur_net),
                        })

    # Insérer les données dans la collection
    saved_data = []
    for data in donnees_traitees:
        rekon_data = RekonData(
            sfd=sfd,
            account_number=data["account_number"],
            description=data["description"],
            amount=data["amount"]
        )
        await rekon_data.save()
        saved_data.append(rekon_data)

    return saved_data
