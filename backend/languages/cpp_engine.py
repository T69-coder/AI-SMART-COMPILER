import subprocess
import os
import tempfile


def run_cpp(code):
    try:
        # Har request ke liye alag temporary folder banate hain
        # taaki 2 users ek saath run karein to files overwrite na hon
        with tempfile.TemporaryDirectory() as tmp_dir:

            source_path = os.path.join(tmp_dir, "temp.cpp")
            executable_path = os.path.join(tmp_dir, "temp.out")

            with open(source_path, "w") as file:
                file.write(code)

            compile_process = subprocess.run(
                ["g++", source_path, "-o", executable_path],
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

            run_process = subprocess.run(
                [executable_path],
                capture_output=True,
                text=True,
                timeout=5
            )

            return {
                "status": "success",
                "output": run_process.stdout if run_process.stdout else run_process.stderr
            }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "details": {
                "type": "Runtime Error",
                "message": "C++ execution timeout."
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