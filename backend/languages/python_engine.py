import subprocess
import sys
import os
import tempfile


def run_python(code):

    try:

        # Har request ke liye alag temporary folder banate hain
        # taaki 2 users ek saath run karein to files overwrite na hon
        with tempfile.TemporaryDirectory() as tmp_dir:

            source_path = os.path.join(tmp_dir, "temp_script.py")

            with open(source_path, "w") as file:
                file.write(code)

            # Code ko ALAG process mein chalate hain (seedha exec() nahi)
            # Isse: (1) infinite loop poore server ko hang nahi karega,
            # (2) crash sirf us chhote process tak seemit rahega,
            # (3) timeout laga sakte hain jo pehle bilkul nahi tha
            run_process = subprocess.run(
                [sys.executable, source_path],
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
                "message": "Python execution timeout."
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