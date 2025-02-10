import io
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from fpdf import FPDF
import docx

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "CV Formatting Tool is Running!", 200

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Read file in memory
    file_stream = io.BytesIO(file.read())

    # Process the CV
    try:
        processed_pdf = process_cv(file_stream)
        return jsonify({"message": "File processed successfully!", "pdf_content": processed_pdf.decode("latin1")}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_cv(file_stream):
    # Read Word file in memory
    doc = docx.Document(file_stream)
    formatted_text = "\n".join([para.text for para in doc.paragraphs])

    # Create PDF in memory
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, formatted_text)

    # Save PDF to memory
    pdf_stream = io.BytesIO()
    pdf.output(pdf_stream)
    pdf_stream.seek(0)

    return pdf_stream.getvalue()

if __name__ == "__main__":
    app.run(debug=True)
