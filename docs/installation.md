### Prerequisites
In order to use it, you need access to a Linux machine (or WSL) with an **NVIDIA GPU of Compute Capability +7.0** (check it [here](https://developer.nvidia.com/cuda-gpus)) and have `cuda-toolkit` installed.

```shell
sudo apt install cuda-toolkit
```

## Installation

!!! info "Prerequisites"
    Before installing, ensure you have an **NVIDIA GPU** (Compute Capability +7.0) and `cuda-toolkit` installed.

You can install the dependencies and the package using your preferred package manager.

=== "Conda (Recommended)"

    We recommend Conda to handle CUDA dependencies automatically.
    
    ```bash
    conda install -c conda-forge cuquantum-python
    pip install pytket-custatevec
    ```

=== "Pip"

    If you use pure pip, you must manage CUDA libraries manually.

    ```bash
    pip install pytket-custatevec
    ```

!!! warning "CUDA Version Matching"
    Ensure your `cupy` and `cuquantum` versions match your installed CUDA Toolkit version. [Read the official guide here](https://docs.nvidia.com/cuda/cuquantum/latest/getting-started/index.html).

---