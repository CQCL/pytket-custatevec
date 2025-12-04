# Installation

`pytket-custatevec` requires **Python 3.10+** and a Linux machine with an **NVIDIA GPU** (Compute Capability 7.0+).

!!! info "Prerequisites"
    Ensure your machine has the **NVIDIA Drivers** installed and working (check with `nvidia-smi`).

    You generally do **not** need to install the full CUDA Toolkit system package, as the Python packages below include the necessary runtime libraries.

## 1. Install Dependencies

Select your package manager to install the required libraries.

=== "Conda (Recommended)"

    We recommend Conda because it reliably manages the system-level CUDA libraries alongside Python packages.

    ```bash
    # 1. Install NVIDIA libraries
    conda install -c conda-forge cuquantum-python

    # 2. Install the package
    pip install pytket-custatevec
    ```

=== "Pip"

    You can install everything via pip. This will automatically download the binary wheels for `cuquantum` and `cupy`.

    ```bash
    pip install pytket-custatevec
    ```

    !!! warning "Linux Requirements"
        If you see `ImportError: libcustatevec.so not found`, ensure you have a recent version of `pip` (`pip install --upgrade pip`) and a compatible Linux distribution (glibc 2.17+).

## 2. Verify Installation

You can check if the backend loads correctly by running this one-liner:

```bash
python -c "from pytket.extensions.custatevec import CuStateVecStateBackend; print('✅ Backend loaded successfully')"
```
