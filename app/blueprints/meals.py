from database.meals_database import MealBase
from flask import Blueprint, jsonify, request

meals_bp = Blueprint("meals", __name__)


@meals_bp.route("/amount", methods=["GET"])
def get_meal_and_ingredient_amounts():
    """Returns the total count of meals and ingredients."""
    amounts = MealBase.return_amount_of_meals_and_ingredients()

    return jsonify({"amounts": [amounts["total_meals"], amounts["total_ingredients"]]})


@meals_bp.route("/total_ingredients")
def get_total_ingredients():
    return jsonify({"amount": MealBase.return_total_ingredients()})


@meals_bp.route("/get", methods=["GET"])
def get_all_meals():
    """Fetches all meals from the database and returns them as JSON."""
    meals = MealBase.get_all_meals()

    for meal in meals:
        if isinstance(meal["ingredients"], str):
            meal["ingredients"] = meal["ingredients"].split(", ")

    return jsonify({"meals": meals})


@meals_bp.route("/add_meal", methods=["POST"])
def add_meal():
    data = request.get_json()

    meal_name = data.get("name")
    ingredients = data.get("ingredients", [])
    category = data.get("category")
    instructions = data.get("instructions", "")
    cook_time = data.get("cook_time", 0)

    if not meal_name or not ingredients or not category:
        return jsonify({"error": "Missing required fields"}), 400

    meal_id = MealBase.add_meal(
        meal_name, ingredients, category, instructions, cook_time
    )

    if meal_id:
        return (
            jsonify(
                {
                    "message": f"Meal '{meal_name}' added successfully!",
                    "meal_id": meal_id,
                }
            ),
            201,
        )
    else:
        return jsonify({"error": f"Meal '{meal_name}' already exists."}), 409
