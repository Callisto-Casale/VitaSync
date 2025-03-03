import os
import sqlite3
import sys
from typing import Dict, List, Optional, Union

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from config import Databases  # noqa: E402

DB_PATH = Databases.INGREDIENTS


class Ingredient:
    def __init__(self, id: int, name: str, unit: str, price: Union[int, float]) -> None:
        self.id = id
        self.name = name
        self.unit = unit
        self.price = price

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Ingredient name must be a non-empty string.")
        self._name = value.strip().capitalize()

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Unit must be a valid non-empty string.")
        self._unit = value.strip().lower()

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: Union[int, float]) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number.")
        self._price = float(value)

    def __repr__(self) -> str:
        return f"Ingredient(name='{self.name}', unit='{self.unit}', price={self.price:.2f})"

    def __str__(self) -> str:
        return f"{self.name} ({self.unit}) - ${self.price:.2f}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ingredient):
            return (self.name, self.unit, self.price) == (
                other.name,
                other.unit,
                other.price,
            )
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Ingredient):
            return self.name < other.name
        return NotImplemented

    def to_dict(self) -> Dict[str, str | float]:
        """Converts the Ingredient object to a dictionary representation."""
        return {"name": self.name, "unit": self.unit, "price": round(self.price, 2)}


class IngredientBase:
    """Handles database operations for ingredients."""

    @staticmethod
    def connect():
        """Creates a new database connection."""
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def init_db():
        """Creates the database table if it doesn’t exist."""
        with IngredientBase.connect() as conn:
            c = conn.cursor()
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    unit TEXT,
                    price REAL
                )
            """
            )
            conn.commit()

    @staticmethod
    def add_ingredient(name: str, unit: str, price: float) -> Optional[int]:
        """Inserts a new ingredient into the database and returns its ID."""
        with IngredientBase.connect() as conn:
            c = conn.cursor()
            try:
                c.execute(
                    "INSERT INTO ingredients (name, unit, price) VALUES (?, ?, ?)",
                    (name, unit, price),
                )
                conn.commit()
                return c.lastrowid
            except sqlite3.IntegrityError:
                print("Error: Ingredient already exists.")
                return None

    @staticmethod
    def get_ingredient(ingredient_id: int) -> Optional[Ingredient]:
        """Retrieves an ingredient by ID, ensuring price is a float."""
        with IngredientBase.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM ingredients WHERE id = ?", (ingredient_id,))
            row = c.fetchone()

            if row:
                ingredient_id, name, unit, price = row
                try:
                    price = float(price)
                except ValueError:
                    print(
                        f"Warning: Price for ingredient {name} is not a valid number: {price}"
                    )
                    return None

                return Ingredient(ingredient_id, name, unit, price)
        return None

    @staticmethod
    def get_all_ingredients() -> List[Dict[str, str | float]]:
        """Returns a list of all ingredients."""
        with IngredientBase.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM ingredients")
            rows = c.fetchall()

            return [
                {"id": row[0], "name": row[1], "unit": row[2], "price": row[3]}
                for row in rows
            ]

    @staticmethod
    def update_ingredient(
        ingredient_id: int,
        name: Optional[str] = None,
        unit: Optional[str] = None,
        price: Optional[float] = None,
    ) -> bool:
        """Updates an ingredient's details. Only provided fields will be updated."""
        with IngredientBase.connect() as conn:
            c = conn.cursor()
            updates = []
            params = []

            if name:
                updates.append("name = ?")
                params.append(name)
            if unit:
                updates.append("unit = ?")
                params.append(unit)
            if price is not None:
                updates.append("price = ?")
                params.append(price)

            if not updates:
                return False

            params.append(ingredient_id)
            query = f"UPDATE ingredients SET {', '.join(updates)} WHERE id = ?"
            c.execute(query, tuple(params))
            conn.commit()
            return c.rowcount > 0

    @staticmethod
    def delete_ingredient(ingredient_id: int) -> bool:
        """Deletes an ingredient by ID."""
        with IngredientBase.connect() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM ingredients WHERE id = ?", (ingredient_id,))
            conn.commit()
            return c.rowcount > 0

    @staticmethod
    def return_amount_of_total_ingredients():
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM ingredients;")
            count = cursor.fetchone()[0]

            return count
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def search_ingredients(query: str) -> List[Dict[str, Union[str, float]]]:
        """Search for ingredients by name with a max limit of 7 results."""
        with IngredientBase.connect() as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, name, unit, price FROM ingredients WHERE name LIKE ? LIMIT 7",
                (f"%{query}%",),
            )
            rows = c.fetchall()

            return [
                {"id": row[0], "name": row[1], "unit": row[2], "price": row[3]}
                for row in rows
            ]
