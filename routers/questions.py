from flask import Blueprint, request, jsonify, Response
from pydantic import ValidationError

from controllers.questions import (
    get_all_questions,
    create_new_question,
    get_question_by_id,
    update_question,
)
from schemas.questions import QuestionCreate, QuestionResponse

questions_bp = Blueprint(name="questions", import_name=__name__)


# @questions_bp.route('', methods=["GET"])
# def get_all_questions():
#     return "ALL QUESTIONS"
#
# @questions_bp.route('', methods=["POST"])
# def create_question():
#     return "CREATE QUESTION"
#
#
# @questions_bp.route('/<int:id>', methods=["GET"])
# def get_question_by_id(id: int):
#     return f"QUESTION - {id}"
#
#
# @questions_bp.route('/<int:id>', methods=["PUT"])
# def update_question(id: int):
#     return f"QUESTION UPDATE BY ID - {id}"
#
#
# @questions_bp.route('/<int:id>', methods=["DELETE"])
# def delete_question(id: int):
#     return f"QUESTION DELETE BY ID - {id}"



@questions_bp.route('', methods=["GET", "POST"])
def questions_list() -> Response | tuple[Response, int]:
    if request.method == "GET":
        questions = get_all_questions()

        return jsonify(questions)

    if request.method == "POST":
        data = request.json

        try:
            new_question = create_new_question(raw_data=data)
        except ValidationError as err:
            return jsonify(err.errors()), 400

        return jsonify(
            QuestionResponse(
                id=new_question.id,
                text=new_question.text,
                category_id=new_question.category_id
            ).model_dump()
        ), 201  # CREATED

# request.args => { "agree_count": True }
# http://127.0.0.1:5000/questions/?agree_count=ture
# Questions.query.order_by(desc(agree_count)).all()

@questions_bp.route('/<int:id>', methods=["GET", "PUT", "DELETE"])
# Реализовать эндпоинт на обновление конкретного вопроса по его ID
def retrieve_question(id: int):
    if request.method == "GET":
        question_by_id = get_question_by_id(id=id)
        if not question_by_id:
            return jsonify(
                {"Error": f"ID {id} not found."}
            ), 404

        return jsonify(question_by_id)

    if request.method == "PUT":
        question_by_id = get_question_by_id(id=id)
        if not question_by_id:
            return jsonify(
                {"Error": f"ID {id} not found."}
            ), 404
        data = request.json
        if not data or "text" not in data:
            return jsonify(
                {"Error": "No required field provided. ('text')"}
            ), 400
        updated_question = update_question(obj=question_by_id, new_data=data)
        return jsonify(
            {
                "id": updated_question.id,
                "text": updated_question.text
            }
        ), 200

    if request.method == "DELETE":
        return f"QUESTION DELETE BY ID - {id}"


