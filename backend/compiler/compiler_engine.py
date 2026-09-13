from compiler.lexer import tokenize
from compiler.parser import parse
from compiler.semantic import analyze
from compiler.engine_selector import run_code

from ai_engine.suggestion import generate_suggestion
from ai_engine.explanation import explain_code
from ai_engine.error_ai import analyze_error
from ai_engine.llm_client import get_ai_review


def compile_code(code, language):

    try:

        # Step 1 : Lexer
        tokens = tokenize(code)

        # Step 2 : Parser
        syntax_result = parse(tokens)

        # Syntax Error Check
        if "Syntax Error" in str(syntax_result):

            error_details = {
                "type": "Syntax Error",
                "message": syntax_result
            }

            # Real AI (Groq) try karo, fail ho to rule-based fallback
            ai_result = get_ai_review(code, language, error_details)

            return {
                "status": "error",
                "tokens": tokens,
                "syntax": syntax_result,
                "semantic": None,
                "output": None,
                "ai_suggestions": ai_result["suggestions"] if ai_result else [],
                "ai_explanation": ai_result["explanation"] if ai_result else [],
                "ai_error_fix": ai_result["error_fix"] if ai_result else analyze_error(
                    error_details,
                    code
                )
            }

        # Step 3 : Semantic Analysis
        semantic_result = analyze(tokens)

        # Step 4 : Execute Code
        output = run_code(language, code)

        # Step 5 : Runtime error hua kya? AI ko batane ke liye details nikaalo
        error_details = None

        if isinstance(output, dict) and output.get("status") == "error":
            error_details = output.get("details", {})

        # Step 6 : AI Review — ek hi Groq call mein explanation + suggestions +
        # error_fix teeno mil jaate hain (fast aur efficient).
        # Fail hone par purana rule-based system fallback ke roop mein chalta hai.
        ai_result = get_ai_review(code, language, error_details)

        if ai_result:

            suggestions = ai_result["suggestions"]
            explanation = ai_result["explanation"]
            error_fix = ai_result["error_fix"]

        else:

            suggestions = generate_suggestion(code)
            explanation = explain_code(code)
            error_fix = analyze_error(error_details, code) if error_details else None

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