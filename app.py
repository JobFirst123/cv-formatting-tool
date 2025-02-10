from flask import Flask, request, send_file, render_template
import docx
from fpdf import FPDF
import os
import tempfile

app = Flask(__name__)

# Define temporary upload folder
UPLOAD_FOLDER = tempfile.gettempdir()
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Define the processed folder
PROCESSED_FOLDER = os.path.join(UPLOAD_FOLDER, "processed")
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

class CustomPDF(FPDF):
    def header(self):
        """ Custom header with logo and company name """
        self.image("static/logo.png", 10, 8, 30)  # Adjust logo path & size
        self.set_font("Arial", "B", 14)
        self.cell(200, 10, "JobFirst AG - CV Formatting", ln=True, align="C")
        self.ln(10)

    def footer(self):
        """ Custom footer with page number """
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Page {self.page_no()} / {{nb}}", align="C")

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
            return send_file(processed_filepath, as_attachment=True)

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
    """ Process the CV and format it into a PDF with corporate design """
    doc = docx.Document(filepath)
    formatted_text = "\n".join([para.text for para in doc.paragraphs])

    pdf = CustomPDF()
    pdf.alias_nb_pages()  # Enable total page count
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, formatted_text)

    output_filepath = os.path.join(PROCESSED_FOLDER, "formatted_cv.pdf")
    pdf.output(output_filepath)

    return output_filepath

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
