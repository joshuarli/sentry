from rest_framework.serializers import ListField


class EmptyListField(ListField):
    def to_internal_value(self, data: list[object] | str) -> list[object] | str:  # type: ignore[override]
        if data == "":
            return ""
        return super().to_internal_value(data)  # type: ignore[arg-type]
