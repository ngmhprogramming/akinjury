from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from os import urandom, path
from base64 import b64encode
from chatbot_search import diagnoser

app = Flask(__name__)
app.secret_key = "chennuodeceoofsex"

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png", "gif"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

diagnosers = {}

#Possibly implement chat history
histories = {}

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
		if session_id is None: session["id"] = b64encode(urandom(64)).decode('utf-8')
		session_id = get_session_id()
		diagnosers[session_id] = diagnoser()
		return render_template("chat.html")
	else:
		session_id = get_session_id()
		try:
			if session_id is not None:
				session.pop("id", None)
				del diagnosers[session_id]
		except:
			pass
		return redirect(url_for("index"))

@app.route("/message", methods=["POST"])
def message():
	session_id = get_session_id()
	if session_id is None: return redirect(url_for("chat"))
	text = request.form["message"]
	response = {}
	done = False
	if text != "Diagnose Me":
		done = not diagnosers[session_id].ans_qn(text)
	if not done:
		response["messages"], response["choices"], possible = diagnosers[session_id].ask_qn()
		if response["messages"] is False: done = True
		#response["messages"].append(["Possible Injuries:"])
		#[response["messages"].append(injury) for injury in possible]
	if done:
		possible = diagnosers[session_id].conclude_injury()
		response["messages"] = ["Possible Injuries:"]
		[response["messages"].append(injury) for injury in possible]
		response["choices"] = []
	print(response["messages"])
	print(response["choices"])
	return jsonify(response)

@app.route("/identify", methods=["GET", "POST"])
def identify():
	if request.method == "GET":
		return render_template("identify.html")
	else:
		upload = request.files["file"]
		if upload.filename != "" and upload and allowed_file(upload.filename):
			upload_name = secure_filename(upload.filename)
			upload.save(path.join(app.config['UPLOAD_FOLDER'], upload_name))
		return render_template("identify.html", upload_name="uploads/"+upload_name)

if __name__ == "__main__":
    app.run(debug=True)
