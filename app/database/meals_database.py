import os
import sqlite3
import sys
from datetime import datetime
from typing import Dict, List, Optional, Union

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from config import Databases  # noqa: E402

from .ingredients_database import IngredientBase  # noqa: E402

DB_PATH = Databases.MEALS


class Meal:
    """Represents a Meal with name, ingredients, and category."""

    def __init__(
        self, id: int, name: str, ingredients: List[str], category: str
    ) -> None:
        self.id = id
        self.name = name
        self.ingredients = ingredients  # List of ingredient names
        self.category = category  # Example: Breakfast, Lunch, Dinner

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Meal name must be a non-empty string.")
        self._name = value.strip().capitalize()

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Category must be a valid non-empty string.")
        self._category = value.strip().capitalize()

    def to_dict(self) -> Dict[str, str | List[str]]:
        """Converts the Meal object to a dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
            "category": self.category,
        }

    def __repr__(self) -> str:
        return f"Meal(name='{self.name}', category='{self.category}', ingredients={self.ingredients})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Meal):
            return (self.name, self.category, self.ingredients) == (
                other.name,
                other.category,
                other.ingredients,
            )
        return False


class MealBase:
    """Handles database operations for meals."""

    @staticmethod
    def connect():
        """Creates a new database connection."""
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def init_db():
        """Creates the meals table if it doesn’t exist."""
        with MealBase.connect() as conn:
            c = conn.cursor()
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS meals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    ingredients TEXT NOT NULL,  -- Stored as comma-separated values
                    category TEXT NOT NULL
                )
            """
            )
            conn.commit()

    @staticmethod
    def add_meal(
        name: str,
        ingredients: List[Dict[str, Union[str, int]]],
        category: str,
        instructions: Optional[str],
        cook_time: int,
    ) -> Optional[int]:
        """Inserts a new meal into the database and returns its ID."""
        ingredients_str = ", ".join(
            [
                f"{item['name']} ({item['amount']} {item['unit']})"
                for item in ingredients
            ]
        )
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with MealBase.connect() as conn:
            c = conn.cursor()
            try:
                c.execute(
                    """
                    INSERT INTO meals (name, ingredients, category, instructions, cook_time, date) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        name,
                        ingredients_str,
                        category,
                        instructions,
                        cook_time,
                        created_at,
                    ),
                )
                conn.commit()
                return c.lastrowid
            except sqlite3.IntegrityError:
                print(f"Error: Meal '{name}' already exists.")
                return None

    @staticmethod
    def get_meal(meal_id: int) -> Optional[Meal]:
        """Retrieves a meal by ID."""
        with MealBase.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM meals WHERE id = ?", (meal_id,))
            row = c.fetchone()

            if row:
                meal_id, name, ingredients, category = row
                ingredients_list = ingredients.split(", ") if ingredients else []
                return Meal(meal_id, name, ingredients_list, category)
        return None

    @staticmethod
    def get_all_meals() -> List[Dict[str, str | List[str]]]:
        """Returns a list of all meals."""
        with MealBase.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM meals")
            rows = c.fetchall()

            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "category": row[2],
                    "ingredients": row[3].split(","),
                }
                for row in rows
            ]

    @staticmethod
    def update_meal(
        meal_id: int,
        name: Optional[str] = None,
        ingredients: Optional[List[str]] = None,
        category: Optional[str] = None,
    ) -> bool:
        """Updates a meal's details. Only provided fields will be updated."""
        with MealBase.connect() as conn:
            c = conn.cursor()
            updates = []
            params = []

            if name:
                updates.append("name = ?")
                params.append(name)
            if ingredients is not None:
                updates.append("ingredients = ?")
                params.append(", ".join(ingredients))  # Convert list to string
            if category:
                updates.append("category = ?")
                params.append(category)

            if not updates:
                return False

            params.append(meal_id)
            query = f"UPDATE meals SET {', '.join(updates)} WHERE id = ?"
            c.execute(query, tuple(params))
            conn.commit()
            return c.rowcount > 0

    @staticmethod
    def delete_meal(meal_id: int) -> bool:
        """Deletes a meal by ID."""
        with MealBase.connect() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
            conn.commit()
            return c.rowcount > 0

    @staticmethod
    def return_total_meals() -> int:
        """Returns the total number of meals in the database."""
        try:
            with MealBase.connect() as conn:
                c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM meals;")
                return c.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0

    @staticmethod
    def return_total_ingredients_in_meals() -> int:
        """Returns the total count of ingredients used in all meals."""
        try:
            with MealBase.connect() as conn:
                c = conn.cursor()
                c.execute("SELECT ingredients FROM meals;")
                rows = c.fetchall()

                all_ingredients = []
                for row in rows:
                    if row[0]:
                        all_ingredients.extend(row[0].split(", "))

                return len(all_ingredients)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0

    @staticmethod
    def return_amount_of_meals_and_ingredients():
        """Returns the total number of meals and total number of ingredients used across all meals."""
        try:
            with MealBase.connect() as conn:
                c = conn.cursor()

                # Count total meals
                c.execute("SELECT COUNT(*) FROM meals;")
                meal_count = c.fetchone()[0]

                # Count total unique ingredients from IngredientBase
                ingredients_count = IngredientBase.return_amount_of_total_ingredients()

                return {
                    "total_meals": meal_count,
                    "total_ingredients": ingredients_count,
                }
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"total_meals": 0, "total_ingredients": 0}
