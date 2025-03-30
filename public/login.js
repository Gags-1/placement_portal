document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const regNumber = document.getElementById("reg_number").value;
    const password = document.getElementById("password").value;

    const loginData = new URLSearchParams();
    loginData.append("username", regNumber);  // FastAPI OAuth2 expects "username"
    loginData.append("password", password);

    try {
        const response = await fetch("http://127.0.0.1:8000/login", {  // Replace with actual FastAPI login endpoint
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: loginData
        });

        if (!response.ok) {
            throw new Error("Invalid registration number or password");
        }

        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);  // Store JWT token for authentication
        localStorage.setItem("reg_number", regNumber);  // Store reg number for future API calls

        // Redirect to student profile page after successful login
        window.location.href = "student_feed.html";
    } catch (error) {
        document.getElementById("error-message").style.display = "block";
        document.getElementById("error-message").textContent = error.message;
    }
});
