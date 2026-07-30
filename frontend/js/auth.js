

// If already logged in, go directly to dashboard
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");

    if (token && window.location.pathname.includes("login.html")) {
        window.location.href = "dashboard.html";
    }
});

// ---------------- LOGIN ----------------

async function login() {

    const email = document.getElementById("email").value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

if (!emailPattern.test(email)) {
    showAlert("Please enter a valid email address.", "warning");
    return;
}
    const password = document.getElementById("password").value.trim();
    if (password.length < 6) {
    showAlert("Password must be at least 6 characters.", "warning");
    return;
}

    if (!email || !password) {
        showAlert("Please enter Email and Password.", "warning");
        return;
    }

    showLoader();

const loginButton = document.querySelector("button[onclick='login()']");
if (loginButton) {
    loginButton.disabled = true;
}

    try {

        const response = await fetch(`${API}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {

            localStorage.setItem("token", data.access_token);

            localStorage.setItem("user", JSON.stringify(data.user));

            showAlert("Login Successful!", "success");

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1000);

        } else {

            showAlert(data.detail || "Invalid Email or Password", "danger");

        }

    } catch (error) {

        console.error(error);

        showAlert("Unable to connect to the server.", "danger");

    } finally {

        hideLoader();
        if (loginButton) {
    loginButton.disabled = false;
}

    }
}

// ---------------- SIGNUP ----------------

async function signup() {

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

if (!emailPattern.test(email)) {
    showAlert("Please enter a valid email address.", "warning");
    return;
}
    const password = document.getElementById("password").value.trim();

    if (!name || !email || !password) {
        showAlert("Please fill all fields.", "warning");
        return;
    }
    const terms = document.getElementById("terms");

if (terms && !terms.checked) {
    showAlert("Please accept the Terms & Conditions.", "warning");
    return;
}

  showLoader();

const signupButton = document.querySelector("button[onclick='signup()']");
if (signupButton) {
    signupButton.disabled = true;
}

    try {

        const response = await fetch(`${API}/auth/signup`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name,
                email,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {

            showAlert("Signup Successful!", "success");

            setTimeout(() => {
                window.location.href = "login.html";
            }, 1000);

        } else {

            showAlert(data.detail || "Signup Failed", "danger");

        }

    } catch (error) {

        console.error(error);

        showAlert("Unable to connect to the server.", "danger");

    } finally {

        hideLoader();
        if (signupButton) {
    signupButton.disabled = false;
}

    }
}

// ---------------- LOGOUT ----------------

function logout() {

    localStorage.removeItem("token");
    localStorage.removeItem("user");

    window.location.href = "login.html";
}

// ---------------- SHOW / HIDE PASSWORD ----------------

function togglePassword() {

    const password = document.getElementById("password");
    const eye = document.getElementById("eyeIcon");

    if (!password || !eye) return;

    if (password.type === "password") {

        password.type = "text";
        eye.className = "bi bi-eye-slash";

    } else {

        password.type = "password";
        eye.className = "bi bi-eye";

    }
}
// ===============================
// Authentication Helper Functions
// ===============================

function getToken() {
    return localStorage.getItem("token");
}

function checkAuth() {
    const token = getToken();

    if (!token) {
        window.location.href = "login.html";
    }
}

function getAuthHeaders() {
    return {
        "Authorization": `Bearer ${getToken()}`
    };
}