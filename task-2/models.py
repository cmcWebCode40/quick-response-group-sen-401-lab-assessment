"""
models.py — Pydantic data models for student records.

This module defines validated data structures using Pydantic (Adaptive Maintenance).
It ensures data integrity by enforcing type checks and value constraints on student records.
"""

from pydantic import BaseModel, Field, field_validator


class Student(BaseModel):
    """
    Represents a single student record with validated fields.

    Attributes:
        name (str): The full name of the student. Must not be empty.
        score (int): The student's score. Must be between 0 and 100 inclusive.
    """

    name: str = Field(..., min_length=1, description="Student's full name")
    score: int = Field(..., ge=0, le=100, description="Student's score (0-100)")

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        """Ensure the student name is not just whitespace."""
        if not v.strip():
            raise ValueError("Student name must not be blank or whitespace only")
        return v.strip()
