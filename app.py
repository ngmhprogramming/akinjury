from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from os import urandom
from binascii import b2a_hex

app = Flask(__name__)
app.secret_key = "chennuodeceoofsex"

UPLOAD_FOLDER = "/uploads"
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png", "gif"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_session_id():
    if "id" in session: return session["id"]
    return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
	if request.method == "GET":
		session_id = get_session_id()
		if session_id is None: session["id"] = b2a_hex(urandom(64))
		session_id = get_session_id()
		print(session_id)
		return render_template("chat.html")
	else:
		session_id = get_session_id()
		if session_id is not None:
			session.pop("id", None)
		return redirect(url_for("index"))

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