from flask import Flask, request, render_template
import docx
from fpdf import FPDF
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

import tempfile
UPLOAD_FOLDER = tempfile.gettempdir()

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            processed_filepath = process_cv(filepath)
            return f"File processed successfully. <a href='/{processed_filepath}'>Download</a>"
    return '''
        <!doctype html>
        <title>Upload CV</title>
        <h1>Upload a CV to Format</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    '''

def process_cv(filepath):
    doc = docx.Document(filepath)
    formatted_text = "\n".join([para.text for para in doc.paragraphs])
    output_filepath = os.path.join(app.config["PROCESSED_FOLDER"], "formatted.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, formatted_text)
    pdf.output(output_filepath)
    return output_filepath

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
