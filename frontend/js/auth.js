const API = "http://127.0.0.1:8000";

async function login() {

    const email = document.getElementById("email").value;

    const password = document.getElementById("password").value;

    const response = await fetch(
        `${API}/auth/login`,
        {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email,

                password

            })

        }
    );

    const data = await response.json();

    if (response.ok) {

        localStorage.setItem(
            "token",
            data.access_token
        );

        localStorage.setItem(
            "user",
            JSON.stringify(data.user)
        );

        alert("Login Successful");

        window.location.href = "dashboard.html";

    } else {

        alert(data.detail);

    }

}
async function signup() {

    const name = document.getElementById("name").value;

    const email = document.getElementById("email").value;

    const password = document.getElementById("password").value;

    const response = await fetch(
        `${API}/auth/signup`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name,
                email,
                password
            })
        }
    );

    const data = await response.json();

    if (response.ok) {

        alert("Signup Successful!");

        window.location.href = "login.html";

    } else {

        alert(data.detail);

    }

}