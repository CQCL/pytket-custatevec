import importlib.metadata
import os
import platform
import time

import cupy
import kaleido
import numpy as np
import pandas as pd
import plotly.express as px

from pytket import Circuit
from pytket.extensions.custatevec import CuStateVecShotsBackend, CuStateVecStateBackend

# --- CONFIGURATION ---
LAYERS = 10
MIN_QUBITS = 6
MAX_QUBITS = 30
STEP = 2
N_SHOTS = 1000
TIMEOUT_SEC = 120.0

# --- BACKEND DISCOVERY ---
backends_sv = {"pytket-custatevec": CuStateVecStateBackend}
backends_shots = {"pytket-custatevec": CuStateVecShotsBackend}

try:
    from pytket.extensions.qiskit.backends.aer import AerBackend, AerStateBackend
    backends_sv["pytket-qiskit"] = AerStateBackend
    backends_shots["pytket-qiskit"] = AerBackend
except ImportError:
    pass

try:
    from pytket.extensions.qulacs.backends.qulacs_backend import QulacsBackend
    backends_sv["pytket-qulacs"] = QulacsBackend
    backends_shots["pytket-qulacs"] = QulacsBackend
except ImportError:
    pass

# --- UTILS ---
def get_hardware_info():
    """Get formatted GPU and CPU names."""
    try:
        dev_id = 0
        props = cupy.cuda.runtime.getDeviceProperties(dev_id)
        gpu_name = props["name"].decode("utf-8")
        free_mem = cupy.cuda.Device(dev_id).mem_info[0]
    except:
        gpu_name = "Unknown GPU"
        free_mem = 0

    cpu_name = platform.processor()
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    cpu_name = line.split(":")[1].strip(); break
    except: pass
    return gpu_name, free_mem, cpu_name

