from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, status

from app.controllers.v1.ads import controller as ad_controller
from app.core.auth import get_current_user
from app.schema.v1.ads import AdIn, AdOut, AdUpdate
from app.schema.v1.pagination import PaginatedAd

router = APIRouter()


@router.post("", response_model=AdOut)
async def create_new_ad(
    ad: AdIn = Body(...),
    user=Depends(get_current_user),
):
    return await ad_controller.create_new_ad(ad, user=user)


@router.get("", response_model=PaginatedAd)
async def get_all_ads(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=0, le=100),
    user=Depends(get_current_user),
):
    result, total = await ad_controller.get_all_ads(offset=offset, limit=limit)
    return PaginatedAd(
        offset=offset,
        limit=min(limit, len(result)),
        total=total,
        data=result,
    )


@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_ad(
    ad_id: UUID,
    user=Depends(get_current_user),
):
    await ad_controller.delete_an_ad(ad_id, user=user)


@router.get("/{ad_id}", response_model=AdOut)
async def get_an_ad(
    ad_id: UUID,
    user=Depends(get_current_user),
):
    return await ad_controller.get_an_ad(ad_id)


@router.patch("/{ad_id}", response_model=AdOut)
async def update_an_ad(
    ad_id: UUID,
    ad: AdUpdate,
    user=Depends(get_current_user),
):
    return await ad_controller.update_an_ad(ad_id, ad, user=user)
