from app.models import Criteria, Indicator, RekonData, Sfd, ThirdCrekonData

from .utils import calculate_c3_indicator_ratio_and_mark, calculate_indicator_ratio_and_mark


async def create_indicators_for_sfd(sfd_id: str, year: int) -> list[Indicator]:
    """
    Create and calculate indicators for a specific SFD and year.
    Returns a list of created indicators.
    """
    # Get the SFD
    sfd = await Sfd.get_or_404(sfd_id)
    print(f"Found SFD: {sfd.id}")  # Debug log

    # Get all rekondata for this SFD and year
    rekon_data_list = await RekonData.find(
        {"sfd.$id": sfd.id, "year": year}  # Utilisez la syntaxe correcte pour les références
    ).to_list()

    print(f"Found {len(rekon_data_list)} RekonData records")  # Debug log

    ############################## Ajoutons un diagnostic des comptes disponibles############################

    available_accounts = set(data.account_number for data in rekon_data_list)
    print(f"Available account numbers: {sorted(available_accounts)}")

    # Si aucun RekonData n'est trouvé, faisons une requête de diagnostic
    if not rekon_data_list:
        # Vérifions d'abord s'il y a des RekonData pour ce SFD, quelle que soit l'année
        all_rekon = await RekonData.find({"sfd.$id": sfd.id}).to_list()

        if all_rekon:
            years = set(r.year for r in all_rekon)
            raise ValueError(
                f"Aucune rekonData trouvée pour l'année {year}. " f"Années disponibles pour ce SFD: {sorted(years)}"
            )
        else:
            raise ValueError(
                f"Aucune rekonData trouvée pour ce SFD ({sfd_id}). "
                "Veuillez vérifier que les données ont été correctement importées."
            )
    #######################################################################################################

    # Get the "Ratios prudentiels" criteria
    criteria_1 = await Criteria.find_one({"name": "Ratios prudentiels"})
    if not criteria_1:
        raise ValueError("Critère 'Ratios prudentiels' non trouvé dans la base de données")

    criteria_2 = await Criteria.find_one({"name": "Indicateurs périodiques"})
    if not criteria_2:
        raise ValueError("Critère 'Ratios prudentiels' non trouvé dans la base de données")

    print(f"Found criteria: {criteria_1.id}")  # Debug log
    print(f"Found criteria: {criteria_2.id}")  # Debug log

    # Define indicators to create
    indicators_to_create = [
        {"name": "Limitation des risques", "sfd": sfd, "criteria": criteria_1, "year": year},
        {
            "name": "La couverture des emplois à MLT par des ressources stables",
            "sfd": sfd,
            "criteria": criteria_1,
            "year": year,
        },
        {
            "name": "La limitation des risques pris sur une seule signature",
            "sfd": sfd,
            "criteria": criteria_1,
            "year": year,
        },
        {"name": "Norme de liquidité", "sfd": sfd, "criteria": criteria_1, "year": year},
        {"name": "La réserve générale", "sfd": sfd, "criteria": criteria_1, "year": year},
        {"name": "La norme de capitalisation", "sfd": sfd, "criteria": criteria_1, "year": year},
        {"name": "La limitation des prises de participation", "sfd": sfd, "criteria": criteria_1, "year": year},
        {
            "name": "La limitation des prêts aux dirigeants, au personnel ainsi qu'aux personnes liées",
            "sfd": sfd,
            "criteria": criteria_1,
            "year": year,
        },
        {
            "name": "La limitation des opérations autres que l’épargne et le crédit",
            "sfd": sfd,
            "criteria": criteria_1,
            "year": year,
        },
        {
            "name": "Le financement des immobilisations et des participants",
            "sfd": sfd,
            "criteria": criteria_1,
            "year": year,
        },
        {"name": "taux de provision pour créances en souffrance", "sfd": sfd, "criteria": criteria_2, "year": year},
        {"name": "taux de perte sur créances", "sfd": sfd, "criteria": criteria_2, "year": year},
        {"name": "portefeuille classe a risque", "sfd": sfd, "criteria": criteria_2, "year": year},
        {
            "name": "charge d’exploitation rapportées au portefeuille de crédits",
            "sfd": sfd,
            "criteria": criteria_2,
            "year": year,
        },
        {"name": "rentabilité des fonds propres", "sfd": sfd, "criteria": criteria_2, "year": year},
    ]

    created_indicators = []

    for indicator_data in indicators_to_create:
        try:
            indicator = Indicator(**indicator_data)
            ratio, mark = calculate_indicator_ratio_and_mark(indicator, rekon_data_list)
            indicator.ratio = ratio
            indicator.mark = mark
            await indicator.insert()
            created_indicators.append(indicator)
            print(f"Created indicator: {indicator.name} with ratio {ratio} and mark {mark}")  # Debug log

        except AssertionError as e:
            print(f"Error calculating indicator {indicator_data['name']}: {str(e)}")
            continue
        except Exception as e:
            print(f"Unexpected error for indicator {indicator_data['name']}: {str(e)}")
            continue

    return created_indicators


