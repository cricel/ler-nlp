from flask import Flask, jsonify, request, make_response
from syllabus_processor import SyllabusProcessor
import io
import pandas as pd

syllabus_processor = SyllabusProcessor()
app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return "<h1>Welcome to the Flask App!</h1>"

# Route to handle form submission
@app.route('/get_transcript_skills', methods=['POST'])
def get_transcript_skills():
    data = request.get_json()

    name = data.get('name')
    
    df = syllabus_processor.summarize_pdf_to_csv("test_1.pdf")

    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)  # Reset the pointer to the start of the stream

    # Create a response with the CSV data
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
