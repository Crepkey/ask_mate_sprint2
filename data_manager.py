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


@connection.connection_handler
def get_answer_message_by_id(cursor, id):
    cursor.execute("""
                    SELECT message FROM answer
                    WHERE id = %(id)s;
    """, {'id': id})
    names = cursor.fetchall()
    return names


@connection.connection_handler
def update_answer(cursor, updated_answer):
    """
    This function updates a row in the answer table.

    :param updated_answer: Dictionary - It contains the data for the updated answer
    :return: Int - ID of the question which the answer belongs to
    """
    cursor.execute("""
                    UPDATE answer
                    SET submission_time=%(submission_time)s,
                    message=%(message)s 
                    WHERE id=%(id)s;
                   """,
                   updated_answer)
    cursor.execute("""
                        SELECT question_id FROM answer
                        WHERE message = %(message)s;
                           """,
                   updated_answer)
    id = cursor.fetchall()
    return id

@connection.connection_handler
def search(cursor, search_phrase):
    cursor.execute("""
                     SELECT id FROM question
                     WHERE title LIKE %(search_phrase)s OR message LIKE %(search_phrase)s
                     UNION
                     SELECT question_id FROM answer
                     WHERE message LIKE %(search_phrase)s;
                   """,
                   {'search_phrase': '%' + search_phrase + '%'})
    found_questions = cursor.fetchall()
    if found_questions:
        ids = []
        for question in found_questions:
            for id in question.values():
               ids.append(id)
        ids = tuple(ids)
        cursor.execute("""
                             SELECT * FROM question
                             WHERE id IN %s;
                           """, (ids,))
        questions = cursor.fetchall()
        return questions

