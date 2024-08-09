from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany
from app.models import Indicator

from .base import Query


class IndicatorQuery(Query[Indicator]):
    """Fetch some key statistics to display in the interface."""

    def get_qs(self) -> FindMany[Indicator]:
        """Instantiate a new query object to avoid cache pollution."""
        qs: FindMany[Indicator] = Indicator.find()

        # Filter by criteria
        if filter_criteria_id := self.filters.get("criteria"):
            qs = qs.find(Indicator.criteria.id == PydanticObjectId(filter_criteria_id))

        return qs
