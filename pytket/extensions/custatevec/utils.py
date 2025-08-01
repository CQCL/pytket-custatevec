# Copyright Quantinuum  # noqa: D100
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pytket._tket.circuit import Circuit
from pytket._tket.unit_id import Bit
from pytket.circuit import OpType, Qubit


def _remove_meas_and_implicit_swaps(circ: Circuit) -> tuple[Circuit, dict[Qubit, Bit]]:
    """Converts a pytket Circuit to an equivalent circuit without measurements or implicit swaps.

    Measurements are extracted and returned as a mapping between qubits and bits.
    This function only supports end-of-circuit measurements. Any mid-circuit
    measurements or operations on classical bits will raise an error.

    Args:
        circ (Circuit): The input pytket Circuit.

    Returns:
        tuple[Circuit, dict[Qubit, Bit]]:
            - A new Circuit object with measurements and implicit swaps removed.
            - A dictionary mapping measured Qubits to their corresponding Bits.

    Raises:
        ValueError: If the circuit contains mid-circuit measurements or operations
        on classical bits.
    """
    pure_circ = Circuit()
    for q in circ.qubits:
        pure_circ.add_qubit(q)
    q_perm = circ.implicit_qubit_permutation()

    measure_map = {}
    # Track measured Qubits to identify mid-circuit measurement
    measured_qubits = set()

    for command in circ:
        cmd_qubits = [q_perm[q] for q in command.qubits]

        for q in cmd_qubits:
            if q in measured_qubits:
                raise ValueError("Circuit contains a mid-circuit measurement")

        if command.op.type == OpType.Measure:
            measure_map[cmd_qubits[0]] = command.bits[0]
            measured_qubits.add(cmd_qubits[0])
        else:
            if command.bits:
                raise ValueError("Circuit contains an operation on a bit")
            pure_circ.add_gate(command.op, cmd_qubits)

    pure_circ.add_phase(circ.phase)
    return pure_circ, measure_map
