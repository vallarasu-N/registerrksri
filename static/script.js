document.getElementById("registerForm").addEventListener("submit", async function(e){

    e.preventDefault();

    const data = {
        fullname: document.getElementById("fullname").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    const response = await fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    document.getElementById("message").innerHTML = result.message;

});