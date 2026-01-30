
import logging
from fastapi import FastAPI
from fastapi.routing import APIRoute
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Role, Permission, RolePermission
from dependence.role_checker import PermissionRequired

logger = logging.getLogger(__name__)

def discover_permissions(app: FastAPI) -> set[str]:
    """
    Scans the FastAPI app routes to discover permissions defined in PermissionRequired dependencies.
    """
    permissions = set()
    logger.info(f"Scanning {len(app.routes)} routes for permissions...")
    
    for route in app.routes:
        if isinstance(route, APIRoute):
            # logger.info(f"Checking route: {route.path} {route.methods}")
            # Check route dependencies
            for dependency in route.dependencies:
                # dependency is usually an instance of fastapi.params.Depends
                # The 'dependency' attribute of Depends holds the callable/class instance
                dep_callable = dependency.dependency
                if isinstance(dep_callable, PermissionRequired):
                    permissions.add(dep_callable.permission_name)
                # handle if it's wrapped or checking type vs instance
                elif hasattr(dep_callable, "permission_name"): # Duck typing check
                     permissions.add(dep_callable.permission_name)

    return permissions

async def init_db(app: FastAPI, session: AsyncSession):
    """
    Initialize roles and permissions in the database using dynamic discovery.
    """
    try:
        logger.info("Initializing roles and permissions...")
        
        # 0. Discover Permissions
        discovered_permissions = discover_permissions(app)
        logger.info(f"Discovered {len(discovered_permissions)} permissions: {discovered_permissions}")

        # 1. Create/Update Permissions
        existing_perms_stmt = select(Permission)
        existing_perms_result = await session.execute(existing_perms_stmt)
        existing_perms = {p.name: p for p in existing_perms_result.scalars().all()}

        new_perms = []
        for perm_name in discovered_permissions:
            if perm_name not in existing_perms:
                new_perm = Permission(name=perm_name)
                session.add(new_perm)
                new_perms.append(new_perm)
        
        if new_perms:
            await session.commit()
            logger.info(f"Created {len(new_perms)} new permissions.")
            # Reload to get IDs
            existing_perms_stmt = select(Permission)
            existing_perms_result = await session.execute(existing_perms_stmt)
            existing_perms = {p.name: p for p in existing_perms_result.scalars().all()}
        else:
            logger.info("All discovered permissions already exist.")

        # 2. Create Roles
        ROLES = ["admin", "teacher", "student", "user"]
        existing_roles_stmt = select(Role)
        existing_roles_result = await session.execute(existing_roles_stmt)
        existing_roles = {r.name: r for r in existing_roles_result.scalars().all()}

        for role_name in ROLES:
            # Note: Role names in DB are typically lower case based on previous init_db
            # But the model makes them title() in init_db previously?
            # Let's standardize on lower case or adhere to existing
            role_key = role_name.title() # The previous code used .title() for name
            
            # Check if exists by name (case sensitive or not? DB unique constraint is on name)
            # We'll check both slug-like and title-like just in case, but existing_roles is keyed by name
            if role_key not in existing_roles:
                new_role = Role(name=role_key)
                session.add(new_role)
                await session.flush()
                existing_roles[role_key] = new_role
                logger.info(f"Created new role: {role_key}")
        
        await session.commit()

        # 3. Assign Permissions to Roles (Dynamic Logic)
        
        # Admin gets ALL permissions
        admin_perms = discovered_permissions

        # Teacher gets questions and quizzes
        teacher_perms = {
            p for p in discovered_permissions 
            if "question" in p or "quiz" in p or "statistics" in p
        }

        # Student gets specific quiz/result/process permissions
        student_perms = {
            p for p in discovered_permissions
            if (
                p == "read:quiz" 
                or p == "read:result"
                or p.startswith("quiz_process:")
            )
        }

        ROLE_PERMISSIONS_MAP = {
            "Admin": admin_perms,
            "Teacher": teacher_perms,
            "Student": student_perms,
            "User": set() 
        }

        for role_name, target_perm_names in ROLE_PERMISSIONS_MAP.items():
            role = existing_roles.get(role_name)
            if not role:
                logger.warning(f"Role {role_name} not found, skipping permission assignment.")
                continue

            current_role_perms_stmt = select(RolePermission).where(RolePermission.role_id == role.id)
            current_role_perms_result = await session.execute(current_role_perms_stmt)
            current_role_perm_ids = {rp.permission_id for rp in current_role_perms_result.scalars().all()}

            for perm_name in target_perm_names:
                perm = existing_perms.get(perm_name)
                if perm and perm.id not in current_role_perm_ids:
                    logger.info(f"Assigning permission '{perm_name}' to role '{role_name}'")
                    session.add(RolePermission(role_id=role.id, permission_id=perm.id))
            
        await session.commit()
        logger.info("Roles and permissions initialization complete.")

    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        await session.rollback()
        raise e
