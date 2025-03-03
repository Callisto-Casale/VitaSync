from flask import Blueprint, jsonify, request

from app.database.ingredients_database import IngredientBase

ingredients_bp = Blueprint("ingredients", __name__)


@ingredients_bp.route("/amount")
def get_amount_of_ingredients():
    return jsonify({"amount": IngredientBase.return_amount_of_total_ingredients()})


@ingredients_bp.route("/search_ingredients", methods=["GET"])
def search_ingredients():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify([])

    results = IngredientBase.search_ingredients(query)
    return jsonify(results)


@ingredients_bp.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    data = request.get_json()

    name = data.get("name")
    unit = data.get("unit")
    price = data.get("price")

    if not name or not unit or price is None or price <= 0:
        return jsonify({"error": "Invalid ingredient data"}), 400

    ingredient_id = IngredientBase.add_ingredient(name, unit, price)

    if ingredient_id:
        return (
            jsonify(
                {
                    "message": f"Ingredient '{name}' added successfully!",
                    "ingredient_id": ingredient_id,
                }
            ),
            201,
        )
    else:
        return jsonify({"error": f"Ingredient '{name}' already exists."}), 409
