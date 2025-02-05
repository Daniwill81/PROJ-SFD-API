"""
CriteriaSerializer.

Handle Retrieve, Create and Update User object.
"""
from .cotation import CotationSerializer
from .criteria import CriteriaSerializer, WriteCriteriaSerializer
from .global_note import GlobalNoteSerializer

__all__ = [
    "CotationSerializer",
    "WriteCriteriaSerializer",
    "CriteriaSerializer",
    "GlobalNoteSerializer",
]
