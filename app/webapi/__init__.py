"""
AppMain.

This package contains configuration for the project.
The `router` list routes URLS to any accessible endpoint for a app.
The router in routes.py is referred as the main router for this app.
"""


from fastapi import APIRouter

from .auth import router as router_auth
from .criteria import router as router_criteria
from .indicators import router as router_indicators
from .rekonData import router as router_rekonData
from .sfd import router as router_sfd
from .user import router as router_user

router_api = APIRouter(redirect_slashes=True)

router_api.include_router(router_auth, prefix="/auth", tags=["auth"])
router_api.include_router(router_user, prefix="/user", tags=["user"])
router_api.include_router(router_criteria, prefix="/criteria", tags=["criteria"])
router_api.include_router(router_indicators, prefix="/indicators", tags=["indicators"])
router_api.include_router(router_rekonData, prefix="/rekonData", tags=["rekonData"])
router_api.include_router(router_sfd, prefix="/sfd", tags=["sfd"])
