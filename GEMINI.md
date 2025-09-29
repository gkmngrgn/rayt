# Project Overview

This project is a ray tracer implementation based on Peter Shirley's "Ray Tracing in One Weekend" book series. It's a hybrid Python and Rust application, with the performance-critical ray tracing logic written in Rust and exposed as a Python extension using `pyo3` and `maturin`. The Python part of the project provides a command-line interface (CLI) using the `click` library and leverages `numba` for CPU-based performance optimization and `numba-cuda` for GPU acceleration.

The project is structured to allow rendering on different backends:

*   **Numba (CPU):** Utilizes Numba's JIT compilation to accelerate the Python code on the CPU.
*   **CUDA (GPU):** Offloads the rendering process to NVIDIA GPUs using Numba's CUDA support.
*   **Rust:** The core ray tracing logic, including vector operations, hittable objects, materials, and camera, is implemented in Rust for maximum performance.

## Building and Running

The project uses `uv` as a package manager. The following commands are available to build and run the ray tracer:

### Basic Rendering (CPU)

```shell
uv run one-weekend --image-width=300 --samples-per-pixel=20 > image.ppm
```

### High-Quality Rendering (CPU)

```shell
uv run one-weekend --image-width=1200 --samples-per-pixel=100 > image.ppm
```

### GPU Rendering

To use the GPU-accelerated renderer, you need a CUDA-enabled NVIDIA GPU and the necessary drivers.

```shell
uv run one-weekend --image-width=300 --samples-per-pixel=20 --engine=gpu > image.ppm
```

### Testing GPU Availability

You can check if a compatible GPU is available with the following command:

```shell
uv run test-gpu
```

## Development Conventions

*   **Hybrid Python/Rust:** The project follows a hybrid development model. The core, performance-sensitive code is in Rust (`src/`), while the CLI, rendering orchestration, and optimization bindings are in Python (`src/rayt/`).
*   **Build System:** `maturin` is used to build the Rust code into a Python extension. The configuration is in `pyproject.toml`.
*   **Dependencies:** Python dependencies are managed with `uv` and are listed in `pyproject.toml`. Rust dependencies are managed with `cargo` and are listed in `Cargo.toml`.
*   **CLI:** The command-line interface is built with `click` and is defined in `src/rayt/cli.py`.
*   **Code Style:** The Python code follows standard Python conventions. The Rust code follows standard Rust conventions.
