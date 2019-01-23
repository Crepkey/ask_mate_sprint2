import connection

@connection.connection_handler
def get_questions(cursor):
    """
    This function returns all the questions (ID and Title)
    :param cursor:
    :return: A list of dictionaries
    """
    cursor.execute("""
                    SELECT id ,title FROM question;
                   """)
    names = cursor.fetchall()
    return names

@connection.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(id)s;
    """, {'id': id})
    names = cursor.fetchall()
    return names


@connection.connection_handler
def get_answer_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s;
    """, {'question_id': question_id})
    names = cursor.fetchall()
    return names


@connection.connection_handler
def add_question(cursor, new_question):
    """
    This function inserts a new row to the question table,
    after that it returns the id of the new question.

    :param new_question: Dictionary - It contains the data for the new question
    :return: Int - ID of the new question
    """
    cursor.execute("""
                    INSERT INTO question(submission_time, title, message)
                    VALUES
                     (%(submission_time)s, %(title)s, %(message)s);
                   """,
                   new_question)
    cursor.execute("""
                    SELECT id FROM question
                    WHERE title = %(title)s;
                       """,
                   new_question)
    id = cursor.fetchall()
    return id


@connection.connection_handler
def add_answer(cursor, new_answer):
    """
    This function inserts a new row to the answer table.

    :param new_answer: Dictionary - It contains the data for the new answer
    """
    cursor.execute("""
                    INSERT INTO answer(submission_time, question_id, message)
                    VALUES
                     (%(submission_time)s, %(question_id)s, %(message)s);
                   """,
                   new_answer)
