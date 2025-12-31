"""Py-Tree-sitter"""

from platform import system
import subprocess

from setuptools import Extension, setup


def pkg_config(args):
    return subprocess.check_output(
        ["pkg-config", *args, "libffi"]
    ).decode().split()

setup(
    packages=["tree_sitter"],
    include_package_data=False,
    package_data={
        "tree_sitter": ["py.typed", "*.pyi"]
    },
    ext_modules=[
        Extension(
            name="tree_sitter._binding",
            sources=[
                "tree_sitter/core/lib/src/lib.c",
                "tree_sitter/binding.c"
            ],
            include_dirs=[
                "tree_sitter/core/lib/include",
                "tree_sitter/core/lib/src"
            ],
            define_macros=[
                ("PY_SSIZE_T_CLEAN", None),
            ],
            undef_macros=[
                "TREE_SITTER_FEATURE_WASM",
            ],
            extra_compile_args=(
                ["-std=c11", "-Wno-unused-variable"] if system() != "Windows" else None
            ),
            extra_link_args=pkg_config(["--libs"]),
        )
    ]
)
