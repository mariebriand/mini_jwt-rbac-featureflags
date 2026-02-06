from fastapi import APIRouter, Depends

from app.db.models import User
from app.core.dependencies import require_roles

router = APIRouter(prefix="/authz", tags=["authz"])


@router.get("/superadmins-only")
def superadmin_endpoint(user: User = Depends(require_roles(["superadmin"]))):
    return {"message": f"Hello {user.email}, you are an superadmin!"}


@router.get("/admins-only")
def admin_endpoint(user: User = Depends(require_roles(["superadmin", "admin"]))):
    return {"message": f"Hello {user.email}, you are a superadmin/admin!"}


@router.get("/users-only")
def user_endpoint(user: User = Depends(require_roles(["superadmin", "admin", "user"]))):
    return {"message": f"Hello {user.email}, you are a superadmin/admin/user!"}
