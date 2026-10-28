"""Import and functional guards for the opt-in component-tools package.

These checks supplement code review, explicit permission checks and fake
backends. They are not a security sandbox for arbitrary Python modification.
The import machinery may read Python source to load/reload a module; direct
application file opens, hardware imports and native calls remain forbidden.
"""

import builtins
from contextlib import contextmanager, ExitStack
import ctypes
import importlib
from pathlib import Path
import sys
from types import ModuleType
import unittest
from unittest.mock import patch


_ROOT = Path(__file__).resolve().parent.parent


class _ForbiddenLibraryLoader:
    def __getattr__(self, name):
        raise AssertionError("Unexpected native-library access: " + name)


@contextmanager
def component_io_guards():
    original_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        root = name.split(".", 1)[0]
        if root in {"tkinter", "serial", "msvcrt", "_tkinter"}:
            # Backend unit tests explicitly supply inert SimpleNamespace/object
            # substitutes in sys.modules. Never permit a real module here, even
            # if it was already imported elsewhere in the test process.
            substitute = sys.modules.get(root)
            if substitute is None or isinstance(substitute, ModuleType):
                raise AssertionError("Unexpected hardware import: " + name)
        return original_import(name, *args, **kwargs)

    targets = ("builtins.open", "io.open", "os.open", "os.read", "os.write",
               "os.fsync", "os.system", "subprocess.Popen", "signal.signal", "socket.socket",
               "socket.create_connection", "socket.getaddrinfo")
    with ExitStack() as stack:
        # Resolve these standard-library patch targets before blocking imports:
        # subprocess itself may import msvcrt without operating any device.
        for target in targets:
            stack.enter_context(patch(target, side_effect=AssertionError("Unexpected I/O: " + target)))
        stack.enter_context(patch("os.startfile", create=True,
                                  side_effect=AssertionError("Unexpected OS launch")))
        for target in ("WinDLL", "OleDLL", "CDLL", "PyDLL"):
            stack.enter_context(patch.object(ctypes, target, create=True,
                                            side_effect=AssertionError("Unexpected native call: " + target)))
        for target in ("windll", "oledll", "cdll", "pydll"):
            stack.enter_context(patch.object(ctypes, target, _ForbiddenLibraryLoader(), create=True))
        stack.enter_context(patch("builtins.__import__", side_effect=guarded_import))
        yield


class ComponentContainmentTests(unittest.TestCase):
    def test_all_component_imports_and_reloads_are_inert(self):
        root = _ROOT / "tv_autocal_tools"
        names = []
        for source in sorted(root.rglob("*.py")):
            relative = source.relative_to(_ROOT).with_suffix("")
            parts = relative.parts[:-1] if relative.name == "__init__" else relative.parts
            names.append(".".join(parts))
        self.assertIn("tv_autocal_tools.__main__", names)
        # Preserve original class identities held by already-imported tests.
        # reload mutates module dictionaries in place, so restore them afterward.
        originals = {name: (module, dict(module.__dict__))
                     for name, module in tuple(sys.modules.items())
                     if name == "tv_autocal_tools" or name.startswith("tv_autocal_tools.")}
        try:
            with component_io_guards():
                for name in names:
                    with self.subTest(module=name):
                        importlib.reload(importlib.import_module(name))
        finally:
            for name in tuple(sys.modules):
                if (name == "tv_autocal_tools" or name.startswith("tv_autocal_tools.")) and name not in originals:
                    del sys.modules[name]
            for name, (module, namespace) in originals.items():
                module.__dict__.clear()
                module.__dict__.update(namespace)
                sys.modules[name] = module

    def test_all_component_functional_cases_use_only_inert_backends(self):
        # Discover modules, not imported TestCase aliases, so unittest's main
        # discovery counts every case once. The guarded rerun is not extra cases.
        files = sorted((_ROOT / "tests").glob("test_component_*.py"))
        names = [path.stem for path in files if path.stem != "test_component_containment"]
        with component_io_guards():
            suite = unittest.TestSuite(
                unittest.defaultTestLoader.loadTestsFromModule(importlib.import_module(name))
                for name in names
            )
            expected = suite.countTestCases()
            result = unittest.TestResult()
            suite.run(result)
        self.assertGreater(expected, 0)
        self.assertEqual(result.testsRun, expected)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
        self.assertEqual(result.skipped, [])
