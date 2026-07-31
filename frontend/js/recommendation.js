checkAuth();

const params = new URLSearchParams(window.location.search);
const companyId = params.get("id");

if (!companyId) {

    showAlert("Company ID not found.", "warning");

    setTimeout(() => {
        window.location.href = "dashboard.html";
    }, 1500);

    throw new Error("Missing company id");

}

let financialChart = null;

async function loadRecommendation() {

    showLoader();

    try {

        const response = await fetch(
            `${window.API}/recommendation/${companyId}`,
            {
                headers: getAuthHeaders()
            }
        );

        if (!response.ok) {

            showAlert("Unable to load recommendation.", "danger");
            return;

        }

        const data = await response.json();
        alert(JSON.stringify(data, null, 2));

        document.getElementById("companyName").textContent =
            data.company_name;

        document.getElementById("score").textContent =
            `${data.score} / 4`;

        document.getElementById("roe").textContent =
            `${Number(data.roe ?? 0).toFixed(2)}%`;

        document.getElementById("roce").textContent =
            `${Number(data.roce ?? 0).toFixed(2)}%`;

        document.getElementById("debt").textContent =
            Number(data.debt_to_equity ?? 0).toFixed(2);

        document.getElementById("fcf").textContent =
            Number(data.free_cash_flow ?? 0).toLocaleString();

        // =============================
        // Score Progress Bar
        // =============================

        const percentage = (data.score / 4) * 100;

        const scoreBar = document.getElementById("scoreBar");

        scoreBar.style.width = percentage + "%";
        scoreBar.textContent = percentage + "%";

        scoreBar.className = "progress-bar";

        if (percentage === 100) {

            scoreBar.classList.add("bg-success");

        } else if (percentage >= 50) {

            scoreBar.classList.add("bg-warning");

        } else {

            scoreBar.classList.add("bg-danger");

        }

        // =============================
        // Recommendation Badge
        // =============================

        const badge = document.getElementById("recommendationBadge");
        const recommendationText =
            document.getElementById("recommendationText");

        badge.textContent = data.recommendation;

        if (data.recommendation === "BUY") {

            badge.className = "badge bg-success";

            recommendationText.textContent =
                "This company has excellent profitability, low debt, and positive free cash flow. Based on the available financial indicators, it appears to be a strong investment candidate.";

        } else if (data.recommendation === "HOLD") {

            badge.className = "badge bg-warning text-dark";

            recommendationText.textContent =
                "The company has moderate financial performance. Consider monitoring future results before making an investment decision.";

        } else {

            badge.className = "badge bg-danger";

            recommendationText.textContent =
                "The company currently has weaker financial indicators. Review its financial statements carefully before investing.";

        }

        // =============================
        // Radar Chart
        // =============================

        if (financialChart) {
            financialChart.destroy();
        }

        financialChart = new Chart(
            document.getElementById("financialChart"),
            {

                type: "radar",

                data: {

                    labels: [
                        "ROE",
                        "ROCE",
                        "Debt / Equity",
                        "Free Cash Flow"
                    ],

                    datasets: [

                        {
                            label: data.company_name,

                            data: [
                                data.roe ?? 0,
                                data.roce ?? 0,
                                data.debt_to_equity ?? 0,
                                data.free_cash_flow ?? 0
                            ]

                        }

                    ]

                },

                options: {

                    responsive: true,

                    scales: {

                        r: {

                            beginAtZero: true

                        }

                    }

                }

            }
        );

    } catch (error) {

        console.error(error);

        showAlert("Server connection failed.", "danger");

    } finally {

        hideLoader();

    }

}

loadRecommendation();