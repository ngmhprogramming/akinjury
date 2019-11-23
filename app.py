from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from os import urandom, path
from base64 import b64encode
from pandas import read_csv

app = Flask(__name__)
app.secret_key = "chennuodeceoofsex"

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png", "gif"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

dfs = {}
idxs = {}
options = {}
items = {}
master_options = list(read_csv("chat/injurylist.csv").iloc[:,:-1])

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
		dfs[session_id] = read_csv("chat/injurylist.csv")
		idxs[session_id] = -1
		return render_template("chat.html")
	else:
		session_id = get_session_id()
		if session_id is not None:
			session.pop("id", None)
			del dfs[session_id]
			del idxs[session_id]
			del options[session_id]
			del items[session_id]
		return redirect(url_for("index"))

@app.route("/message", methods=["POST"])
def message():
	session_id = get_session_id()
	if session_id is None: return redirect(url_for("chat"))
	text = request.form["message"]
	'''
	Response Array
	{
		"messages": [],
		"choices": []
	}
	'''
	response = {}
	response["messages"] = []
	response["choices"] = []

	if idxs[session_id] > -1 and idxs[session_id] < len(master_options):
		if len(options[session_id]) > 1:
			uinput = text
			if "location" not in items[session_id]:
				dfs[session_id] = dfs[session_id].loc[dfs[session_id][items[session_id]] == uinput,:]
			else:
				if uinput != "No specific location":
					dfs[session_id] = dfs[session_id].loc[(dfs[session_id][items[session_id]] == uinput) | (dfs[session_id][items[session_id]] == 'Other area'),:]
				else:
					dfs[session_id] = dfs[session_id].loc[dfs[session_id][items[session_id]] == uinput,:]
			response["messages"].append(str(len(list(dfs[session_id]['Injury name'])))+" possible injuries")
		if len(dfs[session_id]) == 1: idxs[session_id] = len(master_options)
	idxs[session_id] += 1
	if idxs[session_id] < len(master_options):
		items[session_id] = master_options[idxs[session_id]]
		options[session_id] = list(dfs[session_id].loc[:,items[session_id]].unique())
		if len(options[session_id]) == 2: options[session_id].sort(reverse=True)	
		response["messages"].append(items[session_id])
		response["choices"] = options[session_id]
	if idxs[session_id] >= len(master_options):
		response["messages"].append("Injury found! The following injuries are possible")
		[response["messages"].append(injury) for injury in list(dfs[session_id]['Injury name'])]
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
