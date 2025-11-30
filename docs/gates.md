# Supported Gates

`pytket-custatevec` natively implements the following unitary gates using NVIDIA's `cuStateVec` kernels.

## Single Qubit Gates

| Gate | Symbol | Matrix Representation |
| :--- | :---: | :--- |
| **I** | $I$ | $\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$ |
| **X** | $X$ | $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ |
| **Y** | $Y$ | $\begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}$ |
| **Z** | $Z$ | $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ |
| **H** | $H$ | $\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$ |
| **S** | $S$ | $\begin{bmatrix} 1 & 0 \\ 0 & i \end{bmatrix}$ |
| **Sdg** | $S^\dagger$ | $\begin{bmatrix} 1 & 0 \\ 0 & -i \end{bmatrix}$ |
| **T** | $T$ | $\begin{bmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{bmatrix}$ |
| **V** / **SX** | $\sqrt{X}$ | $\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -i \\ -i & 1 \end{bmatrix}$ |

## Parameterized Single Qubit

| Gate | Definition | Matrix Form |
| :--- | :--- | :--- |
| **Rx** | $R_x(\theta)$ | $\begin{bmatrix} \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} \\ -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{bmatrix}$ |
| **Ry** | $R_y(\theta)$ | $\begin{bmatrix} \cos\frac{\theta}{2} & -\sin\frac{\theta}{2} \\ \sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{bmatrix}$ |
| **Rz** | $R_z(\theta)$ | $\begin{bmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{bmatrix}$ |
| **U1** | $U1(\lambda)$ | $\begin{bmatrix} 1 & 0 \\ 0 & e^{i\lambda} \end{bmatrix}$ |
| **U3** | $U3(\theta, \phi, \lambda)$ | $\begin{bmatrix} \cos\frac{\theta}{2} & -e^{i\lambda}\sin\frac{\theta}{2} \\ e^{i\phi}\sin\frac{\theta}{2} & e^{i(\phi+\lambda)}\cos\frac{\theta}{2} \end{bmatrix}$ |
| **PhasedX** | $R_x(\theta, \phi)$ | $R_z(\phi) R_x(\theta) R_z(-\phi)$ |
| **TK1** | $TK1(\alpha, \beta, \gamma)$ | $R_z(\alpha) R_x(\beta) R_z(\gamma)$ |

## Two Qubit Gates

| Gate | Description | Matrix / definition |
| :--- | :--- | :--- |
| **SWAP** | Swap states | $\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$ |
| **ECR** | Echoed Cross-Resonance | $\frac{1}{\sqrt{2}} \begin{bmatrix} 0 & 0 & 1 & i \\ 0 & 0 & i & 1 \\ 1 & -i & 0 & 0 \\ -i & 1 & 0 & 0 \end{bmatrix}$ |
| **ZZMax** | Maximal Entanglement | $e^{-i \frac{\pi}{4} Z \otimes Z} = \text{diag}(e^{-i\pi/4}, e^{i\pi/4}, e^{i\pi/4}, e^{-i\pi/4})$ |
| **XXPhase** | Ising XX | $e^{-i \frac{\theta}{2} X \otimes X}$ |
| **YYPhase** | Ising YY | $e^{-i \frac{\theta}{2} Y \otimes Y}$ |
| **ZZPhase** | Ising ZZ | $e^{-i \frac{\theta}{2} Z \otimes Z}$ |
| **ISWAP** | Swap + Phase | $\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & c & i s & 0 \\ 0 & i s & c & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}, \small{c=\cos(\frac{\theta}{2}), s=\sin(\frac{\theta}{2})}$ |

## Controlled Gates

Standard controlled gates are supported. The backend handles the control logic natively.

| Gate | Description |
| :--- | :--- |
| **CX, CY, CZ** | Controlled Pauli gates |
| **CH, CV, CS, CSX** | Controlled Clifford gates |
| **CCX** (Toffoli) | Doubly-Controlled X |
| **CSWAP** (Fredkin) | Controlled SWAP |
| **CRx, CRy, CRz** | Controlled Rotations |
| **CU1, CU3** | Controlled Unitaries |