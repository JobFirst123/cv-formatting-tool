from flask import Flask, request, render_template, send_file
import os
import tempfile
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = tempfile.gettempdir()
PROCESSED_FOLDER = tempfile.gettempdir()
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file and file.filename.endswith(".pdf"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            processed_filepath = process_pdf(filepath)
            return send_file(processed_filepath, as_attachment=True, download_name="formatted.pdf")
        else:
            return "Please upload a PDF file."
    
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Upload PDF</title>
    </head>
    <body>
        <h1>Upload a PDF to Format</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="application/pdf">
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    '''

def process_pdf(filepath):
    output_filepath = os.path.join(app.config["PROCESSED_FOLDER"], "formatted.pdf")
    
    with open(filepath, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        writer = PyPDF2.PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)

        with open(output_filepath, "wb") as output_pdf:
            writer.write(output_pdf)
    
    return output_filepath

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
