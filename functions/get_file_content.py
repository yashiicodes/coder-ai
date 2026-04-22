import os
from config import FILE_MAX_CHARS
from functions.get_files_info import get_files_info
from google import genai
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file relative to the working directory, with a maximum character limit to prevent excessive output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to retrieve content from, relative to the working directory",
            ),
        },
    ),
)
def get_file_content(working_directory, file_path):
    try: 
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not os.path.isfile(target_dir):
            print(target_dir)
            return f'Error: File not found or is not a regular file: "{file_path}"'
        if not valid_target_dir:
            return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
        # Read file safely
        with open(target_dir, "r") as f:
            content = f.read(FILE_MAX_CHARS)

            # Check if file is larger
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {FILE_MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"

