from ..models.user import User


class ProfileClientService:

    @staticmethod
    def get_profile(user_id: int) -> dict:
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise ValueError("Utilisateur introuvable.")

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_verified": user.is_verified,
            "is_active": user.is_active,
            "roles": [role.name for role in user.roles],
            "can_become_artisan": ProfileClientService.can_become_artisan(user),
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    @staticmethod
    def can_become_artisan(user: User) -> bool:
        role_names = {role.name.lower() for role in user.roles}
        return (
            user.is_active
            and user.is_verified
            and "artisan" not in role_names
            and "admin" not in role_names
        )