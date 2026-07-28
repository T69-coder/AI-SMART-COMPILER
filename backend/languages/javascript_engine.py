import subprocess
import os


def run_javascript(code):

    try:

        # Create JavaScript file
        with open("temp.js", "w") as file:
            file.write(code)


        # Run JavaScript using Node.js
        run_process = subprocess.run(
            ["node", "temp.js"],
            capture_output=True,
            text=True,
            timeout=5
        )


        # Runtime Error
        if run_process.returncode != 0:

            return {
                "status": "error",
                "details": {
                    "type": "Runtime Error",
                    "message": run_process.stderr
                }
            }


        # Success
        return {
            "status": "success",
            "output": run_process.stdout
        }



    except subprocess.TimeoutExpired:

        return {
            "status": "error",
            "details": {
                "type": "Runtime Error",
                "message": "JavaScript execution timeout."
            }
        }



    except Exception as e:

        return {
            "status": "error",
            "details": {
                "type": "Runtime Error",
                "message": str(e)
            }
        }



    finally:

        if os.path.exists("temp.js"):

            os.remove("temp.js")