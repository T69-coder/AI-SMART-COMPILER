# executor.py

import io
import contextlib

from compiler.error_handler import handle_error


def execute(code):

    try:

        # Extra spaces remove
        code = code.strip()


        # Case 1: Simple expression
        try:

            result = eval(code)

            return {
                "status": "success",
                "output": result
            }


        except SyntaxError:

            # Case 2: Multiple line code

            output_buffer = io.StringIO()


            with contextlib.redirect_stdout(output_buffer):

                exec(code)


            output = output_buffer.getvalue()


            return {
                "status": "success",
                "output": output
            }



    except Exception as error:


        return {
            "status": "error",
            "details": handle_error(error)
        }



# Testing

if __name__ == "__main__":


    code = """
x = 10
print(x)
"""


    result = execute(code)


    print(result)