// ----------------------
// Global API URL
// ----------------------

window.API = "https://nifty-financial-analytics-platform-ikzb.onrender.com";

// ----------------------
// Authentication
// ----------------------

function getToken() {
    return localStorage.getItem("token");
}

function getAuthHeaders() {
    return {
        Authorization: `Bearer ${getToken()}`
    };
}

function checkAuth() {
    const token = getToken();

    if (!token) {
        window.location.href = "login.html";
    }
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

// ----------------------
// Loader
// ----------------------

function showLoader() {
    const loader = document.getElementById("loader");

    if (loader) {
        loader.style.display = "flex";
    }
}

function hideLoader() {
    const loader = document.getElementById("loader");

    if (loader) {
        loader.style.display = "none";
    }
}

// ----------------------
// Alert Messages
// ----------------------

function showAlert(message, type = "success") {
    const alertBox = document.getElementById("alertBox");

    if (!alertBox) return;

    alertBox.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show">
            ${message}
            <button class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    setTimeout(() => {
        const alert = alertBox.querySelector(".alert");

        if (alert) {
            alert.classList.remove("show");

            setTimeout(() => {
                alert.remove();
            }, 300);
        }
    }, 3000);
}

// ----------------------
// Number Formatter
// ----------------------

function formatNumber(value) {
    if (value === null || value === undefined) {
        return "N/A";
    }

    return Number(value).toLocaleString("en-US");
}

// ----------------------
// Percentage Formatter
// ----------------------

function formatPercent(value) {
    if (value === null || value === undefined) {
        return "N/A";
    }

    return Number(value).toFixed(2) + "%";
}