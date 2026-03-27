async function checkURL() {
    const url = document.getElementById("urlInput").value;

    const response = await fetch("http://localhost:8080/api/check", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    });

    const data = await response.json();

    document.getElementById("result").innerHTML =
        "Processed URL: " + data.processedUrl + "<br>" +
        "Prediction: " + data.prediction;
}