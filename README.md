# Belle II Analysis: Upper Limit Extraction for $B \rightarrow \Lambda_c^+ p \ell \nu$ (Hadronic Channel)

## 📌 Project Overview
This repository contains core analysis scripts, configurations, and exploratory notebooks developed as part of my **M.Sc. Physics Master's Thesis** at the University of Bonn, focusing on the **Belle II experiment**. 

The primary objective of this specific module was to determine the **upper limit of the branching fraction** for the rare/semileptonic decay channel $B \rightarrow \Lambda_c^+ p \ell \nu$ in the **hadronic tag side**, incorporating rigorous evaluations of both statistical and key systematic uncertainty sources.

---

## 📂 Repository Structure

```text
B-toLambda_c-p-l-v/
├── README.md                   # Project documentation & methodology
├── configs/                    # YAML configuration files (Cuts, variables, steering parameters)
│   ├── config.yaml
│   ├── config_electron.yaml
│   ├── config_muon.yaml
│   ├── project_setup.yaml
│   └── variable_registry.yaml
├── scripts/                    # Python core scripts for execution and grid processing
│   ├── B_to_Lcplnu.py          # Main steering script for analysis workflow
│   ├── SignMC_process.py       # Monte Carlo signal processing & selection
│   └── Grid_submission.py      # Job submission script for remote computing clusters (Grid/NAF)
└── notebooks/                  # Exploratory Data Analysis & statistical evaluation
    └── Data Exploration (Lcp had).ipynb  # Main notebook for fit studies & limit extraction
