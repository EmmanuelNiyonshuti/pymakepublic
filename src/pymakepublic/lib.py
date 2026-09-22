from __future__ import annotations

import sys

from collections.abc import Callable
from functools import wraps
from typing import Protocol
from typing import TypeVar

class _Obj(Protocol):
    __name__: str
    __module__: str

_T = TypeVar("_T", bound=_Obj)

class DoubleExportsError(Exception):
    """
    raised when a module manually defines __all__ and also use @pub.
    """
    pass

class _PubAll(list[str]):
    pass

def pub(obj: _T) -> _T:
    module = sys.modules[obj.__module__]
    all_list = module.__dict__.get("__all__")

    if all_list is None:
        all_list = _PubAll()
        module.__dict__["__all__"] = all_list
    elif not isinstance(all_list, _PubAll):
        raise DoubleExportsError(
            f"{obj.__module__!r} defines __all__; use either @pub or manual __all__. not both! "
        )

    if obj not in all_list:
        all_list.append(obj.__name__)    
    return obj
