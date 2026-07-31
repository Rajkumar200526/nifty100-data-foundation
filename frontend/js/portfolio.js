checkAuth();

let sectorChart = null;
let scoreChart = null;

async function loadPortfolio() {

    try {

        const response = await fetch(`${window.API}/portfolio/list`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {

            showAlert("Unable to load portfolio.", "danger");
            return;

        }

        const data = await response.json();
        alert(JSON.stringify(data, null, 2));

        // =============================
        // Summary Cards
        // =============================

        document.getElementById("totalCompanies").textContent =
            data.length;

        let totalScore = 0;
        const sectors = {};

        data.forEach(company => {

            totalScore += Number(company.investment_score || 0);

            sectors[company.broad_sector] =
                (sectors[company.broad_sector] || 0) + 1;

        });

        const avgScore =
            data.length > 0
                ? (totalScore / data.length).toFixed(2)
                : 0;

        document.getElementById("avgScore").textContent =
            avgScore;

        let topSector = "-";
        let maxCount = 0;

        for (const sector in sectors) {

            if (sectors[sector] > maxCount) {

                maxCount = sectors[sector];
                topSector = sector;

            }

        }

        document.getElementById("topSector").textContent =
            topSector;

        document.getElementById("latestCompany").textContent =
            data.length
                ? data[0].company_name
                : "-";

        // =============================
        // Portfolio Table
        // =============================

        let html = "";

        data.forEach(company => {

            html += `
            <tr>

                <td>${company.company_name}</td>

                <td>${company.broad_sector}</td>

                <td>${company.added_date}</td>

                <td>

                    <a href="company.html?id=${company.company_id}"
                       class="btn btn-success btn-sm me-2">

                        View

                    </a>

                    <button
                        class="btn btn-danger btn-sm"
                        onclick="removeCompany(${company.id})">

                        Remove

                    </button>

                </td>

            </tr>
            `;

        });

        document.getElementById("portfolioTable").innerHTML =
            html;

    } catch (error) {

        console.error(error);

        showAlert("Unable to load portfolio.", "danger");

    }

}

    // =============================
    // // =============================
// Charts
// =============================

if (sectorChart) sectorChart.destroy();
if (scoreChart) scoreChart.destroy();

sectorChart = new Chart(
    document.getElementById("sectorChart"),
    {
        type: "pie",
        data: {
            labels: Object.keys(sectors),
            datasets: [{
                data: Object.values(sectors),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    }
);

scoreChart = new Chart(
    document.getElementById("scoreChart"),
    {
        type: "bar",
        data: {
            labels: data.map(c => c.company_name),
            datasets: [{
                label: "Investment Score",
                data: data.map(c => Number(c.investment_score || 0)),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    }
);


// =============================
// Remove Company
// =============================

async function removeCompany(portfolioId) {

    if (!confirm("Remove this company from your portfolio?")) {
        return;
    }

    try {

        const response = await fetch(
            `${window.API}/portfolio/${portfolioId}`,
            {
                method: "DELETE",
                headers: getAuthHeaders()
            }
        );

        const result = await response.json();

        if (response.ok) {

            showAlert(result.message || "Company removed.", "success");

            await loadPortfolio();

        } else {

            showAlert(result.detail || "Unable to remove company.", "danger");

        }

    } catch (error) {

        console.error(error);

        showAlert("Server connection failed.", "danger");

    }

}

// =============================
// Portfolio Insights
// =============================

async function loadInsights() {

    try {

        const response = await fetch(
            `${window.API}/portfolio/insights`,
            {
                headers: getAuthHeaders()
            }
        );

        if (!response.ok) {
            console.error("Unable to load portfolio insights");
            return;
        }

        const data = await response.json();

        document.getElementById("bestCompany").textContent =
            data.best_company;

        document.getElementById("bestScore").textContent =
            data.best_score;

        document.getElementById("worstCompany").textContent =
            data.worst_company;

        document.getElementById("worstScore").textContent =
            data.worst_score;

        document.getElementById("topSectorInsight").textContent =
            data.top_sector;

        document.getElementById("aiSuggestion").textContent =
            data.suggestion;

    } catch (error) {

        console.error(error);

    }

}

// =============================
// Portfolio Health
// =============================

async function loadHealth() {

    try {

        const response = await fetch(
            `${window.API}/portfolio/health`,
            {
                headers: getAuthHeaders()
            }
        );

        if (!response.ok) {
            console.error("Unable to load portfolio health");
            return;
        }

        const data = await response.json();

        document.getElementById("healthScore").textContent =
            data.health_score;

        document.getElementById("healthStatus").textContent =
            data.status;

        const badge = document.getElementById("healthStatus");

        badge.className = "badge";

        if (data.status === "Excellent") {

            badge.classList.add("bg-success");

        } else if (data.status === "Good") {

            badge.classList.add("bg-primary");

        } else if (data.status === "Average") {

            badge.classList.add("bg-warning");

        } else {

            badge.classList.add("bg-danger");

        }

    } catch (error) {

        console.error(error);

    }

}

// =============================
// Initialize
// =============================

async function initPortfolio() {

    await loadPortfolio();
    await loadHealth();
    await loadInsights();

}

initPortfolio();