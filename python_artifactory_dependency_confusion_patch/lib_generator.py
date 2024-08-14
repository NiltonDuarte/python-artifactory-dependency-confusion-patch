from pathlib import Path
import shutil

from python_artifactory_dependency_confusion_patch.domain.library import Library


class LibGenerator:
    default_libs_dir = Path("/tmp/pypi-libs")
    default_templates_dir = Path(__file__).parent / "lib_template"

    def __init__(self, lib: Library, templates_dir=None, libs_dir=None) -> None:
        self.library = lib
        self.lib_name = lib.name
        self.templates_dir = templates_dir or self.default_templates_dir
        self.libs_dir = libs_dir or self.default_libs_dir

    @classmethod
    def delete_lib_structure(cls, lib_path):
        shutil.rmtree(lib_path)

    def create_lib_structure(self) -> str:
        self.libs_dir.mkdir(exist_ok=True)
        lib_path = self.libs_dir.joinpath(self.lib_name)
        if lib_path.exists():
            shutil.rmtree(lib_path)
        lib_path.mkdir()
        lib_code_path = lib_path.joinpath(self.library.namespace)
        lib_code_path.mkdir(parents=True)
        self.create_readme_md(lib_path)
        self.create_pyproject_toml(lib_path)
        self.create_init_py(lib_code_path)
        return lib_path

    def create_readme_md(self, lib_path: Path):
        shutil.copy(self.templates_dir / "README.md", lib_path)

    def create_pyproject_toml(self, lib_path: Path):
        with open(self.templates_dir / "pyproject.toml", "r") as pyproject_template:
            pyproject_template = pyproject_template.read()
        with open(lib_path / "pyproject.toml", "w+") as pyproject_dst:
            pyproject_dst.write(pyproject_template.replace("{{project_name}}", self.lib_name))

    def create_init_py(self, lib_code_path: Path):
        with open(self.templates_dir / "__init__.py", "r") as init_template:
            init_template = init_template.read()
        with open(lib_code_path / "__init__.py", "w+") as init_dst:
            init_dst.write(init_template.replace("{{project_name}}", self.lib_name))

    @classmethod
    def from_lib_name(cls, lib_name):
        lib = Library(lib_name)
        return LibGenerator(lib)
