from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class MultiDBAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        auth_user, superuser = User.objects.get_superuser_for_app(username=username)

        if superuser and auth_user.check_password(password):
            return superuser

        elif not superuser:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        _, superuser = User.objects.get_superuser_for_app(id=user_id)
        if superuser:
            return superuser

        else:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                return None
