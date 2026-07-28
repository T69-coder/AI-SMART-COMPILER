from languages.python_engine import run_python
from languages.cpp_engine import run_cpp
from languages.java_engine import run_java
from languages.javascript_engine import run_javascript


def run_code(language, code):

    language = language.lower().strip()

    if language == "python":
        return run_python(code)

    elif language == "cpp":
        return run_cpp(code)

    elif language == "java":
        return run_java(code)

    elif language == "javascript":
        return run_javascript(code)

    else:
        return {
            "status": "error",
            "message": f"Unsupported language: {language}"
        }