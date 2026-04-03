# Lab 3: Status Accounting & Auditing — Report

## Quick Response Group | SEN 401 Lab Assessment


### Project Overview

The project is an **Inventory Stock Analysis** application built in Python. It reads a list of inventory items (each with a name, quantity, and unit price) and produces a formatted report showing total stock value, rankings, restock alerts, and summary statistics.

### Project Structure

```
task-3/
├── app.py                 Main entry point — displays the stock analysis report
├── inventory.py           Data module — validated inventory items (Pydantic)
├── requirements.txt       Python dependencies (tabulate, pydantic)
├── changelog.txt          Exported Git change log
├── README.md              This report
├── utils/
│   ├── __init__.py        Package initialiser
│   └── helpers.py         Utility functions for inventory analysis
```

---

## 2. Repository Setup

### Initialisation

The task-3 folder was created inside the existing repository on a dedicated `dev` branch:

```bash
git checkout -b dev/task-3-status-accounting-auditing
mkdir -p task-3/utils
```

### Files Created

| File | Purpose |
|---|---|
| `inventory.py` | Contains a list of inventory items, each with `item_name`, `quantity`, and `price`. Uses Pydantic `BaseModel` for validation. |
| `app.py` | Reads from `inventory.py` and calculates total stock value, rankings, alerts, and statistics. |
| `utils/helpers.py` | Helper functions: `highest_stock_item()`, `lowest_stock_item()`, `total_stock_value()`, `sort_by_stock_value()`, etc. |
| `requirements.txt` | Python dependencies (`tabulate`, `pydantic`). |
| `README.md` | Project description, instructions, and this lab report. |

### Setup Commands

```bash
cd task-3
pip install -r requirements.txt
python app.py
```


## 3. Software Maintenance Tasks

### 3.1 Corrective Maintenance

**Problem:** Helper functions would crash with `ValueError`, `ZeroDivisionError`, or `TypeError` when called with an empty inventory list.

**Fix Applied:** Every function in `utils/helpers.py` includes an empty-list guard that returns a safe default (`None`, `0.0`, or `0`) instead of raising an exception.

**Before (Vulnerable):**

```python
def highest_stock_item(items):
    return max(items, key=lambda item: item.stock_value)
```

**After (Guarded):**

```python
def highest_stock_item(items: list[InventoryItem]) -> InventoryItem | None:
    if not items:
        return None
    return max(items, key=lambda item: item.stock_value)
```

**Additionally**, `inventory.py` uses Pydantic validation to reject malformed data at creation time:

- `quantity` must be ≥ 0
- `price` must be > 0
- `item_name` must not be blank or whitespace-only

```python
class InventoryItem(BaseModel):
    item_name: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)
```

The `app.py` entry point also guards against an empty inventory list before running any analysis.

---

### 3.2 Adaptive Maintenance

**Goal:** Ensure compatibility with **Python 3.12+** and integrate a modern library feature.

**Changes:**

| Change | Detail |
|---|---|
| **Pydantic v2** | `InventoryItem` uses `BaseModel`, `Field`, and `field_validator` from Pydantic v2 |
| **Modern type hints** | `list[InventoryItem]`, `InventoryItem \| None` (PEP 604 union syntax) |
| **`from __future__ import annotations`** | Forward-reference support in `utils/helpers.py` |
| **`statistics.median`** | Standard library function used for median price calculation |
| **`@property` computed field** | `stock_value` is a computed property on the model: `quantity * price` |

---

### 3.3 Perfective Maintenance

**Goal:** Improve console output formatting and add useful functionality.

**Enhancements:**

| Enhancement | Detail |
|---|---|
| **Tabulate tables** | All output uses `tabulate` with `fancy_grid` format and column alignment |
| **Summary statistics** | Total items, total units, total stock value, average price, median price, highest/lowest value items |
| **Ranked inventory** | Full inventory sorted by stock value with rank numbers |
| **Restock alerts** | Items below a configurable threshold (default 50 units) flagged with ⚠️ |
| **Well-stocked items** | Items above the threshold displayed with ✅ |
| **Currency formatting** | All monetary values shown with `$` prefix and comma separators |

---

### 3.4 Preventive Maintenance

**Goal:** Refactor for readability and long-term maintainability.

**Actions:**

