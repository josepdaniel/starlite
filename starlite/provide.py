from typing import TYPE_CHECKING, Any, Dict, Optional, cast

from starlite.types import Empty
from starlite.utils import AsyncCallable, is_async_callable

if TYPE_CHECKING:
    from typing import Type

    from pydantic.typing import AnyCallable

    from starlite.signature import SignatureModel


class Provide:
    """A wrapper class used for dependency injection.

    Args:
        dependency (AnyCallable): callable to inject, can be a function, method or class.
        use_cache (bool): cache the dependency return value. Defaults to False.
        sync_to_thread (bool): run sync code in an async thread. Defaults to False.
    """

    __slots__ = ("dependency", "use_cache", "value", "signature_model")

    def __init__(self, dependency: "AnyCallable", use_cache: bool = False, sync_to_thread: bool = False):

        self.dependency = cast("AnyCallable", AsyncCallable(dependency) if sync_to_thread else dependency)
        self.use_cache = use_cache
        self.value: Any = Empty
        self.signature_model: Optional["Type[SignatureModel]"] = None

    async def __call__(self, **kwargs: Dict[str, Any]) -> Any:
        """Proxies call to 'self.proxy'."""

        if self.use_cache and self.value is not Empty:
            return self.value

        if is_async_callable(self.dependency):
            value = await self.dependency(**kwargs)
        else:
            value = self.dependency(**kwargs)

        if self.use_cache:
            self.value = value

        return value

    def __eq__(self, other: Any) -> bool:
        # check if memory address is identical, otherwise compare attributes
        return other is self or (
            isinstance(other, self.__class__)
            and other.dependency == self.dependency
            and other.use_cache == self.use_cache
            and other.value == self.value
        )
