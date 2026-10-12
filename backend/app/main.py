
import sqlite3

from fastapi import Depends, FastAPI, HTTPException, status

from app.database import get_db
from app.schemas import CategoryCreate, CategoryResponse

from capstone_project_3 import ExerciseCategory


app = FastAPI(
    title="Fitness Tracker API",
    description="API for managing fitness tracker data",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Fitness Tracker API is running"}


@app.get(
    "/exercise-categories",
    response_model=list[CategoryResponse],
)
def get_categories(
    db: sqlite3.Connection = Depends(get_db),
):
    return ExerciseCategory.view_all_categories(db)



@app.post(
    "/exercise-categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: CategoryCreate,
    db: sqlite3.Connection = Depends(get_db),
):
    try:
        category_id = ExerciseCategory.execute(
            category.exercise_category_name,
            db,
        )

        return {
            "exercise_category_id": category_id,
            "exercise_category_name": category.exercise_category_name,
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An exercise category with this name already exists.",
        )
