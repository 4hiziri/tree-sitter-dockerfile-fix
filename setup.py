from os import path
from sysconfig import get_config_var

from setuptools import Extension, find_packages, setup
from setuptools.command.build import build
from setuptools.command.egg_info import egg_info


class Build(build):
    def run(self):
        if path.isdir("queries"):
            dest = path.join(self.build_lib, "tree_sitter_dockerfile", "queries")
            self.copy_tree("queries", dest)
        super().run()


class EggInfo(egg_info):
    def find_sources(self):
        super().find_sources()
        self.filelist.recursive_include("queries", "*.scm")
        self.filelist.include("src/tree_sitter/*.h")


setup(
    packages=find_packages("bindings/python"),
    package_dir={"": "bindings/python"},
    package_data={
        "tree_sitter_dockerfile": ["*.pyi", "py.typed"],
        "tree_sitter_dockerfile.queries": ["*.scm"],
    },
    ext_package="tree_sitter_dockerfile",
    ext_modules=[
        Extension(
            name="_binding",
            sources=[
                "bindings/python/tree_sitter_dockerfile/binding.c",
                "src/parser.c",
                "src/scanner.c",
            ],
            define_macros=[
                ("PY_SSIZE_T_CLEAN", None),
                ("TREE_SITTER_HIDE_SYMBOLS", None),
            ],
            include_dirs=["src"],
            py_limited_api=not get_config_var("Py_GIL_DISABLED"),
        )
    ],
    cmdclass={
        "build": Build,
        "egg_info": EggInfo,
    },
    zip_safe=False,
)
