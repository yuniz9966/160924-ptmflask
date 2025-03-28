from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from controllers.categories import get_all_categories, create_new_category
from controllers.categories import CategoryBase

categories_bp = Blueprint(name='categories', import_name=__name__)

@categories_bp.route('', methods=["GET", "POST"])
def get_categories():
    if request.method == "GET":
        if request.method == "GET":
            categories = get_all_categories()

            return jsonify(categories)

    if request.method == "POST":
        data = request.json

        try:
            new_category = create_new_category(raw_data=data)
        except ValidationError as err:
            return jsonify(err.errors()), 400

        return jsonify(
            CategoryBase(
                id=new_category.id,
                name=new_category.name
            ).model_dump()
        ), 201


@categories_bp.route('<int:id>', methods=["GET"])
def retrieve_category(id):
    return f"CATEGORY {id}"