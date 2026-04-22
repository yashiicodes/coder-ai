import os
import subprocess
from google import genai
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        # Resolve absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(
            os.path.join(working_directory, file_path)
        )

        # Security check: ensure file is inside working directory
        if not abs_file_path.startswith(abs_working_dir):
            return (
                f'Error: Cannot execute "{file_path}" '
                f'as it is outside the permitted working directory'
            )

        # Check file exists and is regular file
        if not os.path.isfile(abs_file_path):
            return (
                f'Error: "{file_path}" does not exist '
                f'or is not a regular file'
            )

        # Check Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", abs_file_path]

        if args:
            command.extend(args)

        # Run subprocess
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []

        # Non-zero exit code
        if result.returncode != 0:
            output_parts.append(
                f"Process exited with code {result.returncode}"
            )

        # Stdout
        if result.stdout.strip():
            output_parts.append(f"STDOUT:\n{result.stdout}")

        # Stderr
        if result.stderr.strip():
            output_parts.append(f"STDERR:\n{result.stderr}")

        # No output
        if not output_parts:
            return "No output produced"

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"