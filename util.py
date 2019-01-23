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
