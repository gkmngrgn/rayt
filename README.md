# RAYT

Ray Tracing codes. I follow Peter Shirley's [Ray Tracing](https://raytracing.github.io/) trilogy. The goal is to have the same output with Python, solving the performance problems.

![](assets/image.png)

## How to Build

This project uses Python 3.13 and UV package manager.

```shell
# Basic rendering (300px wide, CPU engine)
uv run one-weekend --image-width=300 --samples-per-pixel=20 > image_numba.ppm

# High quality rendering, using rust
uv run one-weekend --image-width=1200 --samples-per-pixel=100 --engine=rust > image_rust.ppm

# GPU rendering (if CUDA available)
uv sync --group cuda
uv run one-weekend --image-width=2400 --samples-per-pixel=200 --engine=cuda > image_cuda.ppm
```

## Features

- **CPU Optimization**: Numba JIT compilation for fast CPU rendering
- **GPU Acceleration**: CUDA support for parallel GPU rendering
- **Depth of Field**: Camera blur effects with configurable aperture and focus distance
- **Materials**: Lambertian, Metal, and Dielectric (glass) materials
- **CLI Interface**: Configurable image dimensions, sampling, and rendering engines
