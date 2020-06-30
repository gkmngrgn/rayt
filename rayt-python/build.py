import pathlib

from setuptools import Extension

ext_lib_dir = (pathlib.Path() / "rayt_c").resolve()
ext_lib_config = dict(
    define_macros=[("NDEBUG", None)],
    include_dirs=[ext_lib_dir],
    sources=[str(ext_lib_dir / "ray_color.c"), str(ext_lib_dir / "rayt_c_module.c"),],
)
ext_modules = [Extension("rayt_python.ray_color", **ext_lib_config)]


def build(setup_kwargs):
    setup_kwargs.update({"ext_modules": ext_modules})
