import subprocess
import os
import tempfile


def run_java(code):

    try:

        # Har request ke liye alag temporary folder banate hain
        # taaki 2 users ek saath run karein to Main.java overwrite na ho
        with tempfile.TemporaryDirectory() as tmp_dir:

            source_path = os.path.join(tmp_dir, "Main.java")

            with open(source_path, "w") as file:
                file.write(code)

            # Compile Java (cwd = tmp_dir, taaki .class file bhi wahin bane)
            compile_process = subprocess.run(
                ["javac", "Main.java"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=tmp_dir
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
                timeout=5,
                cwd=tmp_dir
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