# Basis Order
By default, pytket uses ilo (Increasing Lexicographic Order). You can explicitly request dlo (Decreasing Lexicographic Order/Big Endian).

```python
from pytket import Circuit, BasisOrder
from pytket.extensions.custatevec import CuStateVecStateBackend

# Create state |01> (qubit 0 is 0, qubit 1 is 1)
circ = Circuit(2).X(1) 

backend = CuStateVecStateBackend()
compiled_circ = backend.get_compiled_circuit(circ)
result = backend.run_circuit(compiled_circ)

# pytket default (Little Endian): |01> corresponds to index 2 (binary 10 reversed)
print("ILO (Default):", result.get_state(basis=BasisOrder.ilo))

# Big Endian: |01> corresponds to index 1 (binary 01)
print("DLO:", result.get_state(basis=BasisOrder.dlo))
```