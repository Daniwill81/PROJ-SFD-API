from app.models import Cotation, GlobalNote, Sfd


async def global_note_calcul(sfd: Sfd, year: int) -> GlobalNote:
    """
    Calculate the global note for a given SFD and year.

    Args:
        sfd (Sfd): The SFD for which to calculate the global note.
        year (int): The year for which to calculate the global note.

    Returns:
        GlobalNote: The created global note with the calculated mark and risk level.
    """
    # Calculate the total mark from related cotations
    total_mark = await Cotation.find(Cotation.sfd.id == sfd.id, Cotation.year == year).sum(Cotation.mark)

    # Determine the risk level based on the total mark
    if total_mark >= 90:
        risk_level = "Faible"
    elif 70 <= total_mark < 90:
        risk_level = "Moyen"
    elif 40 <= total_mark < 70:
        risk_level = "Elevé"
    else:
        risk_level = "Critique"

    # Create a new GlobalNote instance
    global_note = await GlobalNote(sfd=sfd, mark=total_mark, risk_level=risk_level, year=year).create()

    return global_note
