import subprocess
import os


def run_cpp(code):
    try:
        with open("temp.cpp", "w") as file:
            file.write(code)

        compile_process = subprocess.run(
            ["g++", "temp.cpp", "-o", "temp"],
            capture_output=True,
            text=True
        )

        if compile_process.returncode != 0:
            return {
                "status": "error",
                "details": {
                    "type": "Compilation Error",
                    "message": compile_process.stderr
                }
            }

        executable = "temp.exe" if os.name == "nt" else "./temp"

        run_process = subprocess.run(
            [executable],
            capture_output=True,
            text=True
        )

        return {
            "status": "success",
            "output": run_process.stdout if run_process.stdout else run_process.stderr
        }

    except Exception as e:
        return {
            "status": "error",
            "details": {
                "type": "Runtime Error",
                "message": str(e)
            }
        }