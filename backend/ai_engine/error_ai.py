# error_ai.py
# AI Error Analysis and Fix Suggestion System

ERROR_PATTERNS = [
    # (keyword, problem, reason_template, fix)
    # Specific errors pehle check hote hain, generic (runtime/compilation)
    # sabse aakhir mein — taaki specific match kabhi generic ke peeche na chhupe.

    ("zerodivisionerror", "Division by zero error.",
     "A number is being divided by zero, which is not allowed.",
     "Check the denominator value before division."),

    ("indentationerror", "Incorrect indentation detected.",
     "Python requires consistent spacing for code blocks.",
     "Align your code blocks correctly (use spaces or tabs consistently, not both)."),

    ("nameerror", "Undefined variable detected.",
     "You are using a variable or function that has not been defined.",
     "Declare the variable before using it, or check for typos."),

    ("indexerror", "List/sequence index out of range.",
     "You tried to access an index that doesn't exist in the sequence.",
     "Check the length of the list before indexing into it."),

    ("keyerror", "Dictionary key not found.",
     "You tried to access a key that doesn't exist in the dictionary.",
     "Use .get() or check `if key in dict` before accessing it."),

    ("typeerror", "Type mismatch detected.",
     "An operation was applied to an incompatible data type.",
     "Check the types of the variables involved in the operation."),

    ("attributeerror", "Invalid attribute/method access.",
     "You tried to use a method or attribute that doesn't exist on this object.",
     "Check the object's type and available attributes/methods."),

    ("valueerror", "Invalid value provided.",
     "A function received an argument of the right type but an inappropriate value.",
     "Validate input values before passing them to the function."),

    ("syntax", "Your code syntax is incorrect.",
     "The compiler/interpreter found a structural mistake in your code.",
     "Check brackets, symbols, keywords, and code structure."),

    ("compilation", "Your program could not be compiled.",
     None,  # None matlab: reason mein raw error_message use hoga
     "Check syntax rules, missing headers, class names, and statements."),

    ("runtime", "Your program crashed while executing.",
     None,
     "Check input values, logic errors, and possible runtime exceptions."),
]


def analyze_error(error_details, code):

    error_type = (error_details.get("type") or "").lower()
    error_message = (error_details.get("message") or "").lower()

    # type aur message dono ko ek saath check karte hain, case-insensitive
    combined = f"{error_type} {error_message}"

    for keyword, problem, reason_template, fix in ERROR_PATTERNS:

        if keyword in combined:

            reason = reason_template if reason_template else (
                error_details.get("message")
                or error_details.get("type")
                or "No details provided."
            )

            return {
                "problem": problem,
                "reason": reason,
                "fix": fix
            }

    # Unknown Error
    return {
        "problem": "Unknown error detected.",
        "reason": error_details.get("message") or str(error_details),
        "fix": "Review your code and check the error message."
    }