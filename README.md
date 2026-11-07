# Search for $B^- \rightarrow \Lambda_c^+ \overline{p} \ell^- \overline{\nu}$ decays at Belle II

## 📌 Project Overview
This repository contains core analysis scripts, configurations, and exploratory notebooks developed as part of my **M.Sc. Physics Master's Thesis** at the University of Bonn, focusing on the **Belle II experiment**. 

The primary objective of this specific module was to determine the **upper limit of the branching fraction** for the rare/semileptonic decay channel $B^- \rightarrow \Lambda_c^+ \overline{p} \ell^- \overline{\nu}$ in the **hadronic tag side**, incorporating rigorous evaluations of both statistical and key systematic uncertainty sources.

---

## 📂 Repository Structure

```text
B-toLambda_c-p-l-v/
├── README.md                              # Project documentation & methodology
├── configs/                               # YAML configuration files (Separated by analysis phase & channel)
│   ├── config.yaml                        # Main configuration for template fits (full dataset)
│   ├── config_electron.yaml               # Template fit parameters for the electron channel
│   ├── config_muon.yaml                   # Template fit parameters for the muon channel
│   ├── project_setup.yaml                 # Histogram generation & variable cuts (full dataset)
│   ├── project_setup_electron.yaml        # Histogram configuration for electron channel
│   ├── project_setup_muon.yaml            # Histogram configuration for muon channel
│   └── variable_registry.yaml             # Feature mapping and variable definitions for ntuples
├── scripts/                               # Python core scripts for execution and grid processing
│   ├── B_to_Lcplnu.py                     # Main steering script for analysis workflow
│   ├── SignMC_process.py                  # Monte Carlo signal processing & selection
│   └── Grid_submission.py                 # Job submission script for remote computing clusters (Grid/NAF)
└── notebooks/                             # Exploratory Data Analysis & statistical evaluation
    └── Data Exploration (Lcp had).ipynb   # Main notebook for fit studies & limit extraction
```

---

## 🔬 Methodology & Key Components

### 1. Main Steering Pipeline (`scripts/B_to_Lcplnu.py`)
- Acts as the central steering file for processing reconstructed event data.
- Dynamically loads selection criteria from the `configs/` directory to separate analysis parameters from executable logic.
- Executes candidate selection, vertex fitting, and event filtering for electron and muon channels.

### 2. Signal MC & Grid Processing (`scripts/SignMC_process.py` & `scripts/Grid_submission.py`)
- Standardizes signal Monte Carlo processing to evaluate reconstruction and tagging efficiencies.
- Automates job batching for execution on remote high-performance computing clusters (DESY NAF / Grid infrastructure).

### 3. Statistical Analysis & Limit Setting (`notebooks/Data Exploration (Lcp had).ipynb`)
- **Exploratory Data Analysis:** Signal/background separation and kinematic distribution validation.
- **Uncertainty Propagation:** Incorporates both statistical uncertainties and key systematic error contributions (e.g., tracking efficiencies, PID calibration, intermediate branching fractions).
- **Upper Limit Extraction:** Calculates the upper limit on the branching fraction ($\mathcal{B}$) in the hadronic reconstruction channel using statistical modeling procedures.

---

## 🛠️ Tech Stack & Tools
- **Languages:** Python, Bash
- **Data & Statistical Libraries:** Pandas, NumPy, SciPy, Matplotlib
- **Frameworks:** `basf2` (Belle II Analysis Software Framework), ROOT ecosystem
- **Environment & Infrastructure:** Linux / WSL, Git, High-Performance / Grid Computing
