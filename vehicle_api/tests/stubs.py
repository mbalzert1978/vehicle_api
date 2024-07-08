from __future__ import annotations

from typing import Any


class AttrStub:
    def __init__(self, return_value: Any | None = None) -> None:
        self.__dict__["commands"] = []
        self.__dict__["return_value"] = return_value

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.__dict__["commands"].append(args)
        self.__dict__["commands"].append(kwargs)

        return self.__dict__.get("return_value")

    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__dict__["commands"][__name] = (__value,)


class Stub:
    def __init__(
        self,
        spec: type[Any] | None = None,
        return_value: Any | None = None,
        raise_on: str = "",
        raises: type[Exception] | None = None,
        attr_stub: AttrStub | None = None,
    ) -> None:
        self.spec = spec
        self.commands = {}
        self.raise_on = raise_on
        self.raises = raises
        self.attr_stub = attr_stub or AttrStub(return_value)

    def __enter__(self) -> Stub:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.commands["__exit__"] = (exc_type, exc_val, exc_tb)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)

    def __getattr__(self, attr: str) -> AttrStub:
        self._raise_on(attr)
        if self.spec and getattr(self.spec, attr, None) is None:
            raise AttributeError(attr)
        self.attr_stub.__dict__["func_name"] = attr
        return self.attr_stub

    def _raise_on(self, func_name: str) -> None:
        if func_name != self.raise_on or not self.raises:
            return
        raise self.raises
