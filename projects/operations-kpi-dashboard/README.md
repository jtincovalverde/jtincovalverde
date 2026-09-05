# Operations Management Control Center

A management-oriented operations analysis project that turns capacity data into **KPIs, risk signals, bottleneck diagnosis, decision guidance and a targeted improvement scenario**.

> Portfolio lab created with AI-assisted development. The dataset is synthetic and contains no company- or university-confidential information.

## Management question

**Do we really need more capacity across the operation, or is the problem concentrated in one work center?**

The answer is important because adding people, overtime or equipment everywhere can increase cost without fixing the real constraint.

## Executive snapshot

| KPI | Result |
| --- | ---: |
| Required workload | **220.1 h** |
| Available capacity | **254.0 h** |
| Overall utilization | **86.7%** |
| Net system buffer | **33.9 h** |
| Local overloaded hours | **11.8 h** |
| Primary bottleneck | **Welding** |
| Welding utilization | **119.7%** |

### Key management insight

The system has **more total available capacity than required workload**, yet Welding is still overloaded.

That means the problem is **not simply “we need more resources.”** It is a localized capacity constraint.

**Management implication:** identify the constraint first, verify whether spare capacity elsewhere is transferable, and target the intervention where it changes system performance.

## Work-center diagnosis

| Work center | Required | Available | Utilization | Gap | Risk |
| --- | ---: | ---: | ---: | ---: | --- |
| Cutting | 42.5 h | 64.0 h | 66.4% | +21.5 h | HEALTHY |
| Welding | 71.8 h | 60.0 h | **119.7%** | **-11.8 h** | **CRITICAL** |
| Assembly | 56.2 h | 68.0 h | 82.6% | +11.8 h | HEALTHY |
| Finishing | 49.6 h | 62.0 h | 80.0% | +12.4 h | HEALTHY |

## Decision scenario

Before recommending a broad capacity increase, the project tests a focused scenario:

**Add 12 h of targeted capacity to Welding.**

| Welding scenario | Before | Targeted scenario |
| --- | ---: | ---: |
| Available capacity | 60.0 h | 72.0 h |
| Required workload | 71.8 h | 71.8 h |
| Utilization | 119.7% | **99.7%** |
| Capacity gap | -11.8 h | **+0.2 h** |

This removes the immediate overload, but a manager should still consider a larger safety buffer because utilization close to 100% leaves little resilience for variability, downtime, rework or demand growth.

## Management decision framework

1. **Observe** — identify where workload is accumulating.
2. **Measure** — calculate capacity, utilization and gaps.
3. **Diagnose** — separate a system-wide shortage from a local bottleneck.
4. **Evaluate alternatives** — transfer capacity, reschedule, add overtime or increase resources.
5. **Target the constraint** — avoid adding cost where it does not solve the problem.
6. **Measure again** — compare the intervention against the baseline.

## What the project produces

Running the analysis generates three management outputs:

- `management_summary.csv` — work-center KPI and risk table;
- `capacity_vs_load.svg` — capacity versus workload visualization;
- `executive_summary.md` — management diagnosis and recommended actions.

The repository also includes a ready-to-read [executive summary](executive_summary.md).

## Analysis logic

For each work center:

```text
Capacity gap = Available hours - Required hours
Utilization % = Required hours / Available hours × 100
```

Risk classification:

```text
Utilization > 100%  → CRITICAL
Utilization 90–100% → WATCH
Utilization < 90%   → HEALTHY
```

## Run locally

```bash
pip install -r requirements.txt
python analyze.py
```

## Project structure

```text
operations-kpi-dashboard/
├── README.md
├── analyze.py
├── operations_data.csv
├── management_summary.csv
├── executive_summary.md
├── capacity_vs_load.svg
└── requirements.txt
```

## What this demonstrates

This project is intentionally positioned around **management and operations**, not only programming. It demonstrates:

- operational KPI design;
- capacity planning;
- bottleneck identification;
- risk classification;
- scenario analysis;
- management interpretation of data;
- decision support;
- Python and Pandas automation;
- reproducible reporting.

## Why it matters

A manager should not react to operational pressure by adding resources blindly. Good administration means understanding **where capacity is actually constrained, which resources are underused, what can be transferred, and which intervention produces the highest operational impact for the lowest unnecessary cost**.

That is the purpose of this project.
