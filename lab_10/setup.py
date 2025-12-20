from __future__ import annotations

import os

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


def openmp_flags(compiler_type: str):
    if compiler_type in ("unix", "mingw32"):
        return ["-fopenmp"], ["-fopenmp"]
    if compiler_type == "msvc":
        return ["/openmp"], []
    return [], []


class BuildExt(build_ext):
    def build_extensions(self):
        ct = self.compiler.compiler_type
        cflags, lflags = openmp_flags(ct)

        for ext in self.extensions:
            if os.environ.get("CYTHON_ANNOTATE", "").strip():
                ext.cython_directives = dict(
                    getattr(ext, "cython_directives", {}))
                ext.cython_directives["annotate"] = True

            if ext.name.endswith("integrate_nogil"):
                ext.extra_compile_args = (ext.extra_compile_args or []) + cflags
                ext.extra_link_args = (ext.extra_link_args or []) + lflags

        super().build_extensions()


ext_modules = [
    Extension("cython_mod.integrate_cy", ["cython_mod/integrate_cy.pyx"]),
    Extension("cython_mod.integrate_nogil", ["cython_mod/integrate_nogil.pyx"]),
]

setup(
    name="lab10_full",
    version="1.0.0",
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExt},
)
