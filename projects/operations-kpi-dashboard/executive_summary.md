# Executive Operations Summary

## Management question

**Does the operation need more capacity everywhere, or is the problem concentrated in one work center?**

The data indicates a **localized constraint**, not a system-wide shortage. Total available capacity is **254.0 h** against **220.1 h** of required workload, leaving a net system buffer of **33.9 h**. However, **Welding** is overloaded by **11.8 h** and reaches **119.7% utilization**.

## Executive KPIs

| KPI | Result |
| --- | ---: |
| Total required workload | 220.1 h |
| Total available capacity | 254.0 h |
| Overall utilization | 86.7% |
| Net system capacity buffer | 33.9 h |
| Local overloaded hours | 11.8 h |
| Positive buffer in non-overloaded centers | 45.7 h |
| Primary bottleneck | Welding |

## Work-center diagnosis

| Work center | Required | Available | Utilization | Gap | Risk |
| --- | ---: | ---: | ---: | ---: | --- |
| Cutting | 42.5 h | 64.0 h | 66.4% | +21.5 h | HEALTHY |
| Welding | 71.8 h | 60.0 h | 119.7% | -11.8 h | CRITICAL |
| Assembly | 56.2 h | 68.0 h | 82.6% | +11.8 h | HEALTHY |
| Finishing | 49.6 h | 62.0 h | 80.0% | +12.4 h | HEALTHY |

## Recommended management decision

1. **Do not add capacity everywhere by default.** The system has aggregate spare capacity.
2. **Address Welding first.** Its local gap is the immediate constraint.
3. **Check transferability before spending.** Determine whether spare capacity in other centers can realistically support Welding; capacity is not automatically interchangeable across skills, equipment, or routing.
4. **Test targeted capacity.** A scenario adding **12 h** to Welding raises local capacity to **72.0 h**, reducing utilization to **99.7%** and leaving a **0.2 h** buffer.
5. **Protect resilience.** A utilization level near 100% removes the overload but still leaves little protection against variability, downtime, rework, or demand growth.

## Management lesson

**Aggregate capacity can look healthy while one local constraint still limits the operation.** The management task is not simply to add resources; it is to identify where the constraint is, validate whether spare capacity is transferable, and target the intervention where it changes system performance.

---

*Portfolio lab using synthetic data for demonstration purposes.*
