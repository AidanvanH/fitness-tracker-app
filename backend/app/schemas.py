
from pydantic import BaseModel, Field, field_validator


class CategoryCreate(BaseModel):
    exercise_category_name: str = Field(min_length=1, max_length=100)

    @field_validator("exercise_category_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Category name cannot be empty.")

        return value


class CategoryResponse(BaseModel):
    exercise_category_id: int
    exercise_category_name: str
