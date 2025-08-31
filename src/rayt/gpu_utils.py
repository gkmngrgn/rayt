"""GPU detection and fallback utilities for ray tracing"""

import sys
from typing import Literal

RenderEngine = Literal["cpu", "gpu"]


def detect_gpu_capabilities() -> tuple[bool, str]:
    """
    Detect GPU capabilities and return availability status with details.

    Returns:
        tuple: (is_available, details_message)
    """
    try:
        # First check if CuPy is available (required for GPU rendering)
        try:
            import cupy as cp
        except ImportError:
            return False, "Missing dependency: cupy. Install with: uv add --optional cuda"

        # Check basic CuPy functionality
        try:
            # Simple test to verify CUDA functionality
            test_array = cp.array([1, 2, 3])
            _ = test_array + 1

            # Get CuPy device info
            device_id = cp.cuda.get_device_id()
            device_count = cp.cuda.runtime.getDeviceCount()
            device_props = cp.cuda.runtime.getDeviceProperties(device_id)

            gpu_name = device_props['name'].decode('utf-8')
            compute_capability = f"{device_props['major']}.{device_props['minor']}"
            memory_mb = device_props['totalGlobalMem'] // (1024 * 1024)

            return True, f"GPU: {gpu_name}, Compute: {compute_capability}, Memory: {memory_mb}MB"

        except Exception as e:
            return False, f"CUDA runtime error: {str(e)}"

    except ImportError as e:
        missing_deps = []
        if "numba" in str(e).lower():
            missing_deps.append("numba")
        if "cupy" in str(e).lower():
            missing_deps.append("cupy")

        if missing_deps:
            return False, f"Missing dependencies: {', '.join(missing_deps)}. Install with: uv add --optional cuda"
        else:
            return False, f"Import error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def get_render_engine(prefer_gpu: bool = False, force_engine: RenderEngine | None = None) -> tuple[RenderEngine, str]:
    """
    Determine which render engine to use based on preferences and availability.

    Args:
        prefer_gpu: Whether to prefer GPU rendering when available
        force_engine: Force a specific engine (overrides other preferences)

    Returns:
        tuple: (selected_engine, reason_message)
    """
    if force_engine == "cpu":
        return "cpu", "CPU rendering forced by user"

    if force_engine == "gpu":
        gpu_available, gpu_details = detect_gpu_capabilities()
        if gpu_available:
            return "gpu", f"GPU rendering forced by user - {gpu_details}"
        else:
            return "cpu", f"GPU rendering forced but not available ({gpu_details}), falling back to CPU"

    # Auto-detection logic
    gpu_available, gpu_details = detect_gpu_capabilities()

    if prefer_gpu and gpu_available:
        return "gpu", f"GPU rendering preferred and available - {gpu_details}"
    elif prefer_gpu and not gpu_available:
        return "cpu", f"GPU rendering preferred but not available ({gpu_details}), using CPU"
    elif gpu_available:
        return "cpu", f"GPU available ({gpu_details}) but CPU preferred, using CPU"
    else:
        return "cpu", f"Using CPU rendering ({gpu_details})"


def print_gpu_info(file=None) -> None:
    """Print detailed GPU information for diagnostics"""
    if file is None:
        file = sys.stderr

    gpu_available, gpu_details = detect_gpu_capabilities()

    print("=== GPU Information ===", file=file)
    print(f"Status: {'Available' if gpu_available else 'Not Available'}", file=file)
    print(f"Details: {gpu_details}", file=file)

    if gpu_available:
        try:
            import cupy as cp

            device_count = cp.cuda.runtime.getDeviceCount()
            print(f"CUDA Devices: {device_count}", file=file)

            for i in range(device_count):
                device_props = cp.cuda.runtime.getDeviceProperties(i)
                gpu_name = device_props['name'].decode('utf-8')
                compute_capability = f"{device_props['major']}.{device_props['minor']}"
                memory_mb = device_props['totalGlobalMem'] // (1024 * 1024)

                print(f"  Device {i}: {gpu_name}", file=file)
                print(f"    Compute Capability: {compute_capability}", file=file)
                print(f"    Memory: {memory_mb} MB", file=file)

            # CuPy version info
            print(f"CuPy Version: {cp.__version__}", file=file)

            # Additional Numba CUDA info if available
            try:
                from numba import cuda
                print(f"Numba CUDA available: {cuda.is_available()}", file=file)
                if cuda.is_available():
                    print(f"Numba detected devices: {len(cuda.gpus)}", file=file)
            except Exception as e:
                print(f"Numba CUDA check failed: {e}", file=file)

        except Exception as e:
            print(f"Error getting detailed GPU info: {e}", file=file)

    print("========================", file=file)
