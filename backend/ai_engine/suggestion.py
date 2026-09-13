# suggestion.py

# AI Code Improvement Suggestion System

import re


def _has_word(word, code):
    # "for" ko sirf poore word ke roop mein match karta hai,
    # "before", "format" jaise words ke andar chhupe "for" ko nahi
    return re.search(rf"\b{re.escape(word)}\b", code) is not None


def generate_suggestion(code):

    suggestions = []

    # Loop detection

    if _has_word("for", code) or _has_word("while", code):

        suggestions.append(
            "Loop detected. Check if optimization is possible."
        )

    # Long code detection

    if len(code) > 200:

        suggestions.append(
            "Code length is large. Try breaking it into functions."
        )

    # Print statement detection

    if _has_word("print", code):

        suggestions.append(
            "Consider using proper output handling for production code."
        )

    if len(suggestions) == 0:

        suggestions.append(
            "Code looks good. No major suggestions."
        )

    return suggestions


# Testing

if __name__ == "__main__":

    code = """
    for i in range(100):
        print(i)
    """

    result = generate_suggestion(code)

    print(result)

    # False-positive check
    code2 = "before = 10"
    print(generate_suggestion(code2))  # ab "Loop detected" nahi aayega