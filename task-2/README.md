# Lab 2: Software Maintenance Tasks — Report

## Quick Response Group | SEN 401 Lab Assessment

## 1. Introduction

### Purpose

This report documents the software maintenance activities performed on the `students.py` module and its supporting files from the Task 1 starter code. The objective is to apply the four recognised types of software maintenance — **Corrective**, **Adaptive**, **Perfective**, and **Preventive** — to improve the reliability, compatibility, usability, and maintainability of the student score analysis application.

### Role of `students.py`

`students.py` is the data module that stores all student records. It serves as the single source of truth consumed by `helpers/utils.py` (analysis functions) and `app.py` (main entry point). Any bug or structural weakness in this file propagates throughout the entire application, making it the ideal candidate for a maintenance exercise.

### Project Structure (Task 2 — After Maintenance)

```
task-2/
├── app.py                 # Main entry point (enhanced output)
├── models.py              # NEW — Pydantic data models for validation
├── students.py            # Student data (now uses validated models)
├── requirements.txt       # Updated dependencies
├── helpers/
│   ├── __init__.py        # Package docstring added
│   └── utils.py           # Refactored utility functions
```

---

## 2. Task Breakdown

| Maintenance Type | Goal | Actions Taken |
|---|---|---|
| **Corrective** | Fix existing bugs | Added empty-list guards to all utility functions; validated data with Pydantic to catch malformed records early |
| **Adaptive** | Environment compatibility | Updated code for Python 3.12+; added Pydantic v2 for data validation; used modern type hints (`list[]`, `\|` union) |
| **Perfective** | Improve usability | Added median score calculation; added letter-grade classification; enhanced console output with `tabulate` formatted tables |
| **Preventive** | Improve maintainability | Refactored into a `models.py` module; added comprehensive docstrings and inline comments to every function and module |

---

## 3. Step-by-Step Actions

### 3.1 Corrective Maintenance (Bug Fix)

**Problem Identified:** The original `helpers/utils.py` functions (`get_highest_scorer`, `get_lowest_scorer`, `get_average_score`) would crash with `ValueError`, `ZeroDivisionError`, or `IndexError` if the student list was empty.

**Before (Task 1 — Bug Present):**

```python
# task-1/helpers/utils.py — No empty-list protection
def get_highest_scorer(students):
    return max(students, key=lambda s: s["score"])  # ValueError if empty

def get_average_score(students):
    total = sum(s["score"] for s in students)
    return round(total / len(students), 2)           # ZeroDivisionError if empty
```


**After (Task 2 — Bug Fixed):**

```python
# task-2/helpers/utils.py — Empty-list guards added
def get_highest_scorer(students: list[Student]) -> Student | None:
    """Return the student with the highest score, or None if list is empty."""
    if not students:
        return None
    return max(students, key=lambda s: s.score)

def get_average_score(students: list[Student]) -> float:
    """Return the average score, or 0.0 if list is empty."""
    if not students:
        return 0.0
    total = sum(s.score for s in students)
    return round(total / len(students), 2)
```


**Additional Corrective Fix — Data Validation:**

The original `students.py` used plain dictionaries with no validation. A typo like `{"name": "", "score": 120}` would silently corrupt results.

```python
# task-2/models.py — Pydantic model prevents invalid data
class Student(BaseModel):
    name: str = Field(..., min_length=1, description="Student's full name")
    score: int = Field(..., ge=0, le=100, description="Student's score (0-100)")
```

**Git Command:**

```bash
git add task-2/helpers/utils.py task-2/models.py task-2/students.py
git commit -m "fix: add empty-list guards and Pydantic validation to prevent runtime errors"
```

---

### 3.2 Adaptive Maintenance (Environment Update)

**Goal:** Update the code to be compatible with **Python 3.12+** and include a new feature using a standard library or Pydantic.

**Changes Made:**