def get_docs_assets_path():
    """Robustly finds the docs/assets folder relative to this script."""
    # Script is in <repo>/benchmarks/benchmark.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to <repo>/
    repo_root = os.path.dirname(script_dir)
    # Target <repo>/docs/assets
    assets_dir = os.path.join(repo_root, "docs", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    return assets_dir

def ensure_kaleido_chrome():
    """Ensures the Chrome engine for Kaleido is installed."""
    print("🔧 Checking Kaleido Chrome engine...")
    try:
        # This downloads a local chromium binary if not present
        kaleido.get_chrome_sync()
        print("✅ Kaleido Chrome engine ready.")
    except Exception as e:
        print(f"⚠️ Failed to install Kaleido Chrome: {e}")
        # We might continue, but static export will likely fail

def random_line_circuit(n_qubits: int, layers: int, measure: bool = False) -> Circuit:
    """Generates a random circuit with linear connectivity."""
    np.random.seed(42)
    c = Circuit(n_qubits)
    for i in range(layers):
        for q in range(n_qubits):
            c.TK1(np.random.rand(), np.random.rand(), np.random.rand(), q)

        offset = np.mod(i, 2)
        qubit_pairs = [[c.qubits[i], c.qubits[i+1]] for i in range(offset, n_qubits-1, 2)]
        for pair in qubit_pairs:
            if np.random.rand() > 0.5: pair = [pair[1], pair[0]]
            c.CX(pair[0], pair[1])

    if measure: c.measure_all()
    return c

# --- REPORTING ---
def generate_env_report(gpu_name, cpu_name):
    """Generates a markdown table with environment details."""

    def get_ver(pkg):
        try: return importlib.metadata.version(pkg)
        except: return "N/A"

    report = f"""
| Component | Specification / Version |
| :--- | :--- |
| **GPU** | {gpu_name} |
| **CPU** | {cpu_name} |
| **Python** | {platform.python_version()} |
| **OS** | {platform.system()} {platform.release()} |
| **pytket** | {get_ver("pytket")} |
| **pytket-custatevec** | {get_ver("pytket-custatevec")} |
| **pytket-qulacs** | {get_ver("pytket-qulacs")} |
| **pytket-qiskit** | {get_ver("pytket-qiskit")} |
| **cuquantum-python** | {get_ver("cuquantum-python")} |
"""
    output_dir = get_docs_assets_path()
    output_path = os.path.join(output_dir, "benchmark_env.md")

    with open(output_path, "w") as f:
        f.write(report.strip())
    print(f"✅ Generated Environment Report at {output_path}")

# --- BENCHMARK LOGIC ---
def run_comparison(mode="statevector"):
    results = []
    gpu_name, free_vram, cpu_name = get_hardware_info()

    target_backends = backends_sv if mode == "statevector" else backends_shots

    for n in range(MIN_QUBITS, MAX_QUBITS + 1, STEP):
        if (16 * (2**n)) > (free_vram * 0.9): break

        print(f"  - {n} qubits...")
        circ = random_line_circuit(n, LAYERS, measure=(mode=="shots"))

        for name, BackendClass in target_backends.items():
            is_cpu = "custatevec" not in name
            if is_cpu and n > 26: continue

            try:
                b = BackendClass()
                c_compiled = b.get_compiled_circuit(circ)
                start = time.time()

                if mode == "statevector":
                    _ = b.run_circuit(c_compiled).get_state()
                else:
                    _ = b.run_circuit(c_compiled, n_shots=N_SHOTS).get_counts()

                elapsed = time.time() - start
                results.append({"Qubits": n, "Time (s)": elapsed, "Backend": name})

                if is_cpu and elapsed > TIMEOUT_SEC: break
            except Exception: pass

    return pd.DataFrame(results), gpu_name, cpu_name

def save_plot(df, title, filename_base, gpu_name, cpu_name):
    """Saves interactive HTML (for Docs) and static PNG (for README).

    filename_base: string without extension (e.g. 'benchmark_sv').
    """
    output_dir = get_docs_assets_path()

    if df.empty:
        print(f"⚠️ Skipping plot {filename_base} (Empty Data)")
        return

    colors = {
        "pytket-custatevec": "#76b900",
        "pytket-qiskit": "#ff5722",
        "pytket-qulacs": "#29b6f6"
    }

    fig = px.line(
        df, x="Qubits", y="Time (s)", color="Backend", markers=True, log_y=True,
        title=f"<b>{title}</b>",
        color_discrete_map=colors
    )

    fig.add_annotation(
        text=f"GPU: {gpu_name} | CPU: {cpu_name} | Depth: {LAYERS}",
        xref="paper", yref="paper", x=0, y=1.05, showarrow=False,
        font=dict(size=11, color="#7f7f7f"),
        align="left"
    )

    fig.update_layout(
        font=dict(family="Roboto, sans-serif", size=14, color="#7f7f7f"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(128,128,128,0.1)",
        margin=dict(l=20, r=20, t=90, b=20),
        xaxis=dict(gridcolor="rgba(128,128,128,0.2)", showspikes=True),
        yaxis=dict(gridcolor="rgba(128,128,128,0.2)", exponentformat="power", dtick=1),
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.5)")
    )
    fig.update_traces(marker=dict(size=8), line=dict(width=3))

    # 1. Save HTML
    html_path = os.path.join(output_dir, f"{filename_base}.html")
    fig.write_html(html_path, include_plotlyjs="cdn", full_html=False)

    # 2. Save PNG (White background for README compatibility)
    png_path = os.path.join(output_dir, f"{filename_base}.png")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    fig.write_image(png_path, width=800, height=500, scale=2)

    print(f"✅ Saved {filename_base} (.html and .png) to {output_dir}")

if __name__ == "__main__":
    ensure_kaleido_chrome()

    df_sv, gpu, cpu = run_comparison("statevector")
    generate_env_report(gpu, cpu)

    save_plot(df_sv, "Statevector Simulation", "benchmark_sv", gpu, cpu)

    df_shots, _, _ = run_comparison("shots")
    save_plot(df_shots, "Shot-Based Simulation (1000 Shots)", "benchmark_shots", gpu, cpu)
