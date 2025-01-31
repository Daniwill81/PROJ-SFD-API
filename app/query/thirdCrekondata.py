from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.models import ThirdCrekonData

from .base import Query


class ThirdRekonQuery(Query[ThirdCrekonData]):
    """Fetch some key statistics to display in the interface."""

    def get_qs(self) -> FindMany[ThirdCrekonData]:
        """Instantiate a new query object to avoid cache pollution."""
        qs: FindMany[ThirdCrekonData] = ThirdCrekonData.find()

        # Filtrer par année (year)
        if filter_year := self.filters.get("year"):
            qs = qs.find(ThirdCrekonData.year == int(filter_year))

        # Filtrer par ID du SFD (sfd_id)
        if filter_sfd_id := self.filters.get("sfd_id"):
            qs = qs.find(ThirdCrekonData.sfd.id == PydanticObjectId(filter_sfd_id))

        return qs
