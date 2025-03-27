from models.questions import Question

from models import db


def get_all_questions() -> list[dict[str, int | str]]:
    questions = Question.query.all()

    questions_data = [
        {
            "id": question.id,
            "text": question.text
        }
        for question in questions
    ]

    return questions_data


def create_new_question(raw_data: dict[str, str]) -> Question:
    new_obj = Question(text=raw_data["text"])

    db.session.add(new_obj)
    db.session.commit()

    return new_obj
