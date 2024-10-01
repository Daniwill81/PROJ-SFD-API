from app.models import Indicator, RekonData


def calculate_indicator_ratio(indicator: Indicator, rekon_data_list: list[RekonData]) -> float:
    """
    Calculate the indicator ratio based on the specific indicator and its associated RekonData.
    Returns the calculated ratio, an error message if account numbers are missing, or None if the calculation is not possible.
    """
    indicator_name = indicator.name.lower()

    def check_accounts_exist(accounts: set[str], rekon_data_list: list[RekonData]) -> list[str]:
        existing_accounts = set(data.account_number for data in rekon_data_list)
        missing_accounts = [account for account in accounts if account not in existing_accounts]
        return missing_accounts

    def calculate_resource(accounts: set[str], rekon_data_list: list[RekonData]) -> int:
        return sum(data.amount for data in rekon_data_list if data.account_number in accounts)

    if indicator_name == "limitation des risques":
        resource_A_accounts_number = {
            "A12",
            "A2A",
            "A3A",
            "A70",
            "B2D",
            "B2N",
            "B30",
            "B40",
            "B70",
            "C10",
            "D1E",
            "D1L",
            "N1A",
            "N1J",
            "N3A",
            "Q1A",
        }
        resource_B_accounts_number = {"F1A", "F2A", "F3A", "F50", "G2A", "G10", "G15", "G35", "G60", "G70", "L01"}

        missing_A = check_accounts_exist(resource_A_accounts_number, rekon_data_list)
        missing_B = check_accounts_exist(resource_B_accounts_number, rekon_data_list)
        if missing_A or missing_B:
            missing_accounts = ", ".join(missing_A + missing_B)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'limitation des risques': {missing_accounts}"
            )

        resource_A = calculate_resource(resource_A_accounts_number, rekon_data_list)
        resource_B = calculate_resource(resource_B_accounts_number, rekon_data_list)
        ratio = (resource_A / resource_B) * 100
        return ratio

    elif indicator_name == "couverture des emplois à mlt par des ressources stables":
        resource_A_accounts_number = {"L01", "F2A", "F3F", "F50", "G15", "G2A", "G30", "G35", "G60", "G70"}
        resource_B_accounts_number = {
            "A2H",
            "A2I",
            "A2J",
            "A3C",
            "A70",
            "B30",
            "B40",
            "B70",
            "D1E",
            "D1L",
            "D10",
            "D1S",
            "D23",
            "D30",
            "D40",
        }

        missing_A = check_accounts_exist(resource_A_accounts_number, rekon_data_list)
        missing_B = check_accounts_exist(resource_B_accounts_number, rekon_data_list)
        if missing_A or missing_B:
            missing_accounts = ", ".join(missing_A + missing_B)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'couverture des emplois à mlt par des ressources stables': {missing_accounts}"
            )

        resource_A = calculate_resource(resource_A_accounts_number, rekon_data_list)
        resource_B = calculate_resource(resource_B_accounts_number, rekon_data_list)
        ratio = (resource_A / resource_B) * 100
        return ratio

    elif indicator_name == "limitation des risques pris sur une seule signature":
        resource_A_accounts_number = {"A1X"}
        resource_B_accounts_number = {"F1A", "F2A", "F3A", "F50", "G2A", "G10", "G15", "G35", "G60", "G70", "L01"}
        resource_C_accounts_number = {"L62", "E05", "D24", "D31", "D41", "D46", "L70", "L80", "A2X", "A3X"}

        missing_A = check_accounts_exist(resource_A_accounts_number, rekon_data_list)
        missing_B = check_accounts_exist(resource_B_accounts_number, rekon_data_list)
        missing_C = check_accounts_exist(resource_C_accounts_number, rekon_data_list)
        if missing_A or missing_B or missing_C:
            missing_accounts = ", ".join(missing_A + missing_B + missing_C)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'limitation des risques pris sur une seule signature': {missing_accounts}"
            )

        resource_A = calculate_resource(resource_A_accounts_number, rekon_data_list)
        resource_B = calculate_resource(resource_B_accounts_number, rekon_data_list)
        resource_C = calculate_resource(resource_C_accounts_number, rekon_data_list)

        deducted = resource_B - resource_C
        ratio = (resource_A / deducted) * 100
        return ratio

    elif indicator_name == "norme de liquidité":
        resource_A_accounts_number = {
            "A10",
            "A12",
            "A2J",
            "A2A",
            "A3B",
            "B2D",
            "B2N",
            "B30",
            "B40",
            "C10",
            "C30",
            "C40",
            "C56",
            "A60",
            "B65",
            "C55",
            "N1A",
            "N1J",
            "N2A",
            "N2J",
        }
        resource_B_accounts_number = {
            "F1A",
            "F2A",
            "F3E",
            "F3F",
            "F50",
            "G10",
            "G15",
            "G2A",
            "G30",
            "G35",
            "G60",
            "G70",
            "H10",
            "H40",
            "F60",
            "G90",
            "N1H",
            "N1K",
            "N2H",
            "N2M",
        }

        missing_A = check_accounts_exist(resource_A_accounts_number, rekon_data_list)
        missing_B = check_accounts_exist(resource_B_accounts_number, rekon_data_list)
        if missing_A or missing_B:
            missing_accounts = ", ".join(missing_A + missing_B)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'norme de liquidité': {missing_accounts}"
            )

        resource_A = calculate_resource(resource_A_accounts_number, rekon_data_list)
        resource_B = calculate_resource(resource_B_accounts_number, rekon_data_list)
        ratio = (resource_A / resource_B) * 100
        return ratio

    elif indicator_name == "la réserve générale":
        resource_A_accounts_number = {"L80"}
        resource_B_accounts_number = {"L70"}

        missing_A = check_accounts_exist(resource_A_accounts_number, rekon_data_list)
        missing_B = check_accounts_exist(resource_B_accounts_number, rekon_data_list)
        if missing_A or missing_B:
            missing_accounts = ", ".join(missing_A + missing_B)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'la réserve générale': {missing_accounts}"
            )

        resource_A = calculate_resource(resource_A_accounts_number, rekon_data_list)
        resource_B = calculate_resource(resource_B_accounts_number, rekon_data_list)
        ratio = resource_A + resource_B
        return ratio

    elif indicator_name == "la norme de capitalisation":
        resource_A_accounts_number = {
            "L10",
            "L20",
            "L27",
            "L30",
            "L35",
            "L41",
            "L45",
            "L50",
            "L55",
            "L59",
            "L60",
            "L65",
            "L70",
            "L75",
            "L80",
        }
        resource_B_accounts_number = {"B"}
        resource_C_accounts_number = {"L62", "E05", "D24", "D31", "D41", "D46", "L70", "L80", "A2X", "A3X"}

        missing_A = check_accounts_exist(resource_A_accounts_number, rekon_data_list)
        missing_B = check_accounts_exist(resource_B_accounts_number, rekon_data_list)
        missing_C = check_accounts_exist(resource_C_accounts_number, rekon_data_list)
        if missing_A or missing_B or missing_C:
            missing_accounts = ", ".join(missing_A + missing_B + missing_C)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'la norme de capitalisation': {missing_accounts}"
            )

        resource_A = calculate_resource(resource_A_accounts_number, rekon_data_list)
        resource_B = calculate_resource(resource_B_accounts_number, rekon_data_list)
        resource_C = calculate_resource(resource_C_accounts_number, rekon_data_list)

        deducted = resource_A - resource_C
        ratio = (deducted / resource_B) * 100
        return ratio

    elif indicator_name == "la limitation des prises de participation":
        resource_A_accounts_number = {"D1E"}
        resource_B_accounts_number = {
            "L10",
            "L20",
            "L27",
            "L30",
            "L35",
            "L41",
            "L45",
            "L50",
            "L55",
            "L59",
            "L60",
            "L65",
            "L70",
            "L75",
            "L80",
        }
        resource_C_accounts_number = {"L62", "E05", "D24", "D31", "D41", "D46", "L70", "L80", "A2X", "A3X"}

        missing_A = check_accounts_exist(resource_A_accounts_number, rekon_data_list)
        missing_B = check_accounts_exist(resource_B_accounts_number, rekon_data_list)
        missing_C = check_accounts_exist(resource_C_accounts_number, rekon_data_list)
        if missing_A or missing_B or missing_C:
            missing_accounts = ", ".join(missing_A + missing_B + missing_C)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'la limitation des prises de participation': {missing_accounts}"
            )

        resource_A = calculate_resource(resource_A_accounts_number, rekon_data_list)
        resource_B = calculate_resource(resource_B_accounts_number, rekon_data_list)
        resource_C = calculate_resource(resource_C_accounts_number, rekon_data_list)

        deducted = resource_B - resource_C
        ratio = (resource_A / deducted) * 100
        return ratio

    elif indicator_name == "la limitation des prêts aux dirigeants, au personnel ainsi qu'aux personnes liées":
        resource_A_accounts_number = {"A"}
        resource_B_accounts_number = {
            "L10",
            "L20",
            "L27",
            "L30",
            "L35",
            "L41",
            "L45",
            "L50",
            "L55",
            "L59",
            "L60",
            "L65",
            "L70",
            "L75",
            "L80",
        }
        resource_C_accounts_number = {"L62", "E05", "D24", "D31", "D41", "D46", "L70", "L80", "A2X", "A3X"}

        missing_A = check_accounts_exist(resource_A_accounts_number, rekon_data_list)
        missing_B = check_accounts_exist(resource_B_accounts_number, rekon_data_list)
        missing_C = check_accounts_exist(resource_C_accounts_number, rekon_data_list)
        if missing_A or missing_B or missing_C:
            missing_accounts = ", ".join(missing_A + missing_B + missing_C)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'la limitation des prêts aux dirigeants, au personnel ainsi qu'aux personnes liées': {missing_accounts}"
            )

        resource_A = calculate_resource(resource_A_accounts_number, rekon_data_list)
        resource_B = calculate_resource(resource_B_accounts_number, rekon_data_list)
        resource_C = calculate_resource(resource_C_accounts_number, rekon_data_list)

        deducted = resource_B - resource_C
        ratio = (resource_A / deducted) * 100
        return ratio

    elif indicator_name == "La limitation des opérations autres que l'épargne et le crédit":
        resource_A_accounts_number = {"A"}
        resource_B_accounts_number = {
            "A12",
            "A30",
            "A70",
            "B2D",
            "B2N",
            "B30",
            "B40",
            "B70",
            "C10",
            "D1E",
            "D1L",
            "N1A",
            "N1J",
            "N3A",
            "Q1A",
        }

        missing_A = check_accounts_exist(resource_A_accounts_number, rekon_data_list)
        missing_B = check_accounts_exist(resource_B_accounts_number, rekon_data_list)
        if missing_A or missing_B:
            missing_accounts = ", ".join(missing_A + missing_B)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'La limitation des opérations autres que l'épargne et le crédit': {missing_accounts}"
            )

        resource_A = calculate_resource(resource_A_accounts_number, rekon_data_list)
        resource_B = calculate_resource(resource_B_accounts_number, rekon_data_list)
        ratio = (resource_A / resource_B) * 100
        return ratio

    elif indicator_name == "Le financement des immobilisations et des participants":
        resource_A_accounts_number = {"D24", "D25", "D31", "D36", "D41", "D45", "D46", "D47", "D1E"}
        resource_B_accounts_number = {
            "L10",
            "L20",
            "L27",
            "L30",
            "L35",
            "L41",
            "L45",
            "L50",
            "L55",
            "L59",
            "L60",
            "L65",
            "L70",
            "L75",
            "L80",
        }
        resource_C_accounts_number = {"L62", "E05", "D24", "D31", "D41", "D46", "L70", "L80", "A2X", "A3X"}

        missing_A = check_accounts_exist(resource_A_accounts_number, rekon_data_list)
        missing_B = check_accounts_exist(resource_B_accounts_number, rekon_data_list)
        missing_C = check_accounts_exist(resource_C_accounts_number, rekon_data_list)
        if missing_A or missing_B or missing_C:
            missing_accounts = ", ".join(missing_A + missing_B + missing_C)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'Le financement des immobilisations et des participants': {missing_accounts}"
            )

        resource_A = calculate_resource(resource_A_accounts_number, rekon_data_list)
        resource_B = calculate_resource(resource_B_accounts_number, rekon_data_list)
        resource_C = calculate_resource(resource_C_accounts_number, rekon_data_list)

        deducted = resource_B - resource_C
        ratio = (resource_A / deducted) * 100
        return ratio

    # Si aucun indicateur ne correspond
    return None
