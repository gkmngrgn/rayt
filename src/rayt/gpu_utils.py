"""
CUDA GPU testing and diagnostic utilities.
Provides comprehensive CUDA capability detection and testing.
"""
import traceback
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

# Try to import CUDA dependencies
HAS_NUMBA_CUDA = True
CUDA_IMPORT_ERROR: Optional[str] = None

try:
    from numba import cuda, types
    from numba.cuda.cudadrv.devicearray import DeviceNDArray
    from numba.cuda.cudadrv.error import CudaSupportError
except ImportError as e:
    HAS_NUMBA_CUDA = False
    CUDA_IMPORT_ERROR = str(e)


# Module-level kernels to avoid recompilation
if HAS_NUMBA_CUDA:
    @cuda.jit
    def add_kernel(a: DeviceNDArray, b: DeviceNDArray, c: DeviceNDArray) -> None:
        """Simple addition kernel for testing."""
        idx = cuda.grid(1)
        if idx < len(c):
            c[idx] = a[idx] + b[idx]

    @cuda.jit(device=True)
    def device_add(a: types.float32, b: types.float32) -> types.float32:
        """Device function for testing."""
        return a + b

    @cuda.jit
    def test_kernel(a: DeviceNDArray, b: DeviceNDArray, c: DeviceNDArray) -> None:
        """Kernel that uses device function for testing."""
        idx = cuda.grid(1)
        if idx < len(c):
            c[idx] = device_add(a[idx], b[idx])


def is_cuda_available() -> Tuple[bool, Optional[str]]:
    """
    Check if CUDA is available.
    
    Returns:
        Tuple of (is_available, error_message)
    """
    if not HAS_NUMBA_CUDA:
        return False, f"Numba CUDA not available: {CUDA_IMPORT_ERROR}"
    
    try:
        available = cuda.is_available()
        if not available:
            return False, "CUDA runtime not available or no CUDA devices found"
        return True, None
    except (CudaSupportError, Exception) as e:
        return False, f"CUDA support error: {e}"


def safe_device_name(device) -> str:
    """Safely extract device name handling both bytes and str."""
    name = device.name
    if hasattr(name, 'decode'):
        return name.decode('utf-8')
    return str(name)


def get_environment_summary() -> Dict[str, Union[str, int, bool]]:
    """Get comprehensive CUDA environment information."""
    summary = {
        "numba_available": HAS_NUMBA_CUDA,
        "cuda_available": False,
        "device_count": 0,
        "devices": []
    }
    
    if not HAS_NUMBA_CUDA:
        summary["error"] = CUDA_IMPORT_ERROR
        return summary
    
    try:
        import numba
        summary["numba_version"] = numba.__version__
        summary["numpy_version"] = np.__version__
        
        cuda_available, error = is_cuda_available()
        summary["cuda_available"] = cuda_available
        
        if error:
            summary["error"] = error
            return summary
        
        # Get device information
        devices = cuda.gpus
        summary["device_count"] = len(devices)
        
        device_info = []
        for i, device in enumerate(devices):
            info = {
                "index": i,
                "name": safe_device_name(device),
                "compute_capability": f"{device.compute_capability[0]}.{device.compute_capability[1]}",
                "multiprocessors": getattr(device, "MULTIPROCESSOR_COUNT", "unknown"),
                "max_threads_per_block": getattr(device, "MAX_THREADS_PER_BLOCK", "unknown"),
                "total_memory": getattr(device, "TOTAL_MEMORY", "unknown")
            }
            device_info.append(info)
        
        summary["devices"] = device_info
        
    except Exception as e:
        summary["error"] = f"Failed to get environment info: {e}"
    
    return summary


def test_cuda_availability() -> bool:
    """Test basic CUDA availability."""
    print("=== Testing CUDA Availability ===")
    
    available, error = is_cuda_available()
    if available:
        print("✓ CUDA is available")
        return True
    else:
        print(f"✗ CUDA is not available: {error}")
        return False


def test_device_detection() -> bool:
    """Test CUDA device detection."""
    print("\n=== Testing Device Detection ===")
    
    available, error = is_cuda_available()
    if not available:
        print(f"✗ Skipping device detection: {error}")
        return False
    
    try:
        devices = cuda.gpus
        device_count = len(devices)
        print(f"✓ Detected {device_count} CUDA device(s)")
        
        if device_count == 0:
            print("✗ No CUDA devices found")
            return False
        
        # Test device access
        for i, device in enumerate(devices):
            try:
                name = safe_device_name(device)
                cc = device.compute_capability
                print(f"  Device {i}: {name}")
                print(f"    Compute Capability: {cc[0]}.{cc[1]}")
            except Exception as e:
                print(f"  Device {i}: Error accessing device - {e}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Device detection failed: {e}")
        return False


