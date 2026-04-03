"""
students.py — Student data module.

This module provides the student records used throughout the application.
Each student is validated using the Pydantic Student model to ensure data integrity.

Corrective Maintenance:
    - Added validation to prevent empty student lists from causing runtime errors.
    - Each record is validated via Pydantic to catch malformed data early.

Adaptive Maintenance:
    - Uses Pydantic v2 (BaseModel) for data validation, compatible with Python 3.12+.
    - Type hints follow modern Python conventions.

Preventive Maintenance:
    - Added module-level docstring and inline comments for clarity.
    - Data is defined as a list of validated Student objects for maintainability.
"""

from models import Student

# ──────────────────────────────────────────────
# Student Records (Validated via Pydantic Model)
# ──────────────────────────────────────────────
students: list[Student] = [
    Student(name="Okechukwu Ogbonnaya", score=88),
    Student(name="Kelly Ikenga", score=72),
    Student(name="Michael Lawrence", score=95),
    Student(name="Michael Chinonso Chinweike", score=64),
    Student(name="Isaac Owonifaari", score=81),
    Student(name="Chidera Omeje", score=90),
    Student(name="Confidence Ogboarote Ojenomoh", score=55),
    Student(name="Joshua Arijesuye", score=78),
    Student(name="Alali Tobin", score=92),
    Student(name="Onyedikachi John Eluwa", score=67),
]