| Action | Detail |
|---|---|
| **Descriptive naming** | All functions, variables, and parameters use self-documenting names (e.g., `items_below_threshold`, `sort_by_stock_value`, `RESTOCK_THRESHOLD`) |
| **Module docstrings** | Every `.py` file has a top-level docstring describing its role |
| **Function docstrings** | Every function has a docstring explaining purpose, parameters, and return value |
| **Type annotations** | Full type hints on all function signatures |
| **Separation of concerns** | Data model (`inventory.py`), logic (`utils/helpers.py`), and presentation (`app.py`) are cleanly separated |
| **Display helpers** | `app.py` splits output into focused functions: `display_summary()`, `display_full_inventory()`, `display_restock_alerts()`, `display_well_stocked()` |
| **Constants** | `BORDER`, `DIVIDER`, `RESTOCK_THRESHOLD` defined as module-level constants |

---

## 4. Version Control Using Git

### Branch Strategy

A dedicated `dev` branch was created for all task-3 work:

```bash
git checkout -b dev-task-3-status-accounting-auditing
```

### Commit History

Each maintenance type was committed separately with a descriptive conventional-commit message:

| # | Commit Message | Maintenance Type |
|---|---|---|
| 1 | `feat: add inventory data module with Pydantic validation` | Setup + Corrective |
| 2 | `feat: add helper functions with empty-list guards and statistics` | Corrective + Adaptive |
| 3 | `feat: add main app with tabulate output, rankings, and restock alerts` | Perfective |
| 4 | `docs: add Lab 3 status accounting report and changelog` | Documentation |

### Viewing Commit History

```bash
# One-line summary
git log --oneline

# Detailed graph view
git log --oneline --graph --all

# Full log with author and date
git log --pretty=format:"%h | %an | %ad | %s" --date=short
```

>
> ```bash
> git log --oneline --graph --all
> ```

### Merge and Tag

```bash
git checkout main
git merge dev-task-3-status-accounting-auditing
git tag -a v1.2 -m "Release v1.2 — Lab 3: Status Accounting & Auditing Complete"
git push origin main --tags
```

>
> ```bash
> git tag -n
> ```

---

## 5. Git Change Logs

### Generating the Change Log

The change log is exported using Git's built-in log formatting:

```bash
git log --pretty=format:"%h | %an | %ad | %s" --date=short > task-3/changelog.txt
```

### Viewing Specific Author Contributions

```bash
# Commits by a specific author
git log --author="Michael" --oneline

# Summary of all contributors
git shortlog -sn
```

### Viewing Changes per File

```bash
# Files changed in each commit
git log --stat --oneline

# Detailed diff for a specific commit
git show <commit-hash>
```

>
> ```bash
> git log --pretty=format:"%h | %an | %ad | %s" --date=short
> ```

---

## 6. Configuration Status Accounting

### What is CSA?

**Configuration Status Accounting (CSA)** is the process of recording and reporting the status of configuration items (CIs) throughout the software lifecycle. It answers:

- **What** changed?
- **Who** changed it?
- **When** was it changed?
- **Why** was it changed?

### Configuration Items Tracked

| Configuration Item | Type | Location |
|---|---|---|
| `inventory.py` | Source Code (Data) | `task-3/inventory.py` |
| `app.py` | Source Code (Presentation) | `task-3/app.py` |
| `utils/helpers.py` | Source Code (Logic) | `task-3/utils/helpers.py` |
| `requirements.txt` | Dependency Manifest | `task-3/requirements.txt` |
| `README.md` | Documentation | `task-3/README.md` |
| `changelog.txt` | Change Log | `task-3/changelog.txt` |

### Branch Tracking

| Branch | Purpose | Status |
|---|---|---|
| `main` | Stable production branch | Active — contains all merged releases |
| `feature/task-1-student-score-analysis` | Task 1 feature work | Merged → `main` (v1.0) |
| `maint/task-2-software-maintenance` | Task 2 maintenance work | Merged → `main` (v1.1) |
| `dev-task-3-status-accounting-auditing` | Task 3 development work | Merged → `main` (v1.2) |

>
> ```bash
> git branch -a
> ```

### Release Tracking

