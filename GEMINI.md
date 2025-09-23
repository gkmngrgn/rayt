# Project Overview

This project is a Python-based ray tracer that implements the techniques described in Peter Shirley's "Ray Tracing in One Weekend" series. It is designed to produce the same visual output as the original C++ code, but with the performance challenges of Python addressed through CPU and GPU optimization.

The ray tracer supports features like:

- **CPU and GPU Rendering:** The user can choose to render on the CPU using Numba for optimization, or on the GPU using CUDA for significant acceleration.
- **Advanced Materials:** The renderer supports diffuse (Lambertian), reflective (Metal), and refractive (Dielectric) materials.
- **Camera Effects:** It includes features like depth of field with configurable aperture and focus distance.
- **Command-Line Interface:** The project provides a CLI for easy configuration of image size, sample count, and rendering engine.

## Building and Running

The project uses the `uv` package manager for Python. The following commands are used to build and run the project:

- **Basic Rendering (CPU):**
  ```shell
  uv run one-weekend --image-width=300 --samples-per-pixel=20 > image.ppm
  ```
- **High-Quality Rendering (CPU):**
  ```shell
  uv run one-weekend --image-width=1200 --samples-per-pixel=100 > image.ppm
  ```
- **GPU Rendering (if CUDA is available):**
  ```shell
  uv run one-weekend --image-width=300 --samples-per-pixel=20 --engine=gpu > image.ppm
  ```
- **Test GPU Availability:**
  ```shell
  uv run test-gpu
  ```

## Development Conventions

- **Code Style:** The project follows the standard Python PEP 8 style guide.
- **Type Hinting:** The code uses type hints for improved readability and static analysis.
- **Modularity:** The code is organized into modules for different functionalities like camera, materials, and renderers.
- **Optimization:** The project uses Numba to optimize CPU-bound code and CUDA for GPU acceleration.
