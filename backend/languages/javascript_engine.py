import subprocess
import os
import tempfile


def run_javascript(code):

    try:

        # Har request ke liye alag temporary folder banate hain
        # taaki 2 users ek saath run karein to temp.js overwrite na ho
        with tempfile.TemporaryDirectory() as tmp_dir:

            source_path = os.path.join(tmp_dir, "temp.js")

            with open(source_path, "w") as file:
                file.write(code)

            # Run JavaScript using Node.js
            run_process = subprocess.run(
                ["node", source_path],
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