# pytket-custatevec

[![CI](https://img.shields.io/badge/build-passing-brightgreen?style=flat&logo=github)](https://github.com/CQCL/pytket-custatevec/actions)
[![PyPI](https://img.shields.io/badge/pypi-v0.0.1-blue?style=flat&logo=pypi)](https://pypi.org/project/pytket-custatevec/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?style=flat&logo=python)](https://pypi.org/project/pytket-custatevec/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green?style=flat)](https://github.com/CQCL/pytket-custatevec/blob/main/LICENSE)

**GPU-accelerated statevector simulation for pytket.**

`pytket-custatevec` acts as a bridge between Quantinuum's [pytket](https://tket.quantinuum.com/) compiler and NVIDIA's [cuQuantum](https://developer.nvidia.com/cuquantum-sdk) SDK, enabling massive speedups for statevector simulations.

---

## Why use this backend?

<div class="grid cards" markdown>

-   :material-speedometer: **High Performance**
    ---
    Leverage NVIDIA GPUs to simulate quantum circuits significantly faster than CPU-based simulators, especially for entangling gates.

-   :material-layers-triple: **Seamless Integration**
    ---
    Works as a standard `pytket` Backend. Just switch your backend import, and your existing code runs on the GPU immediately.

-   :material-memory: **Optimized Memory**
    ---
    Utilizes `cuStateVec`'s advanced memory management to handle large statevectors efficiently on GPU VRAM.

-   :material-lock-pattern: **Gate Support**
    ---
    Supports the full range of standard gates, automatic implicit swaps, and complex measurement scenarios.

</div>

## Architecture

This library sits directly on top of the NVIDIA cuQuantum stack.

```mermaid
graph LR
    User[User Code] -->|pytket Circuit| Backend[CuStateVecBackend]
    Backend -->|cuQuantum Python| SDK[NVIDIA cuStateVec]
    SDK -->|CUDA| GPU[NVIDIA GPU]
    
    style User fill:#f9f9f9,stroke:#333,stroke-width:2px
    style Backend fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    style SDK fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style GPU fill:#212121,stroke:#000,stroke-width:2px,color:#fff
```

## Quick Links

Not sure where to start?

<div class="grid cards" markdown>

-   **Get Started**
    ---
    Install the package and set up CUDA.

    [:octicons-arrow-right-24: Installation](installation.md)

-   **See Examples**
    ---
    Run your first simulation or expectation value.

    [:octicons-arrow-right-24: View Examples](examples/index.md)

-   **API Reference**
    ---
    Deep dive into the Backend classes.

    [:octicons-arrow-right-24: Read API](api/index.md)

</div>

## Bugs and Support

Please file bugs and feature requests on the [GitHub Issue Tracker](https://github.com/CQCL/pytket-custatevec/issues).