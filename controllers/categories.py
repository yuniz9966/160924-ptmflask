from models.categories import Category
from schemas.categories import CategoryBase
from models import db


def get_category_by_id(category_id):
    category=Category.query.get_or_404(category_id)
    return category


def get_all_categories() -> list[dict[str, int | str]]:
    categories = Category.query.all()

    categories_data = [
        {
            "id": category.id,
            "name": category.name
        }
        for category in categories
    ]

    return categories_data


def create_new_category(raw_data: dict[str, str]) -> Category:
    validated_obj = CategoryBase.model_validate(raw_data)

    new_obj = Category(name=validated_obj.name)

    db.session.add(new_obj)
    db.session.commit()

    return new_obj

