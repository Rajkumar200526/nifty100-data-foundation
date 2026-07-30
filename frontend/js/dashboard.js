

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
    async function loadPortfolioSummary() {

    // -----------------------------
    // Portfolio List
    // -----------------------------
    const listResponse = await fetch(
        `${API}/portfolio/list`,
        {
            headers: getAuthHeaders()
        }
    );

    if (!listResponse.ok) {
        console.error("Unable to load portfolio");
        return;
    }

    const portfolio = await listResponse.json();

    document.getElementById("portfolioCompanies").textContent =
        portfolio.length;

    let totalScore = 0;
    const sectors = {};

    portfolio.forEach(company => {

        totalScore += Number(company.investment_score);

        sectors[company.broad_sector] =
            (sectors[company.broad_sector] || 0) + 1;

    });

    const average =
        portfolio.length
            ? (totalScore / portfolio.length).toFixed(2)
            : 0;

    document.getElementById("portfolioAverage").textContent =
        average;

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

    // -----------------------------
    // Portfolio Health
    // -----------------------------
    const healthResponse = await fetch(
        `${API}/portfolio/health`,
        {
            headers: getAuthHeaders()
        }
    );

    if (healthResponse.ok) {

        const health = await healthResponse.json();

        document.getElementById("portfolioHealth").textContent =
            health.status;

    }

    // -----------------------------
    // AI Insights
    // -----------------------------
    const insightResponse = await fetch(
        `${API}/portfolio/insights`,
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

}

    // ---------------------
    // Load Everything
    // ---------------------
    loadDashboard();
loadCompanies();
loadPortfolioSummary();