import typing 
from app.models import RekonData, Indicator

def calculate_indicator_ratio(indicator: Indicator, rekon_data_list: list[RekonData]) -> typing.Optional[int]:
    """
    Calculate the indicator ratio based on the specific indicator and its associated RekonData.
    Returns the calculated ratio or None if the calculation is not possible.
    """
    indicator_name = indicator.name.lower()

    if indicator_name == "limitation des risques":
        resource_A_accounts_number = {'A12', 'A2A', 'A3A', 'A70', 'B2D', 'B2N', 'B30', 'B40', 'B70', 'C10', 'D1E', 'D1L', 'N1A', 'N1J', 'N3A', 'Q1A'}
        resource_B_accounts_number = {'F1A', 'F2A', 'F3A', 'F50', 'G2A', 'G10', 'G15', 'G35', 'G60', 'G70', 'L01'}

        resource_A = sum(data.amount for data in rekon_data_list if data.account_number in resource_A_accounts_number)
        resource_B = sum(data.amount for data in rekon_data_list if data.account_number in resource_B_accounts_number)
        ratio = (resource_B / resource_A)*100 if resource_A != 0 else None
        return ratio

    elif indicator_name == "couverture des emplois à mlt par des ressources stables":
        resource_A_accounts_number = {'L01', 'F2A', 'F3F', 'F50', 'G15', 'G2A', 'G30', 'G35', 'G60', 'G70'}
        resource_B_accounts_number = {'A2H', 'A2I', 'A2J', 'A3C', 'A70', 'B30', 'B40', 'B70', 'D1E', 'D1L', 'D10', 'D1S', 'D23', 'D30', 'D40'}

        resource_A = sum(data.amount for data in rekon_data_list if data.account_number in resource_A_accounts_number)
        resource_B = sum(data.amount for data in rekon_data_list if data.account_number in resource_B_accounts_number)
        ratio = (resource_B / resource_A)*100 if resource_A != 0 else None
        return ratio

    #elif indicator_name == "limitation des risques pris sur une seule signature":
        #resource_A_accounts_number = {'A12', 'A2A', 'A3A', 'A70', 'B2D', 'B2N', 'B30', 'B40', 'B70', 'C10', 'D1E', 'D1L', 'N1A', 'N1J', 'N3A', 'Q1A'}
        #resource_B_accounts_number = {'F1A', 'F2A', 'F3A', 'F50', 'G2A', 'G10', 'G15', 'G35', 'G60', 'G70', 'L01'}

        #resource_A = sum(data.amount for data in rekon_data_list if data.account_number in resource_A_accounts_number)
        #resource_B = sum(data.amount for data in rekon_data_list if data.account_number in resource_B_accounts_number)
        #ratio = (resource_B / resource_A)*100 if resource_A != 0 else None
        #return ratio

    elif indicator_name == "norme de liquidité":
        resource_A_accounts_number = {'A10', 'A12', 'A2J', 'A2A', 'A3B', 'B2D', 'B2N', 'B30', 'B40', 'C10', 'C30', 'C40', 'C56', 'A60', 'B65', 'C55', 'N1A', 'N1J', 'N2A', 'N2J'}
        resource_B_accounts_number = {'F1A', 'F2A', 'F3E', 'F3F', 'F50', 'G10', 'G15', 'G2A', 'G30', 'G35', 'G60', 'G60', 'G70', 'H10', 'H40', 'F60', 'G90', 'N1H', 'N1K', 'N2H', 'N2M'}

        resource_A = sum(data.amount for data in rekon_data_list if data.account_number in resource_A_accounts_number)
        resource_B = sum(data.amount for data in rekon_data_list if data.account_number in resource_B_accounts_number)
        ratio = (resource_B / resource_A)*100 if resource_A != 0 else None
        return ratio

    elif indicator_name == "la réserve générale":
        resource_A_accounts_number = {'L80'}
        resource_B_accounts_number = {'L70'}

        resource_A = sum(data.amount for data in rekon_data_list if data.account_number in resource_A_accounts_number)
        resource_B = sum(data.amount for data in rekon_data_list if data.account_number in resource_B_accounts_number)
        ratio = resource_A + resource_B
        return ratio

    elif indicator_name == "la norme de capitalisation":
        resource_A_accounts_number = {'A12', 'A2A', 'A3A', 'A70', 'B2D', 'B2N', 'B30', 'B40', 'B70', 'C10', 'D1E', 'D1L', 'N1A', 'N1J', 'N3A', 'Q1A'}
        resource_B_accounts_number = {'F1A', 'F2A', 'F3A', 'F50', 'G2A', 'G10', 'G15', 'G35', 'G60', 'G70', 'L01'}

        resource_A = sum(data.amount for data in rekon_data_list if data.account_number in resource_A_accounts_number)
        resource_B = sum(data.amount for data in rekon_data_list if data.account_number in resource_B_accounts_number)
        ratio = (resource_B / resource_A)*100 if resource_A != 0 else None
        return ratio
    
    elif indicator_name == "la limitation des prises de participation":
        resource_A_accounts_number = {'A12', 'A2A', 'A3A', 'A70', 'B2D', 'B2N', 'B30', 'B40', 'B70', 'C10', 'D1E', 'D1L', 'N1A', 'N1J', 'N3A', 'Q1A'}
        resource_B_accounts_number = {'F1A', 'F2A', 'F3A', 'F50', 'G2A', 'G10', 'G15', 'G35', 'G60', 'G70', 'L01'}

        resource_A = sum(data.amount for data in rekon_data_list if data.account_number in resource_A_accounts_number)
        resource_B = sum(data.amount for data in rekon_data_list if data.account_number in resource_B_accounts_number)
        ratio = (resource_B / resource_A)*100 if resource_A != 0 else None
        return ratio
    
    elif indicator_name == "la limitation des prêts aux dirigeants, au personnel ainsi qu’aux personnes liées":
        resource_A_accounts_number = {'A12', 'A2A', 'A3A', 'A70', 'B2D', 'B2N', 'B30', 'B40', 'B70', 'C10', 'D1E', 'D1L', 'N1A', 'N1J', 'N3A', 'Q1A'}
        resource_B_accounts_number = {'F1A', 'F2A', 'F3A', 'F50', 'G2A', 'G10', 'G15', 'G35', 'G60', 'G70', 'L01'}

        resource_A = sum(data.amount for data in rekon_data_list if data.account_number in resource_A_accounts_number)
        resource_B = sum(data.amount for data in rekon_data_list if data.account_number in resource_B_accounts_number)
        ratio = (resource_B / resource_A)*100 if resource_A != 0 else None
        return ratio
    
    elif indicator_name == "La limitation des opérations autres que l’épargne et le crédit":
        resource_A_accounts_number = {'A12', 'A2A', 'A3A', 'A70', 'B2D', 'B2N', 'B30', 'B40', 'B70', 'C10', 'D1E', 'D1L', 'N1A', 'N1J', 'N3A', 'Q1A'}
        resource_B_accounts_number = {'F1A', 'F2A', 'F3A', 'F50', 'G2A', 'G10', 'G15', 'G35', 'G60', 'G70', 'L01'}

        resource_A = sum(data.amount for data in rekon_data_list if data.account_number in resource_A_accounts_number)
        resource_B = sum(data.amount for data in rekon_data_list if data.account_number in resource_B_accounts_number)
        ratio = (resource_B / resource_A)*100 if resource_A != 0 else None
        return ratio
    
    elif indicator_name == "Le financement des immobilisations et des participants":
        resource_A_accounts_number = {'A12', 'A2A', 'A3A', 'A70', 'B2D', 'B2N', 'B30', 'B40', 'B70', 'C10', 'D1E', 'D1L', 'N1A', 'N1J', 'N3A', 'Q1A'}
        resource_B_accounts_number = {'F1A', 'F2A', 'F3A', 'F50', 'G2A', 'G10', 'G15', 'G35', 'G60', 'G70', 'L01'}

        resource_A = sum(data.amount for data in rekon_data_list if data.account_number in resource_A_accounts_number)
        resource_B = sum(data.amount for data in rekon_data_list if data.account_number in resource_B_accounts_number)
        ratio = (resource_B / resource_A)*100 if resource_A != 0 else None
        return ratio
    # Ajoutez d'autres conditions pour les indicateurs restants...

    # Si aucun indicateur ne correspond
    return None
