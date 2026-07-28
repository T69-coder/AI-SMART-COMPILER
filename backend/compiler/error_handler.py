# error_handler.py


def handle_error(error):


    error_type = type(error).__name__

    message = str(error)



    if error_type == "SyntaxError":

        return {
            "type": "Syntax Error",
            "message": "Code structure is incorrect.",
            "suggestion": "Check brackets, symbols and indentation."
        }



    elif error_type == "NameError":

        return {
            "type": "Name Error",
            "message": "Variable is not defined.",
            "suggestion": "Check variable name spelling."
        }



    elif error_type == "TypeError":

        return {
            "type": "Type Error",
            "message": "Wrong data type operation.",
            "suggestion": "Check values and their data types."
        }



    else:

        return {
            "type": error_type,
            "message": message,
            "suggestion": "Review your code logic."
        }