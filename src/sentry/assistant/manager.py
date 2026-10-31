from collections.abc import Mapping


class AssistantManager:
    def __init__(self) -> None:
        self._guides: dict[str, int] = {}

    def add(self, guides: Mapping[str, int]) -> None:
        for guide_key, id in guides.items():
            self._guides[guide_key] = id

    def get_valid_ids(self) -> list[int]:
        return list(self._guides.values())

    def get_guide_id(self, guide: object) -> int | None:
        if not isinstance(guide, str):
            return None
        return self._guides.get(guide)

    def all(self) -> dict[str, int]:
        return self._guides
