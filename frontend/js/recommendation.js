const API = "http://127.0.0.1:8000";

const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "login.html";
}

const params = new URLSearchParams(window.location.search);
const companyId = params.get("id");

if (!companyId) {
    alert("Company ID not found");
    window.location.href = "dashboard.html";
}

async function loadRecommendation() {

    const response = await fetch(
        `${API}/recommendation/${companyId}`,
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        alert("Unable to load recommendation.");
        return;
    }

    const data = await response.json();

    document.getElementById("companyName").innerHTML =
        data.company_name;

    document.getElementById("score").innerHTML =
        data.score + " / 4";

    document.getElementById("roe").innerHTML =
        data.roe + "%";

    document.getElementById("roce").innerHTML =
        data.roce + "%";

    document.getElementById("debt").innerHTML =
        data.debt_to_equity;

    document.getElementById("fcf").innerHTML =
        data.free_cash_flow;
        const percentage = (data.score / 4) * 100;

const scoreBar = document.getElementById("scoreBar");

scoreBar.style.width = percentage + "%";
scoreBar.innerHTML = percentage + "%";
if (percentage === 100) {

    scoreBar.classList.add("bg-success");

}
else if (percentage >= 50) {

    scoreBar.classList.add("bg-warning");

}
else {

    scoreBar.classList.add("bg-danger");

}

   const badge = document.getElementById("recommendationBadge");
const recommendationText = document.getElementById("recommendationText");

badge.innerHTML = data.recommendation;

if (data.recommendation === "BUY") {

    badge.className = "badge bg-success";

    recommendationText.innerHTML =
        "This company has excellent profitability, low debt, and positive free cash flow. Based on the available financial indicators, it appears to be a strong investment candidate.";

}
else if (data.recommendation === "HOLD") {

    badge.className = "badge bg-warning text-dark";

    recommendationText.innerHTML =
        "The company has moderate financial performance. Consider monitoring future results before making an investment decision.";

}
else {

    badge.className = "badge bg-danger";

    recommendationText.innerHTML =
        "The company currently has weaker financial indicators. Review its financial statements carefully before investing.";

}
new Chart(document.getElementById("financialChart"), {

    type: "radar",

    data: {

        labels: [

            "ROE",

            "ROCE",

            "Debt/Equity",

            "Free Cash Flow"

        ],

        datasets: [{

            label: data.company_name,

            data: [

                data.roe,

                data.roce,

                data.debt_to_equity,

                data.free_cash_flow

            ]

        }]

    },

    options: {

        responsive: true,

        scales: {

            r: {

                beginAtZero: true

            }

        }

    }

});
}

loadRecommendation();