from flask import Flask, request, jsonify
import subprocess
from jsonschema import validate, ValidationError
import json
import os

app = Flask(__name__)

# Define the schema globally
schema = {
    "type": "object",
    "properties": {
        "students": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "student_id": {"type": "number"},
                    "student_progress": {"type": "number"},
                    "selections": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 1,
                        "maxItems": 20
                    }
                },
                "required": ["student_id", "student_progress", "selections"]
            }
        },
        "executable_name": {"type": "string"}
    },
    "required": ["students"]
}

def validate_json(data):
    try:
        validate(instance=data, schema=schema)
        selection_lengths = [len(student['selections']) for student in data['students']]
        if len(set(selection_lengths)) > 1:
            return False, "All students must have selections of the same length"
        return True, None
    except ValidationError as e:
        return False, str(e)

def execute_script(executable_name, students_json):
    if executable_name != os.path.basename(executable_name):
        return False, "Executable name must be a file name without any path"

    try:
        result = subprocess.check_output(
            ['python3', executable_name, students_json],
            stderr=subprocess.STDOUT
        )
        return True, result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json

    is_valid, message = validate_json(data)
    if not is_valid:
        return jsonify({"error": "Invalid input", "message": message}), 400

    students = data.get('students')
    executable_name = data.get('executable_name')

    students_json = json.dumps(students)

    success, output = execute_script(executable_name, students_json)
    if success:
        return jsonify({"status": "success", "output": output})
    else:
        return jsonify({"error": output}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
