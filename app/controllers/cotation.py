from app.models import Cotation, Criteria, Indicator, Sfd


async def cotation_calcul(sfd: Sfd, criteria: Criteria, year: int = 2024) -> Cotation:
    """Create a cotation and calculate the total mark for the given SFD, criteria, and year."""
    # Calculer la somme des marks des indicateurs
    total_mark = await Indicator.find(
        Indicator.sfd.id == sfd.id, Indicator.criteria.id == criteria.id, Indicator.year == year
    ).sum(Indicator.mark)

    # Créer une nouvelle cotation avec le total_mark calculé
    cotation = await Cotation(sfd=sfd, criteria=criteria, mark=total_mark, year=year).create()

    return cotation
