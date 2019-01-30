from flask import Flask, render_template, request, redirect, url_for, session
import data_manager
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():

    # This row is responsible for adding the current url to the session
    session['current_url'] = url_for('index')

    if request.method == 'GET':
        sorted_messages = data_manager.get_questions()
        return render_template('index.html', sorted_messages=sorted_messages)
    if request.method == 'POST':
        search_phrase = request.form.get('search_phrase')
        return redirect(url_for('search', search_phrase=search_phrase))


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

    session['current_url'] = url_for('get_question_details', question_id=question_id)

    question = data_manager.get_question_by_id(id=question_id)[0]
    title = question["title"]
    del question["title"]
    question_header = [header.replace("_", " ").capitalize() for header in question.keys()]

    answers = data_manager.get_answer_by_question_id(question_id=question_id)
    # This decision below is necessary because if
    # a question doesn't have any answer then the program has to use another way to handle it

    if len(answers) > 0:
        answers_header = [header.replace("_", " ").capitalize() for header in answers[0].keys()]
    else:
        answers_header = []

    return render_template('question_details.html',
                           question=question,
                           question_header=question_header,
                           title=title,
                           answers=answers,
                           answers_header=answers_header)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    """
    This function directs to a page with a form where we can add a new question,
    after that it inserts the new question to the database and redirects to the new question's page.
    """

    session['current_url'] = url_for('add_question')

    if request.method == 'GET':
        return render_template('add_question.html')

    if request.method == 'POST':

        # Generating the final dictionary for the new question
        new_question = {
            'submission_time': datetime.now(),
            'title': request.form.get('title'),
            'message': request.form.get('message')
        }

        # Writing the new question to the database and getting back the id of the new question
        question_id = data_manager.add_question(new_question)[0]['id']

        # Generating the URL for the new question
        question_url = url_for('get_question_details', question_id=question_id)

        return redirect(question_url)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    """
    This function directs to a page with a form where we can add a new answer to the selected question,
    after that it inserts the new answer to the database and redirects to the selected question's page.

    :param question_id: (string)- the ID of the selected question
    """

    session['current_url'] = url_for('add_answer', question_id=question_id)

    if request.method == 'GET':
        return render_template('add_answer.html', question_id=question_id)

    if request.method == 'POST':

        # Generating the final dictionary for the new answer
        new_answer = {
            'submission_time': datetime.now(),
            'question_id': int(question_id),
            'message': request.form.get('answer')
        }

        # Writing the new answer to the database
        data_manager.add_answer(new_answer)

        # Generating the URL for the question which the answer belongs to
        question_url = url_for('get_question_details', question_id=question_id)

        return redirect(question_url)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    """
    This function directs to a page with a form where we can edit an existing answer,
    after that it updates the database and redirects to the question_details page.
    :param answer_id: (string)- the ID of the selected answer
    """

    session['current_url'] = url_for('edit_answer', answer_id=answer_id)

    if request.method == 'GET':

        # Reading the original answer from the database
        answer_message = data_manager.get_answer_message_by_id(answer_id)[0]['message']
        return render_template('edit_answer.html', answer_id=answer_id, answer_message=answer_message)

    if request.method == 'POST':

        # Generating the new dictionary for the updated answer
        updated_answer = {
            'id': int(answer_id),
            'submission_time': datetime.now(),
            'message': request.form.get('answer')
        }

        # Updating the database and getting back the id of the question which the answer belongs to
        question_id = str(data_manager.update_answer(updated_answer)[0]['question_id'])

        # Generating the URL for the question which the answer belongs to
        question_url = url_for('get_question_details', question_id=question_id)

        return redirect(question_url)


@app.route('/search')
def search():
    session['current_url'] = url_for('search')
    found_questions = data_manager.search(request.args.get('search_phrase'))  #TODO
    return render_template('search_results.html', found_questions=found_questions)


@app.route('/theme', methods=['POST'])
def change_theme():
    session['theme'] = request.form.get('theme')
    return redirect(request.referrer)


if __name__ == "__main__":
    app.secret_key = 'FuckDaCSS'
    app.run(
        debug=True,
        port=5000
    )
