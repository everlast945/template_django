from users.filters import UserFilter
from users.models import User
from users.serializers import UserListSerializer, UserAutocompleteSerializer
from utils.views import MultiSerializerViewSet


class UserViewSet(MultiSerializerViewSet):
    queryset = User.objects.filter(is_active=True).all()
    filtersets = {
        'list': UserFilter,
        'autocomplete': UserFilter,
    }
    serializers = {
        'list': UserListSerializer,
        'autocomplete': UserAutocompleteSerializer,
    }

    def list(self, request, *args, **kwargs):
        """
        Список пользователей
        """
        return super().list(request, *args, **kwargs)

    def autocomplete(self, request, *args, **kwargs):
        """
        Список пользователей (для автокомплита)
        """
        return super().list(request, *args, **kwargs)
