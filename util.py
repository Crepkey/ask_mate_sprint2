import data_manager


def sort_by_key(key='submission_time', reverse=False, database='questions'):
    if database == 'questions':
        database = data_manager.QUESTION_FILE_PATH
    else:
        database = data_manager.ANSWER_FILE_PATH
    file = data_manager.read_from_csv(database)
    file.sort(key=lambda row: row[key], reverse=True)
    return file


def create_header(input):
    header = []
    if type(input) == list:  # This section handles the answers
        for details in input:
            for key in details:
                formatted_header = key.replace("_", " ").capitalize()
                if formatted_header not in header:
                    header.append(formatted_header)
    elif type(input) == dict:  # This section handles the questions
        for details in input:
            formatted_header = details.replace("_", " ").capitalize()
            if formatted_header not in header:
                header.append(formatted_header)
    return header
