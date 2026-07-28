import io
import sys
import traceback


def run_python(code):

    output = io.StringIO()
    old_stdout = sys.stdout

    try:

        sys.stdout = output

        exec(code)

        return {
            "status": "success",
            "output": output.getvalue()
        }


    except Exception:

        return {
            "status": "error",
            "details": {
                "type": "Runtime Error",
                "message": traceback.format_exc()
            }
        }


    finally:

        sys.stdout = old_stdout