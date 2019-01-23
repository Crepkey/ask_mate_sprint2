from flask import Flask, render_template, request, redirect, url_for
import data_manager
import util
import copy

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    sorted_messages = data_manager.get_questions()
    return render_template('index.html', sorted_messages=sorted_messages)


@app.route('/question/<question_id>')
def get_question_details(question_id):
    """ Input: question_id = string
        Output: render_template with different attributes

        This function collects the questions'/answers' details for the table creating on the question_details.html

        ATTRIBUTES:
            question = {dictionary}
            question_header = {list}
            title = {string}
            answers = {list which has dictionaries}
            answers_header = {list}
        """
    question = data_manager.get_question_by_id(id=question_id)[0]
    title = question["title"]
    del question["title"]
    question_header = [header.replace("_", " ").capitalize() for header in question.keys()]

    answers = data_manager.get_answer_by_question_id(question_id=question_id)

    # This decision is necessary because if
    # a question doesn't have any answer then the program has to use another way to handle it

    if len(answers) > 0:
        answers_header = [header.replace("_", " ").capitalize() for header in answers[0].keys()]
    else:
        answers = [{'TEST': 'There are no answers here'}]
        answers_header = []

    return render_template('question_details.html',
                           question=question,
                           question_header=question_header,
                           title=title,
                           answers=answers,
                           answers_header=answers_header)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    else:
        new_question = {
            'title': request.form.get('title'),
            'message': request.form.get('message')
        }

        # Generating the final dictionary for the new question
        new_question_final = data_manager.collect_data(new_question)

        # Writing the new question to the csv
        data_manager.write_to_csv(new_question_final)

        # Generating the URL for the new question
        question_id = new_question_final['id']
        question_url = url_for('get_question_details', question_id=question_id)

        return redirect(question_url)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    """
    Add a new answer to the selected question
    on the Question Details page
    Args:
        question_id (string): the ID of the selected question
    Returns:
        question_url (string): the URL back to the selected question
    """
    if request.method == 'GET':
        return render_template('add_answer.html')
    else:
        new_answer = {'message': request.form.get('answer')}

        # Generating the final dictionary for the new answer
        new_answer_final = data_manager.collect_data(new_answer, header=data_manager.ANSWERS_HEADER)
        new_answer_final['question_id'] = question_id

        # Writing the new answer to the csv
        data_manager.write_to_csv(new_answer_final, data_manager.ANSWER_FILE_PATH)

        # Generating the URL for the question which the answer belongs to
        question_url = url_for('get_question_details', question_id=question_id)

        return redirect(question_url)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
