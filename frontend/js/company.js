const API = "http://127.0.0.1:8000";


const token = localStorage.getItem("token");

// If user is not logged in
if (!token) {
    window.location.href = "login.html";
}

// Get company ID from URL
// Get company ID from URL
const params = new URLSearchParams(window.location.search);

const companyId = params.get("id");

// Set Compare button link
document.getElementById("compareLink").href =
    `compare.html?id=${companyId}`;

// Load company details
async function loadCompany() {

    const response = await fetch(`${API}/company/${companyId}`, {

        headers: {
            "Authorization": `Bearer ${token}`
        }

    });

    if (!response.ok) {

        alert("Unable to load company.");

        window.location.href = "dashboard.html";

        return;
    }

    const company = await response.json();

    document.getElementById("companyName").innerHTML =
        company.company_name;

    document.getElementById("sector").innerHTML =
        company.broad_sector;

    document.getElementById("score").innerHTML =
        company.investment_score;

    document.getElementById("recommendation").innerHTML =
        company.Recommendation;

    document.getElementById("rank").innerHTML =
        company.Rank;
        document.getElementById("ratioLink").href =
    `ratios.html?id=${companyId}`;

}

loadCompany();