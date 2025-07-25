from flask import Flask, render_template, request
import PyPDF2
import docx

app = Flask(__name__,template_folder="client")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.filename.endswith(".docx"):
            text = extract_text_from_docx(uploaded_file)
    return render_template("index.html", text=text)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
