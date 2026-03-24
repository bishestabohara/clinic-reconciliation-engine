from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any


@dataclass
class SimpleCache:
    store: dict[str, Any] = field(default_factory=dict)

    def make_key(self, payload: Any) -> str:
        normalized = json.dumps(payload, sort_keys=True, default=str)
        return sha256(normalized.encode("utf-8")).hexdigest()

    def get(self, payload: Any) -> Any | None:
        return self.store.get(self.make_key(payload))

    def set(self, payload: Any, value: Any) -> Any:
        self.store[self.make_key(payload)] = value
        return value


cache = SimpleCache()
