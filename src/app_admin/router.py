from fastapi import APIRouter

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@admin_router.get('get_admin_info')
async def get_info_admin():
    pass

