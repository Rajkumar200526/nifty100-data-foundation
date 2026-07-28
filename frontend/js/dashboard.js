const API = "http://127.0.0.1:8000";

const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "login.html";
}

// Store company data
let companyData = [];

// ---------------------
// Load Dashboard Cards
// ---------------------
async function loadDashboard() {

    const response = await fetch(`${API}/dashboard`, {

        headers: {
            "Authorization": `Bearer ${token}`
        }

    });

    if (!response.ok) {

        alert("Session Expired");

        localStorage.clear();

        window.location.href = "login.html";

        return;

    }

    const data = await response.json();

    document.getElementById("totalCompanies").innerHTML =
        data.total_companies;

    document.getElementById("totalClusters").innerHTML =
        data.total_clusters;

    document.getElementById("averageROE").innerHTML =
        data.average_roe;

}

// ---------------------
// Load Companies
// ---------------------
async function loadCompanies() {

    const response = await fetch(`${API}/company-scores`, {

        headers: {
            "Authorization": `Bearer ${token}`
        }

    });

    if (!response.ok) {

        alert("Session Expired");

        localStorage.clear();

        window.location.href = "login.html";

        return;

    }

    companyData = await response.json();

    displayCompanies(companyData);
    drawScoreChart(companyData);
    drawSectorChart(companyData);

}

// ---------------------
// Display Table
// ---------------------
function displayCompanies(data) {
    console.log(data);

    let html = "";

    data.forEach((company) => {

        html += `

        <tr>

            <td>${company.Rank}</td>

            <td>
    <a href="company.html?id=${company.company_id}"
       class="text-decoration-none fw-bold">
        ${company.company_name}
    </a>
</td>

            <td>${company.broad_sector}</td>

            <td>${Number(company.investment_score).toFixed(2)}</td>

        </tr>

        `;

    });

    document.getElementById("companyTable").innerHTML = html;

}

// ---------------------
// Search Company
// ---------------------
document.getElementById("searchBox").addEventListener("keyup", function () {

    const search = this.value.toLowerCase();

    const filtered = companyData.filter(company =>

        company.company_name.toLowerCase().includes(search)

    );

    displayCompanies(filtered);
    

});

// ---------------------
// Logout
// ---------------------
function logout() {

    localStorage.clear();

    window.location.href = "login.html";

}
// --------------------
// Bar Chart
// --------------------
function drawScoreChart(data) {

    const labels = data.map(c => c.company_name);

    const scores = data.map(c => c.investment_score);

    new Chart(document.getElementById("scoreChart"), {

        type: "bar",

        data: {

            labels: labels,

            datasets: [{

                label: "Investment Score",

                data: scores

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    });

}

// --------------------
// Pie Chart
// --------------------
function drawSectorChart(data) {

    const sectors = {};

    data.forEach(company => {

        sectors[company.broad_sector] =
            (sectors[company.broad_sector] || 0) + 1;

    });

    new Chart(document.getElementById("sectorChart"), {

        type: "pie",

        data: {

            labels: Object.keys(sectors),

            datasets: [{

                data: Object.values(sectors)

            }]

        }

    });

}

// ---------------------
// Load Everything
// ---------------------
loadDashboard();

loadCompanies();