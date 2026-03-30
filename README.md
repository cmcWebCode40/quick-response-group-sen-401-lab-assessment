# Quick Response Group - SEN 401 Lab Assessment (Edited)

## Task 1: Modular Python Project

A modular Python application that manages and analyses student score data.

### Project Structure

```
task-1/
├── app.py                 Main entry point for the demo application
├── students.py            Data module containing the list of students
├── requirements.txt       Python package dependencies
├── helpers/
│   ├── __init__.py        Package initializer
│   └── utils.py           Utility functions for score analysis
```

### Modules

**students.py** — Stores student records as a list of dictionaries. Each student has a `name` and a `score`.

**helpers/utils.py** — Provides utility functions:
- `get_highest_scorer(students)` — Returns the student with the highest score.
- `get_lowest_scorer(students)` — Returns the student with the lowest score.
- `get_average_score(students)` — Calculates the average score across all students.
- `get_passing_students(students, passing_score)` — Filters students who passed.
- `get_failing_students(students, passing_score)` — Filters students who failed.
- `sort_students_by_score(students, descending)` — Sorts students by score.
- `get_student_count(students)` — Returns the total number of students.

**app.py** — Imports data from `students.py` and functions from `helpers/utils.py`, then runs a demo that prints a full score analysis report to the console.

### Setup and Usage

1. Navigate to the task-1 directory:
   ```bash
   cd task-1
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

### Requirements

- Python 3.8+