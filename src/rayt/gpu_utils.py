"""
Test script for Numba CUDA support.
Diagnoses CUDA capability issues with the RTX 5080.
"""
import numpy as np


try:
    from numba import cuda, types
    from numba.cuda.cudadrv.devicearray import DeviceNDArray
except ImportError:
    print("✗ Numba not installed")
    exit(1)


def test_cuda_availability() -> bool:
    """Test basic CUDA availability"""
    print("=== Testing CUDA Availability ===")

    try:
        print("✓ Numba CUDA import successful")
        print(f"✓ CUDA available: {cuda.is_available()}")

        if not cuda.is_available():
            print("✗ CUDA not available")
            return False

        return True
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_device_detection() -> bool:
    """Test CUDA device detection"""
    print("\n=== Testing Device Detection ===")

    try:

        # Test device count
        device_count = len(cuda.gpus)
        print(f"✓ Detected {device_count} CUDA device(s)")

        if device_count == 0:
            print("✗ No CUDA devices found")
            return False

        # Test device access
        for i in range(device_count):
            try:
                device = cuda.gpus[i]
                name = device.name.decode('utf-8') if hasattr(device.name, 'decode') else str(device.name)
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
    """Test CUDA context creation"""
    print("\n=== Testing Context Creation ===")

    try:
        from numba import cuda

        # Try to select device 0
        cuda.select_device(0)
        print("✓ Device 0 selected")

        # Try to get current device
        current = cuda.get_current_device()
        print(f"✓ Current device: {current.name.decode()}")

        return True
    except Exception as e:
        print(f"✗ Context creation failed: {e}")
        return False

def test_simple_kernel() -> bool:
    """Test simple CUDA kernel compilation and execution"""
    print("\n=== Testing Simple CUDA Kernel ===")

    try:
        from numba import cuda

        @cuda.jit
        def add_kernel(a: DeviceNDArray, b: DeviceNDArray, c: DeviceNDArray) -> None:
            idx = cuda.grid(1)
            if idx < len(c):
                c[idx] = a[idx] + b[idx]

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
        if np.allclose(result, np.full(n, 2.0)):
            print("✓ Kernel execution successful - results correct")
            return True
        else:
            print("✗ Kernel execution failed - incorrect results")
            return False

    except Exception as e:
        print(f"✗ Kernel test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_device_function() -> bool:
    """Test CUDA device function compilation"""
    print("\n=== Testing Device Functions ===")

    try:
        from numba import cuda

        @cuda.jit(device=True)
        def device_add(a: types.float32, b: types.float32) -> types.float32:
            return a + b

        @cuda.jit
        def test_kernel(a: DeviceNDArray, b: DeviceNDArray, c: DeviceNDArray) -> None:
            idx = cuda.grid(1)
            if idx < len(c):
                c[idx] = device_add(a[idx], b[idx])

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

        if np.allclose(result, np.full(n, 2.0)):
            print("✓ Device function test successful")
            return True
        else:
            print("✗ Device function test failed")
            return False

    except Exception as e:
        print(f"✗ Device function test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def detect_gpu_capabilities() -> None:
    """Run all CUDA tests"""
    print("CUDA Support Test for RTX 5080")
    print("=" * 40)

    tests = [
        test_cuda_availability,
        test_device_detection,
        test_context_creation,
        test_simple_kernel,
        test_device_function
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            results.append(False)

    print("\n" + "=" * 40)
    print("SUMMARY:")
    test_names = [
        "CUDA Availability",
        "Device Detection",
        "Context Creation",
        "Simple Kernel",
        "Device Functions"
    ]

    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")

    overall = all(results)
    print(f"\nOverall CUDA Support: {'WORKING' if overall else 'BROKEN'}")

    if not overall:
        print("\nTroubleshooting suggestions:")
        print("1. Check CUDA driver version compatibility")
        print("2. Try updating Numba: uv add numba@latest")
        print("3. Check environment: echo $CUDA_VISIBLE_DEVICES")
        print("4. RTX 5080 is very new - may need newer Numba/CUDA versions")
