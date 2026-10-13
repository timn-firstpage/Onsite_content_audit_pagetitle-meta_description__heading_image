from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / '.venv'

    def test_platform_paths_are_derived_from_environment(self):
        from setup_runtime import python_path
        self.assertEqual(python_path(Path('.venv'), 'darwin'), Path('.venv/bin/python'))
        self.assertEqual(python_path(Path('.venv'), 'linux'), Path('.venv/bin/python'))
        self.assertEqual(python_path(Path('.venv'), 'win32'), Path('.venv/Scripts/python.exe'))

    def test_setup_uses_only_environment_python_and_bundled_requirements(self):
        import setup_runtime
        def create(path):
            path.mkdir()
            (path / 'pyvenv.cfg').write_text('test')
            executable = setup_runtime.python_path(path)
            executable.parent.mkdir()
            executable.touch()
        with patch.object(setup_runtime.venv.EnvBuilder, 'create', side_effect=create) as builder, \
             patch.object(setup_runtime.subprocess, 'run') as run:
            executable = setup_runtime.setup(self.path)
        builder.assert_called_once()
        commands = [call.args[0] for call in run.call_args_list]
        self.assertTrue(all(command[0] == str(executable) for command in commands))
        pip = next(c for c in commands if 'pip' in c)
        self.assertEqual(pip[1:5], ['-m', 'pip', 'install', '-r'])
        self.assertEqual(Path(pip[5]), Path(setup_runtime.__file__).resolve().parents[1] / 'requirements.txt')

    def test_existing_unrelated_directory_is_not_modified(self):
        from setup_runtime import setup
        self.path.mkdir()
        (self.path / 'keep.txt').write_text('keep')
        with self.assertRaises(ValueError):
            setup(self.path)
        self.assertEqual([p.name for p in self.path.iterdir()], ['keep.txt'])

    def test_check_only_does_not_create_or_install(self):
        import setup_runtime
        with self.assertRaises(ValueError):
            setup_runtime.setup(self.path, check_only=True)
        self.path.mkdir()
        (self.path / 'pyvenv.cfg').touch()
        executable = setup_runtime.python_path(self.path)
        executable.parent.mkdir()
        executable.touch()
        with patch.object(setup_runtime.venv.EnvBuilder, 'create') as builder, \
             patch.object(setup_runtime.subprocess, 'run') as run:
            setup_runtime.setup(self.path, check_only=True)
        builder.assert_not_called()
        self.assertTrue(all('pip' not in call.args[0] for call in run.call_args_list))


if __name__ == '__main__':
    unittest.main()
