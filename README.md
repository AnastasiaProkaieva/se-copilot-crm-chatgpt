# Fluxora SE Copilot Demo

A demo of how a ChatGPT Enterprise workspace — with a custom Agent, Skills,
and a CRM Connector — could help a Sales Engineer at a fictional,
aggressively-scaling data/AI infrastructure company ("Fluxora") do their
day-to-day job.

This repo contains the **design spec**, the **synthetic CRM data
generator**, and the **ChatGPT Enterprise setup guide** for the demo. No
live system is connected — see "Scope" below.

## Contents

- `docs/superpowers/specs/2026-07-16-crm-agent-demo-design.md` — the full
  design spec: business narrative, agent/skill architecture, CRM data
  model, and script plan.
- `docs/superpowers/plans/2026-07-16-crm-agent-demo.md` — the
  implementation plan that produced this repo's code.
- `docs/chatgpt-enterprise-setup-guide.md` — step-by-step guidance for
  configuring the corresponding Agent, Skills, and Connector in a real
  ChatGPT Enterprise workspace.
- `scripts/generate_crm_data.py` — generates the synthetic CRM dataset.
- `output/*.csv` — the generated dataset (8 files, one per CRM object).

## Running the data generator

```bash
cd scripts
python3 generate_crm_data.py
```

Requires Python 3 and the `faker` package (`pip3 install faker`). Writes 8
CSV files to `../output/`. Uses a fixed random seed, so re-running produces
identical output.

Run the test suite with:

```bash
cd scripts/tests
python3 -m pytest -v
```

## Scope

This repo produces data and documentation only. It does not create any
agent, skill, or connector in a live ChatGPT Enterprise workspace, and does
not connect the generated data to any real CRM system.
