function send(){
	var message = document.getElementById("message").value;
	document.getElementById("message").value = "";

	var user = document.createElement("p");
	user.className = "message user";
	user.innerHTML = message;
	document.getElementById("messages").appendChild(user);

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			var response = this.responseText;
			var bot = document.createElement("p");
			bot.className = "message bot";
			bot.innerHTML = response;
			document.getElementById("messages").appendChild(bot);
		}
	}
	xhttp.open("POST", "/message", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send("message="+message);
}