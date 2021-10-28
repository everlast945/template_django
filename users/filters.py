from users.models import User
from utils.filterset import SearchFilterSet


class UserFilter(SearchFilterSet):
    search_fields = ('username', )

    class Meta:
        model = User
        fields = (
        )
