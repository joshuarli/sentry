from collections.abc import Mapping
from typing import Any

from django.contrib.auth.models import AnonymousUser

from sentry.api.serializers import Serializer, register
from sentry.sentry_apps.models.servicehook import ServiceHookProject
from sentry.sentry_apps.services.cell.model import RpcServiceHookProject
from sentry.users.models.user import User
from sentry.users.services.user import RpcUser


@register(ServiceHookProject)
class ServiceHookProjectSerializer(Serializer):
    def serialize(
        self,
        obj: ServiceHookProject | RpcServiceHookProject,
        attrs: Mapping[Any, Any],  # justification: serializer attrs and kwargs are dynamic.
        user: User | RpcUser | AnonymousUser,
        **kwargs: Any,  # justification: serializer attrs and kwargs are dynamic.
    ) -> dict[str, str]:
        return {
            "id": str(obj.id),
            "project_id": str(obj.project_id),
        }