def test_context_creation() -> bool:
    """Test CUDA context creation."""
    print("\n=== Testing Context Creation ===")
    
    available, error = is_cuda_available()
    if not available:
        print(f"✗ Skipping context creation: {error}")
        return False
    
    try:
        # Try to select device 0
        cuda.select_device(0)
        print("✓ Device 0 selected")
        
        # Try to get current device
        current = cuda.get_current_device()
        name = safe_device_name(current)
        print(f"✓ Current device: {name}")
        
        return True
    except Exception as e:
        print(f"✗ Context creation failed: {e}")
        return False


def test_simple_kernel() -> bool:
    """Test simple CUDA kernel compilation and execution."""
    print("\n=== Testing Simple CUDA Kernel ===")
    
    available, error = is_cuda_available()
    if not available:
        print(f"✗ Skipping kernel test: {error}")
        return False
    
    try:
        print("✓ Kernel defined successfully")
        
        # Create test data
        n = 1024
        a = np.ones(n, dtype=np.float32)
        b = np.ones(n, dtype=np.float32)
        c = np.zeros(n, dtype=np.float32)
        
        print("✓ Test data created")
        
        # Transfer to GPU
        d_a = cuda.to_device(a)
        d_b = cuda.to_device(b)
        d_c = cuda.to_device(c)
        
        print("✓ Data transferred to GPU")
        
        # Launch kernel
        threads_per_block = 256
        blocks_per_grid = (n + threads_per_block - 1) // threads_per_block
        add_kernel[blocks_per_grid, threads_per_block](d_a, d_b, d_c)
        
        print("✓ Kernel launched")
        
        # Copy back result
        result = d_c.copy_to_host()
        print("✓ Result copied back")
        
        # Verify result
        expected = np.full(n, 2.0, dtype=np.float32)
        if np.allclose(result, expected):
            print("✓ Kernel execution successful - results correct")
            return True
        else:
            print("✗ Kernel execution failed - incorrect results")
            return False
    
    except Exception as e:
        print(f"✗ Kernel test failed: {e}")
        traceback.print_exc()
        return False


def test_device_function() -> bool:
    """Test CUDA device function compilation."""
    print("\n=== Testing Device Functions ===")
    
    available, error = is_cuda_available()
    if not available:
        print(f"✗ Skipping device function test: {error}")
        return False
    
    try:
        print("✓ Device function defined")
        
        # Test with small array
        n = 32
        a = np.ones(n, dtype=np.float32)
        b = np.ones(n, dtype=np.float32)
        c = np.zeros(n, dtype=np.float32)
        
        d_a = cuda.to_device(a)
        d_b = cuda.to_device(b)
        d_c = cuda.to_device(c)
        
        test_kernel[1, 32](d_a, d_b, d_c)
        result = d_c.copy_to_host()
        
        expected = np.full(n, 2.0, dtype=np.float32)
        if np.allclose(result, expected):
            print("✓ Device function test successful")
            return True
        else:
            print("✗ Device function test failed")
            return False
    
    except Exception as e:
        print(f"✗ Device function test failed: {e}")
        traceback.print_exc()
        return False


def detect_gpu_capabilities() -> Dict[str, Union[bool, List[str]]]:
    """
    Run all CUDA tests and return structured results.
    
    Returns:
        Dictionary with test results and environment summary
    """
    print("CUDA Support Test for GPU Capabilities")
    print("=" * 40)
    
    # Get environment summary
    env_summary = get_environment_summary()
    
    # Define tests
    tests = [
        ("CUDA Availability", test_cuda_availability),
        ("Device Detection", test_device_detection),
        ("Context Creation", test_context_creation),
        ("Simple Kernel", test_simple_kernel),
        ("Device Functions", test_device_function)
    ]
    
    results = {}
    passed_tests = []
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name.lower().replace(" ", "_")] = result
            if result:
                passed_tests.append(test_name)
            else:
                failed_tests.append(test_name)
        except Exception as e:
            print(f"✗ Test {test_name} crashed: {e}")
            results[test_name.lower().replace(" ", "_")] = False
            failed_tests.append(test_name)
    
    # Print summary
    print("\n" + "=" * 40)
    print("SUMMARY:")
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        display_name = test_name.replace("_", " ").title()
        print(f"{display_name}: {status}")
    
    overall_success = all(results.values())
    print(f"\nOverall CUDA Support: {'WORKING' if overall_success else 'BROKEN'}")
    
    # Return structured results
    return {
        "overall_success": overall_success,
        "test_results": results,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "environment": env_summary
    }