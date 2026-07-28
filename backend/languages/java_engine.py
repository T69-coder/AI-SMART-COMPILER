import subprocess
import os


def run_java(code):

    try:

        # Create Java file
        with open("Main.java", "w") as file:
            file.write(code)


        # Compile Java
        compile_process = subprocess.run(
            ["javac", "Main.java"],
            capture_output=True,
            text=True,
            timeout=10
        )


        if compile_process.returncode != 0:

            return {
                "status": "error",
                "details": {
                    "type": "Compilation Error",
                    "message": compile_process.stderr
                }
            }


        # Run Java
        run_process = subprocess.run(
            ["java", "Main"],
            capture_output=True,
            text=True,
            timeout=5
        )


        if run_process.returncode != 0:

            return {
                "status": "error",
                "details": {
                    "type": "Runtime Error",
                    "message": run_process.stderr
                }
            }


        return {
            "status": "success",
            "output": run_process.stdout
        }


    except subprocess.TimeoutExpired:

        return {
            "status": "error",
            "details": {
                "type": "Runtime Error",
                "message": "Program execution timeout."
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

        if os.path.exists("Main.java"):
            os.remove("Main.java")

        if os.path.exists("Main.class"):
            os.remove("Main.class")