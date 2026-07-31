checkAuth();

const token = getToken();

// Store company data
let companyData = [];

// ---------------------
// Load Dashboard Cards
// ---------------------
async function loadDashboard() {

    try {

        const response = await fetch(`${window.API}/dashboard`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {

            showAlert("Session Expired", "danger");

            localStorage.clear();

            window.location.href = "login.html";

            return;

        }

        const data = await response.json();

        document.getElementById("totalCompanies").textContent =
            data.total_companies ?? 0;

        document.getElementById("totalClusters").textContent =
            data.total_clusters ?? 0;

        document.getElementById("averageROE").textContent =
            data.average_roe ?? 0;

    } catch (error) {

        console.error(error);

        showAlert("Unable to load dashboard.", "danger");

    }

}

// ---------------------
// Load Companies
// ---------------------
async function loadCompanies() {

    try {

        const response = await fetch(`${window.API}/company-scores`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {

            showAlert("Session Expired", "danger");

            localStorage.clear();

            window.location.href = "login.html";

            return;

        }

        companyData = await response.json();

        displayCompanies(companyData);

        drawScoreChart(companyData);

        drawSectorChart(companyData);

    } catch (error) {

        console.error(error);

        showAlert("Unable to load companies.", "danger");

    }

}

// ---------------------
// Display Table
// ---------------------
function displayCompanies(data) {

    let html = "";

    data.forEach(company => {

        html += `
        <tr>

            <td>${company.rank ?? "-"}</td>

            <td>
                <a href="company.html?id=${company.company_id}"
                class="text-decoration-none fw-bold">
                    ${company.company_name}
                </a>
            </td>

            <td>${company.broad_sector}</td>

            <td>${Number(company.investment_score ?? 0).toFixed(2)}</td>

        </tr>
        `;

    });

    document.getElementById("companyTable").innerHTML = html;

}

// ---------------------
// Search
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

// ---------------------
// Score Chart
// ---------------------
function drawScoreChart(data) {

    const labels = data.map(c => c.company_name);

    const scores = data.map(c => c.investment_score);

    new Chart(document.getElementById("scoreChart"), {

        type: "bar",

        data: {

            labels,

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

// ---------------------
// Sector Chart
// ---------------------
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
// Portfolio Summary
// ---------------------
async function loadPortfolioSummary() {

    try {

        const listResponse = await fetch(
            `${window.API}/portfolio/list`,
            {
                headers: getAuthHeaders()
            }
        );

        if (!listResponse.ok) return;

        const portfolio = await listResponse.json();

        document.getElementById("portfolioCompanies").textContent =
            portfolio.length;

        let totalScore = 0;

        const sectors = {};

        portfolio.forEach(company => {

            totalScore += Number(company.investment_score ?? 0);

            sectors[company.broad_sector] =
                (sectors[company.broad_sector] || 0) + 1;

        });

        document.getElementById("portfolioAverage").textContent =
            portfolio.length
                ? (totalScore / portfolio.length).toFixed(2)
                : "0";

        let topSector = "-";
        let max = 0;

        for (const sector in sectors) {

            if (sectors[sector] > max) {

                max = sectors[sector];
                topSector = sector;

            }

        }

        document.getElementById("portfolioSector").textContent =
            topSector;

        const healthResponse = await fetch(
            `${window.API}/portfolio/health`,
            {
                headers: getAuthHeaders()
            }
        );

        if (healthResponse.ok) {

            const health = await healthResponse.json();

            document.getElementById("portfolioHealth").textContent =
                health.status;

        }

        const insightResponse = await fetch(
            `${window.API}/portfolio/insights`,
            {
                headers: getAuthHeaders()
            }
        );

        if (insightResponse.ok) {

            const insight = await insightResponse.json();

            document.getElementById("bestCompany").textContent =
                insight.best_company;

            document.getElementById("worstCompany").textContent =
                insight.worst_company;

            document.getElementById("dashboardSuggestion").textContent =
                insight.suggestion;

        }

    } catch (error) {

        console.error(error);

    }

}

// ---------------------
// Initialize
// ---------------------

loadDashboard();
loadCompanies();
loadPortfolioSummary();