async def create_c3_indicators_for_sfd(sfd_id: str, year: int) -> list[Indicator]:
    # Get the SFD
    sfd = await Sfd.get_or_404(sfd_id)
    print(f"Found SFD: {sfd.id}")  # Debug log

    rekon_data = await ThirdCrekonData.find_one(
        {"sfd.$id": sfd.id, "year": year}  # Utilisez la syntaxe correcte pour les références
    )

    # Get the "Autre indicateurs" criteria
    criteria_3 = await Criteria.find_one({"name": "Autres indicateurs"})
    if not criteria_3:
        raise ValueError("Critère 'Autres indicateurs' non trouvé dans la base de données")

    print(f"Found criteria: {criteria_3.id}")  # Debug log

    # Define indicators to create
    indicators_to_create = [
        {"name": "variation du nombre de déposants", "sfd": sfd, "criteria": criteria_3, "year": year},
        {"name": "Rapport montant total des emprunts sur actif net", "sfd": sfd, "criteria": criteria_3, "year": year},
    ]

    created_indicators = []

    for indicator_data in indicators_to_create:
        try:
            indicator = Indicator(**indicator_data)
            ratio, mark = calculate_c3_indicator_ratio_and_mark(indicator, rekon_data)
            indicator.ratio = ratio
            indicator.mark = mark
            await indicator.insert()
            created_indicators.append(indicator)
            print(f"Created indicator: {indicator.name} with ratio {ratio} and mark {mark}")  # Debug log

        except AssertionError as e:
            print(f"Error calculating indicator {indicator_data['name']}: {str(e)}")
            continue
        except Exception as e:
            print(f"Unexpected error for indicator {indicator_data['name']}: {str(e)}")
            continue

    return created_indicators


async def create_c4_indicators_for_sfd(sfd_id: str, year: int, name: str, mark: int) -> list[Indicator]:
    # Get the SFD
    sfd = await Sfd.get_or_404(sfd_id)
    print(f"Found SFD: {sfd.id}")  # Debug log

    # Get the "Reporting reglementaire" criteria
    criteria_4 = await Criteria.find_one({"name": "Reporting reglementaire"})
    if not criteria_4:
        raise ValueError("Critère 'Reporting reglementaire' non trouvé dans la base de données")

    print(f"Found criteria: {criteria_4.id}")  # Debug log

    indicator = Indicator(
        sfd=sfd,
        criteria=criteria_4,
        name=name,
        ratio=0,
        estimation="Non necessaire pour cet indicateur",
        mark=mark,
        year=2024,
    )

    await indicator.save()

    print(f"Created indicator: {indicator.name} with mark {indicator.mark}")  # Debug log

    return indicator


async def create_c5_indicators_for_sfd(
    sfd_id: str, year: int, name: str, mark: int, estimation: str
) -> list[Indicator]:
    # Get the SFD
    sfd = await Sfd.get_or_404(sfd_id)
    print(f"Found SFD: {sfd.id}")  # Debug log

    # Get the "Autres critères non financier" criteria
    criteria_5 = await Criteria.find_one({"name": "Autres critères non financier"})
    if not criteria_5:
        raise ValueError("Critère 'Autres critères non financier' non trouvé dans la base de données")

    print(f"Found criteria: {criteria_5.id}")  # Debug log

    indicator = Indicator(sfd=sfd, criteria=criteria_5, name=name, ratio=0, estimation=estimation, mark=mark, year=2024)

    await indicator.save()

    print(
        f"Created indicator: {indicator.name} with estimation {indicator.estimation} and mark {indicator.mark}"
    )  # Debug log

    return indicator
