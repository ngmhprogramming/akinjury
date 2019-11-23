function send(message){
	//var message = document.getElementById("message").value;
	//document.getElementById("message").value = "";
	
	var user_div = document.createElement("div");
	user_div.className = "message user";
	var user = document.createElement("p");
	user.innerHTML = message;
	user_div.appendChild(user);
	document.getElementById("messages").appendChild(user_div);

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			var response = JSON.parse(this.responseText);
			for (const response_message of response["messages"]){
				var bot_div = document.createElement("div");
				bot_div.className = "message bot";
				var bot = document.createElement("p");
				bot.innerHTML = response_message;
				bot_div.appendChild(bot);
				document.getElementById("messages").appendChild(bot_div);

				var speech = new SpeechSynthesisUtterance(response_message);
				window.speechSynthesis.speak(speech);
			}
			var choice_div = document.getElementById("choices");
			choice_div.innerHTML = "";
			for (const choice of response["choices"]){
				var choice_button = document.createElement("button");
				choice_button.onclick = function (){ send(choice); };
				choice_button.innerHTML = choice;
				choice_div.appendChild(choice_button);
			}
		}
	}
	xhttp.open("POST", "/message", true);
	xhttp.setRequestHeader("Content-type", "text/plain");
	xhttp.send(message);
	setTimeout(function(){
		$("#messages").animate({scrollTop: document.getElementById("messages").scrollHeight},"slow");
	}, 500);
}