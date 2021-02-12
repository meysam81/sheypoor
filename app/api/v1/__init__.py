from fastapi import APIRouter

from . import ads, auth

router = APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(ads.router, prefix="/ads")