| Change | Detail |
|---|---|
| **Pydantic v2 integration** | Created `models.py` with a `Student` BaseModel using `Field` validators and `field_validator` decorators |
| **Modern type hints** | Replaced old-style `List[dict]` with `list[Student]` and `Student \| None` (PEP 604) |
| **`from __future__ import annotations`** | Added for forward-reference support in type hints |
| **`statistics.median`** | Used the standard library `statistics` module for median calculation |


**Git Command:**

```bash
git add task-2/models.py task-2/students.py task-2/requirements.txt
git commit -m "feat: adapt code for Python 3.12+ with Pydantic v2 data validation"
```

---

### 3.3 Perfective Maintenance (Enhancement)

**Goal:** Improve code readability, usability, and console output formatting.

**Changes Made:**

| Enhancement | Detail |
|---|---|
| **Median score** | Added `get_median_score()` using `statistics.median` |
| **Letter grades** | Added `grade_student()` function (A/B/C/F scale) |
| **Tabulate tables** | All console output now uses `tabulate` with `fancy_grid` format |
| **Emoji indicators** | Added  and  visual markers for report sections |
| **Section headers** | Clear visual separators between report sections |

**Before (Task 1 — Plain text output):**

```
==================================================
       STUDENT SCORE ANALYSIS
==================================================

Total Students: 10

Highest Scorer: Michael Lawrence with 95 points
Lowest Scorer: Confidence Ogboarote Ojenomoh with 55 points
```

**After (Task 2 — Enhanced tabulated output):**

```
============================================================
           STUDENT SCORE ANALYSIS REPORT
============================================================

------------------------------------------------------------
  Summary Statistics
------------------------------------------------------------
╒════════════════╤════════════════════════════════════╕
│ Metric         │ Value                              │
╞════════════════╪════════════════════════════════════╡
│ Total Students │ 10                                 │
├────────────────┼────────────────────────────────────┤
│ Average Score  │ 78.2                               │
├────────────────┼────────────────────────────────────┤
│ Median Score   │ 79.5                               │
├────────────────┼────────────────────────────────────┤
│ Highest Scorer │ Michael Lawrence (95)              │
├────────────────┼────────────────────────────────────┤
│ Lowest Scorer  │ Confidence Ogboarote Ojenomoh (55) │
╘════════════════╧════════════════════════════════════╛

------------------------------------------------------------
  Student Rankings (Highest → Lowest)
------------------------------------------------------------
╒════════╤═══════════════════════════════╤═════════╤═════════╕
│  Rank  │ Student Name                  │  Score  │  Grade  │
╞════════╪═══════════════════════════════╪═════════╪═════════╡
│   1    │ Michael Lawrence              │   95    │    A    │
│  ...   │ ...                           │  ...    │   ...   │
╘════════╧═══════════════════════════════╧═════════╧═════════╛
```

**Git Command:**

```bash
git add task-2/app.py task-2/helpers/utils.py
git commit -m "feat: enhance console output with tabulate tables, median score, and letter grades"
```

---

### 3.4 Preventive Maintenance (Refactoring)

**Goal:** Refactor code for improved modularity, maintainability, and documentation.

**Changes Made:**

| Refactoring Action | Detail |
|---|---|
| **Extracted `models.py`** | Separated data model definition from data, following Single Responsibility Principle |
| **Module docstrings** | Every `.py` file now has a top-level docstring explaining its purpose and the maintenance types applied |
| **Function docstrings** | Every function has a Google-style docstring with Args, Returns, and description |
| **Inline comments** | Section separators and meaningful comments added throughout |
| **Type annotations** | All function signatures have full type hints |
| **Package docstring** | `helpers/__init__.py` now has a descriptive docstring |

**Before (Task 1 — No docstrings):**

```python
# task-1/helpers/utils.py
def get_highest_scorer(students):
    return max(students, key=lambda s: s["score"])
```

**After (Task 2 — Full documentation):**

