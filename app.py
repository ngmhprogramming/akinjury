from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "/uploads"
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png", "gif"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/chat")
def chat():
	return render_template("chat.html")

@app.route("/message", methods=["POST"])
def message():
	text = request.form["message"]
	print(text)
	return ("You sent: "+text)

@app.route("/identify", methods=["GET", "POST"])
def identify():
	upload = request.files["file"]
	return render_template("identify.html")

if __name__ == "__main__":
    app.run(debug=True)