| Tag | Description | Base Branch |
|---|---|---|
| `v1.0` | Baseline — Task 1 student score analysis | `main` |
| `v1.1` | Task 2 — Software maintenance complete | `main` |
| `v1.2` | Task 3 — Status accounting & auditing complete | `main` |

>
> ```bash
> git tag -n
> ```

### Commit-to-Maintenance Mapping

This table maps each commit to the specific maintenance task it addresses:

| Commit Hash | Message | Maintenance Type | Files Changed |
|---|---|---|---|
| *(hash)* | `feat: add inventory data module with Pydantic validation` | Corrective + Adaptive | `inventory.py`, `utils/__init__.py` |
| *(hash)* | `feat: add helper functions with empty-list guards and statistics` | Corrective + Adaptive | `utils/helpers.py`, `requirements.txt` |
| *(hash)* | `feat: add main app with tabulate output, rankings, and restock alerts` | Perfective + Preventive | `app.py` |
| *(hash)* | `docs: add Lab 3 status accounting report and changelog` | Documentation | `README.md`, `changelog.txt` |

>
> ```bash
> git log --stat --oneline
> ```

### CSA Summary Commands

Use these commands to perform status accounting at any time:

```bash
# List all branches (local and remote)
git branch -a

# List all tags with annotations
git tag -n

# Full commit history with graph
git log --oneline --graph --all --decorate

# Commits with files changed
git log --stat --oneline

# Formatted log for export
git log --pretty=format:"%h | %an | %ad | %s" --date=short

# Export to changelog
git log --pretty=format:"%h | %an | %ad | %s" --date=short > changelog.txt

# Compare two releases
git diff v1.1..v1.2 --stat
```

---


## 7. Results & Observations

### Key Results

- **Repository Structure:** The project follows a clean separation of concerns — data (`inventory.py`), logic (`utils/helpers.py`), and presentation (`app.py`).
- **Data Validation:** Pydantic v2 catches invalid inventory entries (negative quantities, zero prices, blank names) at creation time, not at runtime during analysis.
- **Comprehensive Output:** The report displays 7 summary metrics, a full ranked inventory table, and filtered views for low-stock and well-stocked items.
- **Full Audit Trail:** Every change is tracked through Git commits, branches, and tags. The `changelog.txt` provides an exportable record.

### Challenges Encountered

| Challenge | Resolution |
|---|---|
| Ensuring `stock_value` is always calculated consistently | Used a `@property` on the Pydantic model so the value is computed from validated `quantity` and `price` |
| Formatting currency values in tabulate columns | Used f-string formatting with `$` prefix and `:,.2f` specifier before passing to tabulate |
| Tracking which commits correspond to which maintenance type | Used conventional commit prefixes (`feat:`, `fix:`, `docs:`) and documented the mapping in the CSA section |

### CSA Observations

1. **Git log** provides a complete history of who changed what and when — the foundation of status accounting.
2. **Branching** isolates work-in-progress from the stable `main` branch, allowing parallel development without risk.
3. **Tagging** creates immutable milestones (`v1.0`, `v1.1`, `v1.2`) that can be checked out at any time to reproduce a specific release.
4. **Change logs** exported from Git serve as auditable records for stakeholders who may not use Git directly.
5. **`git diff` between tags** quickly reveals what changed between any two releases.

---

## 8. Conclusion

### Lessons Learned

1. **Configuration Status Accounting** is not just a bureaucratic exercise — it provides real value by making every change traceable and every release reproducible.
2. **Git is the primary CSA tool** for modern software projects. Its branching, tagging, and logging capabilities directly support status accounting requirements.
3. **Conventional commits** (`feat:`, `fix:`, `refactor:`, `docs:`) make the commit history self-documenting and easy to categorise by maintenance type.
4. **Exported change logs** bridge the gap between developers (who use Git) and managers/auditors (who need reports).
5. **Combining maintenance with CSA** ensures that every improvement — corrective, adaptive, perfective, or preventive — is recorded and can be audited.

### Importance of CSA in Software Engineering

- **Traceability:** Every line of code can be traced to a specific commit, author, and date.
- **Reproducibility:** Any tagged release can be checked out and rebuilt identically.
- **Accountability:** The commit history shows who made each change and why.
- **Compliance:** CSA records satisfy audit requirements in regulated industries.
- **Change Impact Analysis:** `git diff` between versions reveals the scope of changes for risk assessment.