```python
# task-2/helpers/utils.py
def get_highest_scorer(students: list[Student]) -> Student | None:
    """
    Return the student with the highest score.

    Args:
        students: A list of Student objects.

    Returns:
        The Student with the highest score, or None if the list is empty.
    """
    if not students:
        return None
    return max(students, key=lambda s: s.score)
```

**Git Command:**

```bash
git add task-2/
git commit -m "refactor: add docstrings, type hints, and modular structure for maintainability"
```

---

## 4. Version Control with Git

### Branch Strategy

All maintenance changes were made on a dedicated branch following the `maint/*` naming convention:

```bash
git checkout -b maint/task-2-software-maintenance
```

### Commit History

| Commit | Message | Type |
|---|---|---|
| 1 | `fix: add empty-list guards and Pydantic validation to prevent runtime errors` | Corrective |
| 2 | `feat: adapt code for Python 3.12+ with Pydantic v2 data validation` | Adaptive |
| 3 | `feat: enhance console output with tabulate tables, median score, and letter grades` | Perfective |
| 4 | `refactor: add docstrings, type hints, and modular structure for maintainability` | Preventive |
| 5 | `docs: add Lab 2 maintenance report with step-by-step documentation` | Documentation |


### Merge & Tag

```bash
git checkout main
git merge maint/task-2-software-maintenance
git tag -a v1.1 -m "Release v1.1 — Software Maintenance Tasks Complete"
git push origin main --tags
```


## 5. Results & Observations

### Key Results

- **Corrective:** All utility functions now handle edge cases (empty lists) gracefully — no more runtime crashes. Data validation via Pydantic rejects invalid records at initialization time.
- **Adaptive:** The codebase is fully compatible with Python 3.12+. Pydantic v2 provides modern data validation with clear error messages.
- **Perfective:** The console report is now professional-looking with formatted tables, letter grades, and a median score metric. User experience significantly improved.
- **Preventive:** Every module and function is documented with docstrings. Type hints make the code self-documenting and IDE-friendly. The `models.py` extraction follows the Single Responsibility Principle.

### Challenges Encountered

| Challenge | Resolution |
|---|---|
| Pydantic v2 API differences from v1 | Used `field_validator` (v2) instead of `validator` (v1); followed migration guide |
| Type hint compatibility | Added `from __future__ import annotations` for forward references |
| `tabulate` formatting with Pydantic objects | Accessed model attributes via dot notation (`.name`, `.score`) instead of dict keys |

### Statistics Comparison

| Metric | Task 1 | Task 2 |
|---|---|---|
| Functions with docstrings | 0 / 7 | 11 / 11 |
| Functions with type hints | 0 / 7 | 11 / 11 |
| Empty-list guard coverage | 0 / 7 | 7 / 7 |
| Data validation | None | Pydantic v2 |
| Console output format | Plain text | Tabulated tables |
| Statistical metrics | Average only | Average + Median |

---

## 6. Conclusion

### Lessons Learned

1. **Corrective Maintenance** is essential even for seemingly simple code — edge cases like empty lists are easy to overlook but cause production failures.
2. **Adaptive Maintenance** ensures longevity — migrating to modern Python features and validated data models future-proofs the codebase.
3. **Perfective Maintenance** directly impacts user satisfaction — a well-formatted report is more useful than raw text output.
4. **Preventive Maintenance** pays dividends over time — docstrings, type hints, and modular design make future changes faster and safer.
5. **Version Control** using branching (`maint/*`) and tagging (`v1.1`) provides a clear audit trail of all changes and enables safe rollbacks.

### Importance of Version Control in Maintenance

- **Branching** isolates maintenance work from the stable `main` branch, preventing unfinished changes from affecting production.
- **Descriptive commits** (using conventional prefixes like `fix:`, `feat:`, `refactor:`, `docs:`) make the history self-documenting.
- **Tagging** (`v1.0` → `v1.1`) creates clear milestones and enables reproducible deployments.
- **Pull requests** facilitate code review before merging maintenance changes.

---
