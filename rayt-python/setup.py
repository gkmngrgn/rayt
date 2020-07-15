import pathlib

from Cython.Build import cythonize
from setuptools import Extension, setup

ext_lib_dir = (pathlib.Path() / "rayt_cython").resolve()
ext_modules = cythonize(
    [Extension("rayt_python.vec3_2", [str(ext_lib_dir / "vec3.pyx")])]
)

setup(ext_modules=ext_modules)
