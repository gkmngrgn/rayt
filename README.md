# RAYT

## Build C++ Project

CMake will generate makefiles for your operating system. If you didn't use CMake before, take a look at the documentation to learn how to build a C++ project. Example usage:

```
cd rayt-cpp
cmake . -G "NMake Makefiles" -B build
cd build
nmake
rayt-cpp.exe > image.ppm
```

If you are on Windows, open solution file (rayt-cpp.sln) with Visual Studio and build it using the IDE.

I didn't try the project on Ubuntu yet, will write here how to do that later.


## Build Rust Project

**TODO:**

## Build Python Project

I tested the project using the latest stable version of Python (3.8). Use poetry to manage commands and dependencies.

```
cd rayt-python
poetry run rayt
```
