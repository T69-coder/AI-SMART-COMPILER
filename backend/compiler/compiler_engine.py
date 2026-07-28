from compiler.lexer import tokenize
from compiler.parser import parse
from compiler.semantic import analyze
from compiler.engine_selector import run_code

from ai_engine.suggestion import generate_suggestion
from ai_engine.explanation import explain_code
from ai_engine.error_ai import analyze_error


def compile_code(code, language):

    try:

        # Step 1 : Lexer
        tokens = tokenize(code)

        # Step 2 : Parser
        syntax_result = parse(tokens)

        # Syntax Error Check
        if "Syntax Error" in str(syntax_result):

            return {
                "status": "error",
                "tokens": tokens,
                "syntax": syntax_result,
                "semantic": None,
                "output": None,
                "ai_suggestions": [],
                "ai_explanation": [],
                "ai_error_fix": analyze_error(
                    {
                        "type": "Syntax Error",
                        "message": syntax_result
                    },
                    code
                )
            }

        # Step 3 : Semantic Analysis
        semantic_result = analyze(tokens)

        # Step 4 : Execute Code
        output = run_code(language, code)

        # Step 5 : AI Suggestion
        suggestions = generate_suggestion(code)

        # Step 6 : AI Explanation
        explanation = explain_code(code)

        # Step 7 : Runtime Error Analysis
        error_fix = None

        if isinstance(output, dict):

            if output.get("status") == "error":

                error_fix = analyze_error(
                    output.get("details", {}),
                    code
                )

        return {

            "status": "success",

            "tokens": tokens,

            "syntax": syntax_result,

            "semantic": semantic_result,

            "output": output,

            "ai_suggestions": suggestions,

            "ai_explanation": explanation,

            "ai_error_fix": error_fix

        }

    except Exception as error:

        return {

            "status": "error",

            "message": str(error)

        }