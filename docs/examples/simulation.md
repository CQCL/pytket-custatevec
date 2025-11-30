# Simulation Examples

## Statevector Simulation

The `CuStateVecStateBackend` allows you to retrieve the full statevector of a quantum circuit. This example simulates a Bell State ($|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$).

```python
import numpy as np
from pytket import Circuit
from pytket.extensions.custatevec import CuStateVecStateBackend

# 1. Define a Bell State circuit
circ = Circuit(2)
circ.H(0).CX(0, 1)

# 2. Initialize the Statevector Backend
backend = CuStateVecStateBackend()

# 3. Compile the circuit for the backend
compiled_circ = backend.get_compiled_circuit(circ)

# 4. Run and retrieve the statevector
handle = backend.process_circuit(compiled_circ)
result = backend.get_result(handle)
statevector = result.get_state()

print("Statevector:", np.round(statevector, 3))
```

## Shot-based Sampling
The CuStateVecShotsBackend mimics a quantum computer by returning measurement counts.

```python
from pytket import Circuit
from pytket.extensions.custatevec import CuStateVecShotsBackend

# 1. Define a circuit with measurements
circ = Circuit(2, 2)
circ.H(0).CX(0, 1)
circ.measure_all()

# 2. Initialize the Shots Backend
backend = CuStateVecShotsBackend()
compiled_circ = backend.get_compiled_circuit(circ)

# 3. Run with a specific number of shots
handle = backend.process_circuit(compiled_circ, n_shots=1000)
result = backend.get_result(handle)

# 4. Get counts
counts = result.get_counts()
print("Counts:", counts)
```

## Calculating Expectation Values

You can calculate operator expectation values efficiently on the GPU without explicitly retrieving the full statevector.

```python
from pytket import Circuit, Qubit
from pytket.pauli import Pauli, QubitPauliString
from pytket.utils.operators import QubitPauliOperator
from pytket.utils.expectations import get_operator_expectation_value
from pytket.extensions.custatevec import CuStateVecStateBackend

# 1. Define a circuit
circ = Circuit(2)
circ.H(0).CX(0, 1)  # Bell state

# 2. Define an operator (e.g., Z0 * Z1)
op = QubitPauliOperator({
    QubitPauliString([Qubit(0), Qubit(1)], [Pauli.Z, Pauli.Z]): 1.0
})

# 3. Calculate expectation value
backend = CuStateVecStateBackend()
expectation = get_operator_expectation_value(circ, op, backend)

print(f"Expectation value <Z0 Z1>: {expectation}")
```