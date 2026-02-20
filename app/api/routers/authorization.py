from app.core.limiter import limiter
from fastapi import APIRouter, Depends, Request

from app.core.dependencies import require_roles
from app.db.models import User

router = APIRouter(prefix="/authz", tags=["authz"])


@router.get("/superadmins-only")
@limiter.limit("60/minute")
def superadmin_endpoint(request: Request, user: User = Depends(require_roles(["superadmin"]))):
    return {"message": f"Hello {user.email}, you are an superadmin!"}


@router.get("/admins-only")
@limiter.limit("60/minute")
def admin_endpoint(request: Request, user: User = Depends(require_roles(["superadmin", "admin"]))):
    return {"message": f"Hello {user.email}, you are a superadmin/admin!"}


@router.get("/users-only")
@limiter.limit("60/minute")
def user_endpoint(request: Request, user: User = Depends(require_roles(["superadmin", "admin", "user"]))):
    return {"message": f"Hello {user.email}, you are a superadmin/admin/user!"}
