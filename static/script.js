function send(){
	var message = document.getElementById("message").value;
	document.getElementById("message").value = "";

	var user_div = document.createElement("div");
	user_div.className = "message user";
	var user = document.createElement("p");
	user.innerHTML = message;
	user_div.appendChild(user);
	document.getElementById("messages").appendChild(user_div);

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			var response = this.responseText;

			var bot_div = document.createElement("div");
			bot_div.className = "message bot";
			var bot = document.createElement("p");
			bot.innerHTML = response;
			bot_div.appendChild(bot);
			document.getElementById("messages").appendChild(bot_div);
		}
	}
	xhttp.open("POST", "/message", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send("message="+message);
}