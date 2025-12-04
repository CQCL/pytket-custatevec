# API Reference

The `pytket-custatevec` package provides high-performance GPU backends for simulating quantum circuits.

## Available Backends

<div class="grid cards" markdown>

-   :material-vector-line: **Statevector Backend**
    ---
    Calculates the exact quantum state vector ($2^n$ amplitudes). Ideal for theoretical validation and calculating exact expectation values.

    [:octicons-arrow-right-24: Read Docs](state_backend.md)

-   :material-chart-bar: **Shots Backend**
    ---
    Simulates measurement sampling (shots). Use this to mimic the behavior of a real QPU or to test probabilistic algorithms.

    [:octicons-arrow-right-24: Read Docs](shots_backend.md)

</div>

## Comparison

Not sure which backend to use?

| Feature | `CuStateVecStateBackend` | `CuStateVecShotsBackend` |
| :--- | :--- | :--- |
| **Output** | Full Statevector (`np.ndarray`) | Measurement Counts (`dict`) |
| **Memory Usage** | High (scales exponentially $2^n$) | High (internal statevector) |
| **Primary Use** | Debugging, Exact Expectations | Sampling, QPU Emulation |
| **Basis Order** | Supports ILO & DLO | Supports ILO & DLO |
| **Noise** | Ideal (Noise-free) | Shot Noise (Sampling error) |

## Common Functionality

Both backends inherit from the `pytket` `Backend` class and support:

* **Compilation:** `get_compiled_circuit(circ)` handles implicit swaps and gate decomposition automatically.
* **GPU Acceleration:** Both utilize NVIDIA cuStateVec to accelerate tensor operations.
* **Context Management:** Both handle GPU memory resources efficiently.

!!! tip "Performance Note"
    For circuits with more than 30 qubits, ensure your GPU has sufficient VRAM. The statevector size doubles with every additional qubit.
