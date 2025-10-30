from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour n'autoriser que les propriétaires à éditer un objet.
    Les admins peuvent tout voir et modifier.
    """

    def has_object_permission(self, request, view, obj):
        # Les requêtes de lecture sont autorisées pour tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True

        # Les admins peuvent tout modifier
        if request.user and request.user.is_staff:
            return True

        # Les propriétaires peuvent modifier leurs propres objets
        # Note: Quote n'a pas de champ 'user', donc on ne peut pas vérifier
        # Pour l'instant, seuls les admins peuvent modifier
        return False


class IsAdminOrCreateOnly(permissions.BasePermission):
    """
    Permission qui permet aux anonymes de créer un devis,
    mais seuls les admins peuvent lire/modifier les devis existants.
    """

    def has_permission(self, request, view):
        # Autoriser la création pour tout le monde
        if request.method == 'POST':
            return True

        # Pour les autres actions, seuls les admins
        return bool(request.user and request.user.is_staff)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission qui autorise tout le monde à lire, mais uniquement les admins à modifier.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
