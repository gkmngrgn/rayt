# RAYT - Ray Tracing with Python

## Overview
RAYT is a Python ray tracing application that follows Peter Shirley's "Ray Tracing" trilogy. It implements high-performance ray tracing using NumPy and Numba for CPU optimization, with optional CUDA support for GPU acceleration.

## Project Architecture
- **Language**: Python 3.13
- **Package Manager**: UV (Astral's fast Python package installer)
- **Core Dependencies**: NumPy, Numba, Matplotlib, Click
- **Optional GPU Support**: CuPy, Numba-CUDA
- **Project Structure**: 
  - `src/rayt/` - Main package with ray tracing components
  - `pyproject.toml` - Project configuration and dependencies
  - CLI entry points: `one-weekend` and `test-gpu`

## Current Setup
- Python 3.13 environment installed
- Dependencies installed via UV package manager
- Virtual environment located at `.pythonlibs/`
- CLI commands available through installed scripts

## Usage
The main CLI command generates ray-traced images in PPM format:
```bash
one-weekend --image-width=300 --samples-per-pixel=20 > image.ppm
```

Options:
- `--aspect-ratio`: Image aspect ratio (default: 16:9)
- `--image-width`: Image width in pixels (default: 300)
- `--samples-per-pixel`: Anti-aliasing samples (default: 20)
- `--max-depth`: Maximum ray bounce depth (default: 50)
- `--engine`: Rendering engine [cpu|gpu] (default: cpu)

## Performance
- Uses Numba JIT compilation for CPU optimization
- Optional CUDA support for GPU acceleration
- First run includes JIT compilation time
- Generates high-quality ray-traced scenes with materials (metal, glass, lambertian)

## Recent Changes
- 2025-09-11: Initial Replit environment setup completed
- Dependencies installed and tested successfully
- CLI functionality verified with test render

## Development Notes
- UV package manager provides fast dependency resolution
- Virtual environment isolated at `.pythonlibs/`
- PPM output format can be converted to other formats using external tools
- Project supports both CPU and GPU rendering modes