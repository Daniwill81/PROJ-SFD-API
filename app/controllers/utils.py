import typing
from app.models import Indicator, RekonData


def calculate_indicator_ratio_and_mark(indicator: Indicator, rekon_data_list: list[RekonData]) -> typing.Union[float, int]:
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
        resource_a_accounts_number = {
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
            "N1A+N1J+N3A+Q1A",
        }
        resource_b_accounts_number = {"F1A", "F2A", "F3A", "F50", "G2A", "G10", "G15", "G35", "G60", "G70", "L01"}

        missing_a = check_accounts_exist(resource_a_accounts_number, rekon_data_list)
        missing_b = check_accounts_exist(resource_b_accounts_number, rekon_data_list)
        if missing_a or missing_b:
            missing_accounts = ", ".join(missing_a + missing_b)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'limitation des risques': {missing_accounts}"
            )

        resource_a = calculate_resource(resource_a_accounts_number, rekon_data_list)
        resource_b = calculate_resource(resource_b_accounts_number, rekon_data_list)
        ratio = (resource_a / resource_b) * 100

        if ratio <= 200:
            mark = 5
        elif 200 < ratio <= 210:
            mark = 4
        elif 210 < ratio <= 220:
            mark = 3
        elif 220 < ratio <= 230:
            mark = 2
        elif 230 < ratio <= 250:
            mark = 1
        else:  # ratio > 250
            mark = 0
        
        return ratio, mark

    if indicator_name == "couverture des emplois à mlt par des ressources stables":
        resource_a_accounts_number = {"L01", "F2A", "F3F", "F50", "G15", "G2A", "G30", "G35", "G60", "G70"}
        resource_b_accounts_number = {
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

        missing_a = check_accounts_exist(resource_a_accounts_number, rekon_data_list)
        missing_b = check_accounts_exist(resource_b_accounts_number, rekon_data_list)
        if missing_a or missing_b:
            missing_accounts = ", ".join(missing_a + missing_b)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'couverture des emplois à mlt par des ressources stables': {missing_accounts}"
            )

        resource_a = calculate_resource(resource_a_accounts_number, rekon_data_list)
        resource_b = calculate_resource(resource_b_accounts_number, rekon_data_list)
        ratio = (resource_a / resource_b) * 100

        if ratio >= 100:
            mark = 5
        elif 100 > ratio >= 90:
            mark = 4
        elif 90 > ratio >= 80:
            mark = 3
        elif 800 > ratio >= 70:
            mark = 2
        elif 70 > ratio >= 60:
            mark = 1
        else:  # ratio <60
            mark = 0
        
        return ratio, mark

    if indicator_name == "limitation des risques pris sur une seule signature":
        resource_a_accounts_number = {"A1X"}
        resource_b_accounts_number = {"F1A", "F2A", "F3A", "F50", "G2A", "G10", "G15", "G35", "G60", "G70", "L01"}
        resource_c_accounts_number = {"L62", "E05", "D24+D31+D41+D46", "L70", "L80", "A2X", "A3X"}

        missing_a = check_accounts_exist(resource_a_accounts_number, rekon_data_list)
        missing_b = check_accounts_exist(resource_b_accounts_number, rekon_data_list)
        missing_c = check_accounts_exist(resource_c_accounts_number, rekon_data_list)
        if missing_a or missing_b or missing_c:
            missing_accounts = ", ".join(missing_a + missing_b + missing_c)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'limitation des risques pris sur une seule signature': {missing_accounts}"
            )

        resource_a = calculate_resource(resource_a_accounts_number, rekon_data_list)
        resource_b = calculate_resource(resource_b_accounts_number, rekon_data_list)
        resource_c = calculate_resource(resource_c_accounts_number, rekon_data_list)

        deducted = resource_b - resource_c
        ratio = (resource_a / deducted) * 100

        if ratio <= 10:
            mark = 5
        elif 10 < ratio <= 12:
            mark = 4
        elif 12 < ratio <= 14:
            mark = 3
        elif 14 < ratio <= 16:
            mark = 2
        elif 16 < ratio <= 18:
            mark = 1
        else:  # ratio > 18
            mark = 0
        
        return ratio, mark

    if indicator_name == "norme de liquidité":
        resource_a_accounts_number = {
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
            "N1A+N1J+N2A+N2J",
        }
        resource_b_accounts_number = {
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
            "N1H+N1K+N2H+N2M",
        }

        missing_a = check_accounts_exist(resource_a_accounts_number, rekon_data_list)
        missing_b = check_accounts_exist(resource_b_accounts_number, rekon_data_list)
        if missing_a or missing_b:
            missing_accounts = ", ".join(missing_a + missing_b)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'norme de liquidité': {missing_accounts}"
            )

        resource_a = calculate_resource(resource_a_accounts_number, rekon_data_list)
        resource_b = calculate_resource(resource_b_accounts_number, rekon_data_list)
        ratio = (resource_a / resource_b) * 100
        
        if ratio >= 100:
            mark = 5
        elif 100 > ratio >= 90:
            mark = 4
        elif 90 > ratio >= 80:
            mark = 3
        elif 80 > ratio >= 70:
            mark = 2
        elif 70 > ratio >= 60:
            mark = 1
        else:  # ratio <60
            mark = 0
        
        return ratio, mark

    if indicator_name == "la réserve générale":
        resource_a_accounts_number = {"L80"}
        resource_b_accounts_number = {"L70"}

        missing_a = check_accounts_exist(resource_a_accounts_number, rekon_data_list)
        missing_b = check_accounts_exist(resource_b_accounts_number, rekon_data_list)
        if missing_a or missing_b:
            missing_accounts = ", ".join(missing_a + missing_b)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'la réserve générale': {missing_accounts}"
            )

        resource_a = calculate_resource(resource_a_accounts_number, rekon_data_list)
        resource_b = calculate_resource(resource_b_accounts_number, rekon_data_list)
        ratio = resource_a + resource_b
        
        if ratio > 15:
            mark = 3
        elif ratio == 15:
            mark = 2
        else:  # ratio < 15
            mark = 1

        return ratio, mark

    if indicator_name == "la norme de capitalisation":
        resource_a_accounts_number = {
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
        resource_b_accounts_number = {"B"}
        resource_c_accounts_number = {"L62", "E05", "D24+D31+D41+D46", "L70", "L80", "A2X", "A3X"}

        missing_a = check_accounts_exist(resource_a_accounts_number, rekon_data_list)
        missing_b = check_accounts_exist(resource_b_accounts_number, rekon_data_list)
        missing_c = check_accounts_exist(resource_c_accounts_number, rekon_data_list)
        if missing_a or missing_b or missing_c:
            missing_accounts = ", ".join(missing_a + missing_b + missing_c)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'la norme de capitalisation': {missing_accounts}"
            )

        resource_a = calculate_resource(resource_a_accounts_number, rekon_data_list)
        resource_b = calculate_resource(resource_b_accounts_number, rekon_data_list)
        resource_c = calculate_resource(resource_c_accounts_number, rekon_data_list)

        deducted = resource_a - resource_c
        ratio = (deducted / resource_b) * 100
        
        if ratio >= 15:
            mark = 5
        elif 15 > ratio >= 13:
            mark = 4
        elif 13 > ratio >= 11:
            mark = 3
        elif 11 > ratio >= 9:
            mark = 2
        elif 9 > ratio >= 7:
            mark = 1
        else:  # ratio <7
            mark = 0
        
        return ratio, mark

    if indicator_name == "la limitation des prises de participation":
        resource_a_accounts_number = {"D1E"}
        resource_b_accounts_number = {
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
        resource_c_accounts_number = {"L62", "E05", "D24+D31+D41+D46", "L70", "L80", "A2X", "A3X"}

        missing_a = check_accounts_exist(resource_a_accounts_number, rekon_data_list)
        missing_b = check_accounts_exist(resource_b_accounts_number, rekon_data_list)
        missing_c = check_accounts_exist(resource_c_accounts_number, rekon_data_list)
        if missing_a or missing_b or missing_c:
            missing_accounts = ", ".join(missing_a + missing_b + missing_c)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'la limitation des prises de participation': {missing_accounts}"
            )

        resource_a = calculate_resource(resource_a_accounts_number, rekon_data_list)
        resource_b = calculate_resource(resource_b_accounts_number, rekon_data_list)
        resource_c = calculate_resource(resource_c_accounts_number, rekon_data_list)

        deducted = resource_b - resource_c
        ratio = (resource_a / deducted) * 100
        
        if ratio <= 25:
            mark = 5
        elif 25 < ratio <= 27:
            mark = 4
        elif 27 < ratio <= 29:
            mark = 3
        elif 29 < ratio <= 31:
            mark = 2
        elif 31 < ratio <= 33:
            mark = 1
        else:  # ratio > 33
            mark = 0
        
        return ratio, mark

    if indicator_name == "la limitation des prêts aux dirigeants, au personn ainsi qu'aux personnes liées":
        resource_a_accounts_number = {"A"}
        resource_b_accounts_number = {
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
        resource_c_accounts_number = {"L62", "E05", "D24", "D24+D31+D41+D46", "L70", "L80", "A2X", "A3X"}

        missing_a = check_accounts_exist(resource_a_accounts_number, rekon_data_list)
        missing_b = check_accounts_exist(resource_b_accounts_number, rekon_data_list)
        missing_c = check_accounts_exist(resource_c_accounts_number, rekon_data_list)
        if missing_a or missing_b or missing_c:
            missing_accounts = ", ".join(missing_a + missing_b + missing_c)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'la limitation des prêts aux dirigeants, au personnel ainsi qu'aux personnes liées': {missing_accounts}"
            )

        resource_a = calculate_resource(resource_a_accounts_number, rekon_data_list)
        resource_b = calculate_resource(resource_b_accounts_number, rekon_data_list)
        resource_c = calculate_resource(resource_c_accounts_number, rekon_data_list)

        deducted = resource_b - resource_c
        ratio = (resource_a / deducted) * 100
        
        if ratio <= 10:
            mark = 5
        elif 10 < ratio <= 12:
            mark = 4
        elif 12 < ratio <= 14:
            mark = 3
        elif 14 < ratio <= 16:
            mark = 2
        elif 16 < ratio <= 18:
            mark = 1
        else:  # ratio > 18
            mark = 0
        
        return ratio, mark

    if indicator_name == "La limitation des opérations autres que l'épargne et le crédit":
        resource_a_accounts_number = {"A"}
        resource_b_accounts_number = {
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
            "N1A+N1J+N3A+Q1A",
        }

        missing_a = check_accounts_exist(resource_a_accounts_number, rekon_data_list)
        missing_b = check_accounts_exist(resource_b_accounts_number, rekon_data_list)
        if missing_a or missing_b:
            missing_accounts = ", ".join(missing_a + missing_b)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'La limitation des opérations autres que l'épargne et le crédit': {missing_accounts}"
            )

        resource_a = calculate_resource(resource_a_accounts_number, rekon_data_list)
        resource_b = calculate_resource(resource_b_accounts_number, rekon_data_list)
        ratio = (resource_a / resource_b) * 100
        
        if ratio <= 5:
            mark = 5
        elif 5 < ratio <= 6:
            mark = 4
        elif 6 < ratio <= 7:
            mark = 3
        elif 7 < ratio <= 8:
            mark = 2
        elif 8 < ratio <= 10:
            mark = 1
        else:  # ratio > 18
            mark = 0
        
        return ratio, mark

    if indicator_name == "Le financement des immobilisations et des participants":
        resource_a_accounts_number = {"D24", "D25", "D31", "D36", "D41", "D45", "D46", "D47", "D1E"}
        resource_b_accounts_number = {
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
        resource_c_accounts_number = {"L62", "E05", "D24", "D31", "D41", "D46", "L70", "L80", "A2X", "A3X"}

        missing_a = check_accounts_exist(resource_a_accounts_number, rekon_data_list)
        missing_b = check_accounts_exist(resource_b_accounts_number, rekon_data_list)
        missing_c = check_accounts_exist(resource_c_accounts_number, rekon_data_list)
        if missing_a or missing_b or missing_c:
            missing_accounts = ", ".join(missing_a + missing_b + missing_c)
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur 'Le financement des immobilisations et des participants': {missing_accounts}"
            )

        resource_a = calculate_resource(resource_a_accounts_number, rekon_data_list)
        resource_b = calculate_resource(resource_b_accounts_number, rekon_data_list)
        resource_c = calculate_resource(resource_c_accounts_number, rekon_data_list)

        deducted = resource_b - resource_c
        ratio = (resource_a / deducted) * 100

        if ratio <= 100:
            mark = 5
        elif 100 < ratio <= 105:
            mark = 4
        elif 105 < ratio <= 110:
            mark = 3
        elif 110 < ratio <= 115:
            mark = 2
        elif 115 < ratio <= 120:
            mark = 1
        else:  # ratio > 120
            mark = 0
        
        return ratio, mark
    # Si aucun indicateur ne correspond
    return None
