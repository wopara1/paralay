# settings/routes.py
from fastapi import APIRouter
from .users.routes import user_router 

router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["Users"])
