from python_artifactory_dependency_confusion_patch.lib_generator import LibGenerator


def test_lib_generator():
    lib_name = "lib-name"
    lib_gen = LibGenerator.from_lib_name(lib_name)
    lib_gen.create_lib_structure()
    with open(str(lib_gen.libs_dir / lib_name / "README.md"), "r") as f:
        content = f.read()
    assert content
    lib_gen.delete_lib_structure()
