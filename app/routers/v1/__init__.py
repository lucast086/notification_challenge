from fastapi import APIRouter

from app.routers.v1.auth import router as auth_router
from app.routers.v1.notifications import router as noti_router
from app.routers.v1.users import router as users_router

router = APIRouter(prefix='/v1')

router.include_router(auth_router)
router.include_router(noti_router)
router.include_router(users_router)
