import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the specified file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written at the specified file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    wdir_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not file_abs_path.startswith(wdir_abs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(file_abs_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    if not os.path.exists(file_abs_path):
        try:
            os.makedirs(os.path.dirname(file_abs_path), exist_ok=True)
        except Exception as err:
            return f'Error: could not create directory {err=}'
        
    try:
        with open(file_abs_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as err:
        return f'Error: could not write to {file_abs_path}'