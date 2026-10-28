from collections.abc import Sequence
from datetime import datetime
from typing import TypedDict

from django.contrib.auth.models import AnonymousUser

from sentry.api.serializers import Serializer, register, serialize
from sentry.api.serializers.models.groupsearchview import (
    GroupSearchViewSerializer,
    GroupSearchViewSerializerResponse,
)
from sentry.models.groupsearchviewstarred import GroupSearchViewStarred
from sentry.models.savedsearch import SORT_LITERALS
from sentry.users.models.user import User
from sentry.users.services.user.model import RpcUser


class GroupSearchViewStarredSerializerResponse(TypedDict):
    id: str
    name: str
    query: str
    querySort: SORT_LITERALS
    projects: list[int]
    environments: list[str]
    timeFilters: dict
    lastVisited: datetime | None
    dateCreated: datetime | None
    dateUpdated: datetime


@register(GroupSearchViewStarred)
class GroupSearchViewStarredSerializer(Serializer[GroupSearchViewStarredSerializerResponse]):
    def __init__(self, *args, **kwargs) -> None:
        self.organization = kwargs.pop("organization", None)
        super().__init__(*args, **kwargs)

    def get_attrs(
        self,
        item_list: Sequence[GroupSearchViewStarred],
        user: User | RpcUser | AnonymousUser,
        **kwargs: object,
    ) -> dict[GroupSearchViewStarred, GroupSearchViewSerializerResponse]:
        views = [item.group_search_view for item in item_list]
        serialized_views = serialize(
            views,
            user,
            serializer=GroupSearchViewSerializer(organization=self.organization),
        )
        return dict(zip(item_list, serialized_views))

    def serialize(
        self,
        obj: GroupSearchViewStarred,
        attrs,
        user: User | RpcUser | AnonymousUser,
        **kwargs: object,
    ) -> GroupSearchViewStarredSerializerResponse:
        return {
            "id": attrs["id"],
            "name": attrs["name"],
            "query": attrs["query"],
            "querySort": attrs["querySort"],
            "projects": attrs["projects"],
            "environments": attrs["environments"],
            "timeFilters": attrs["timeFilters"],
            "lastVisited": attrs["lastVisited"],
            "dateCreated": attrs["dateCreated"],
            "dateUpdated": attrs["dateUpdated"],
        }
