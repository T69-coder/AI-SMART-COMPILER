# error_ai.py

# AI Error Analysis and Fix Suggestion System


def analyze_error(error_details, code):

    error_type = error_details.get("type", "")
    error_message = error_details.get("message", "")


    # Syntax Error

    if "Syntax" in error_type:

        return {

            "problem": "Your code syntax is incorrect.",

            "reason": "The compiler found a structural mistake in your code.",

            "fix": "Check brackets, symbols, keywords and code structure."

        }


    # Compilation Error (C++, Java)

    elif "Compilation" in error_type:

        return {

            "problem": "Your program could not be compiled.",

            "reason": error_message,

            "fix": "Check syntax rules, missing headers, class names and statements."

        }


    # Runtime Error

    elif "Runtime" in error_type:

        return {

            "problem": "Your program crashed while executing.",

            "reason": error_message,

            "fix": "Check input values, logic errors and possible runtime exceptions."

        }


    # Name Error

    elif "NameError" in error_message or "Name Error" in error_type:

        return {

            "problem": "Undefined variable detected.",

            "reason": "You are using a variable that has not been created.",

            "fix": "Declare the variable before using it."

        }


    # Indentation Error

    elif "IndentationError" in error_message:

        return {

            "problem": "Incorrect indentation detected.",

            "reason": "Python requires proper spacing for code blocks.",

            "fix": "Align your code blocks correctly."

        }


    # Zero Division Error

    elif "ZeroDivisionError" in error_message:

        return {

            "problem": "Division by zero error.",

            "reason": "A number is being divided by zero which is not allowed.",

            "fix": "Check the denominator value before division."

        }


    # Unknown Error

    else:

        return {

            "problem": "Unknown error detected.",

            "reason": error_message if error_message else str(error_details),

            "fix": "Review your code and check the error message."

        }