from beanie.odm.queries.find import FindMany

from app.models import GlobalNote

from .base import Query


class GlobalNoteQuery(Query[GlobalNote]):
    """Fetch some key statistics to display in the interface."""

    def get_qs(self) -> FindMany[GlobalNote]:
        """Instantiate a new query object to avoid cache pollution."""
        qs: FindMany[GlobalNote] = GlobalNote.find()

        # Filter by sfd risk level
        if filter_risk_level := self.filters.get("risk_level"):
            if filter_risk_level == "Faible":
                qs = qs.find(GlobalNote.risk_level == "Faible")
            elif filter_risk_level == "Moyen":
                qs = qs.find(GlobalNote.risk_level == "Moyen")
            elif filter_risk_level == "Elevé":
                qs = qs.find(GlobalNote.risk_level == "Elevé")
            elif filter_risk_level == "Critique":
                qs = qs.find(GlobalNote.risk_level == "Critique")

        return qs
