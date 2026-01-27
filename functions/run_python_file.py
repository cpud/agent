import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run specified Python file found within the current working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the specified Python file.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to pass to the Python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    wdir_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not file_abs_path.startswith(wdir_abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory"'
    if not os.path.exists(file_abs_path):
        return f'Error: File "{file_path}" does not exist.'
    if not os.path.isfile(file_abs_path):
        return f'Error: "{file_path}" does not exist or is not a regular file.'
    if not os.path.basename(file_abs_path).endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python", file_abs_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=wdir_abs_path,
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        return "\n".join(output) if output else "No output produced."
    except Exception as err:
        return f"Error: executing Python file: {err=}"