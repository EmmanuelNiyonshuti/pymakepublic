import importlib
import sys
import textwrap
import uuid
from pathlib import Path
from types import ModuleType

import pytest

from pymakepublic import DoubleExportsError


def import_temp_module(tmp_path: Path, source: str) -> ModuleType:
    file_name = f"pymakepublic_test_{str(uuid.uuid4())[:6]}"
    test_file = tmp_path / f"{file_name}.py"
    test_file.write_text(textwrap.dedent(source))

    spec = importlib.util.spec_from_file_location(file_name, test_file)
    assert spec is not None and spec.loader is not None, (
        f"could not build an import spec for {test_file}"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[file_name] = module
    try:
        spec.loader.exec_module(module)
        return module
    finally:
        sys.modules.pop(file_name, None)


def test_mark_pub(tmp_path: Path) -> None:
    module = import_temp_module(
        tmp_path,
        """
        from pymakepublic import pub

        @pub
        class Foo: ...

        @pub
        def bar(): ...

        def _private(): ...
        """,
    )

    assert module.__all__ == ["Foo", "bar"]
    assert "_private" in dir(module)


def test_pub_and_all_in_same_module_raises_exception(tmp_path: Path) -> None:
    with pytest.raises(DoubleExportsError):
        import_temp_module(
            tmp_path,
            """
            from pymakepublic import pub

            __all__ = ["something_else"]

            @pub
            def bar(): ...
            """,
        )
