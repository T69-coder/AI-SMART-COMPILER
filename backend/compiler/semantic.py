# semantic.py

# Semantic Analyzer
# Code ka meaning check karta hai


def analyze(tokens):

    variables = {}


    # Simple variable assignment check

    if "=" in tokens:

        index = tokens.index("=")


        variable = tokens[0]
        value = tokens[index + 1]


        # Number check

        if value.isdigit():

            variables[variable] = "integer"


        else:

            variables[variable] = "string"


        return {
            "status": "Valid",
            "variables": variables
        }


    return {
        "status": "Unknown statement"
    }



# Testing

if __name__ == "__main__":


    tokens = ["x", "=", "10"]


    result = analyze(tokens)


    print(result)
    