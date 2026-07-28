# suggestion.py

# AI Code Improvement Suggestion System


def generate_suggestion(code):


    suggestions = []


    # Loop detection

    if "for" in code:

        suggestions.append(
            "Loop detected. Check if optimization is possible."
        )


    # Long code detection

    if len(code) > 200:

        suggestions.append(
            "Code length is large. Try breaking it into functions."
        )


    # Print statement detection

    if "print" in code:

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