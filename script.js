function sendChatGPTRequest() {
    var xhr = new XMLHttpRequest();
    var url = "https://api.openai.com/v1/completions";

    var base64String = "c2staUE2cG5aWE1Pc3ZxUGc0TXZZdVhUM0JsYmtGSnRrTHEzUHVGcUVvZVZlY2lLTENy";

    var decodedString = atob(base64String);

    var Authorization = "Bearer "+decodedString


// Decode Base64 string
var decodedString = atob(base64String);

    var postData = {
        prompt: "Can you check if this news is correct or if it is fake, and explain why you think so: " + document.getElementById("titleView").value,
        // prompt: "Can you check if this news is correct or if it is fake, and explain why you think so: ",
        max_tokens: 1000,
        model: "text-davinci-003",
        temperature: 0.5
    };

    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
    xhr.setRequestHeader('Authorization', Authorization);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var choices = response.choices;
            var id = response.id;

            for (var i = 0; i < choices.length; i++) {
                var choice = choices[i];
                var gptText = choice.text;

                document.getElementById("response").innerText = gptText;
                // Perform other actions with the response

                // Example: Start text-to-speech
                var speech = new SpeechSynthesisUtterance(gptText);
                speechSynthesis.speak(speech);
            }
        }
    };

    xhr.send(JSON.stringify(postData));
}

