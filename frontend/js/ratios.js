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

let ratioChart = null;

async function loadRatios() {

    showLoader();

    try {

        const response = await fetch(
            `${window.API}/company/${companyId}/ratios`,
            {
                headers: getAuthHeaders()
            }
        );

        if (!response.ok) {

            showAlert("Unable to load financial ratios.", "danger");
            return;

        }

        const data = await response.json();

        if (!Array.isArray(data) || data.length === 0) {

            showAlert("No financial ratio data found.", "warning");
            return;

        }

        const latest = data[data.length - 1];

        document.getElementById("companyName").innerText =
            `Financial Trends - ${latest.company_name}`;

        document.getElementById("roe").innerText =
            latest.roe != null
                ? latest.roe.toFixed(2) + "%"
                : "N/A";

        document.getElementById("roa").innerText =
            latest.roa != null
                ? latest.roa.toFixed(2) + "%"
                : "N/A";

        document.getElementById("debt").innerText =
            latest.debt_to_equity != null
                ? latest.debt_to_equity.toFixed(2)
                : "N/A";

        document.getElementById("currentRatio").innerText =
            latest.current_ratio != null
                ? latest.current_ratio.toFixed(2)
                : "N/A";

        document.getElementById("roce").innerText =
            latest.roce != null
                ? latest.roce.toFixed(2) + "%"
                : "N/A";

        document.getElementById("fcf").innerText =
            latest.free_cash_flow != null
                ? Number(latest.free_cash_flow).toLocaleString()
                : "N/A";

        document.getElementById("backCompany").href =
            `company.html?id=${companyId}`;

        const years = data.map(item => item.year);

        if (ratioChart) {
            ratioChart.destroy();
        }

        ratioChart = new Chart(
            document.getElementById("ratioChart"),
            {
                type: "line",

                data: {

                    labels: years,

                    datasets: [

                        {
                            label: "ROE %",
                            data: data.map(item => item.roe ?? 0),
                            borderWidth: 2,
                            fill: false
                        },

                        {
                            label: "ROCE %",
                            data: data.map(item => item.roce ?? 0),
                            borderWidth: 2,
                            fill: false
                        },

                        {
                            label: "Free Cash Flow",
                            data: data.map(item => item.free_cash_flow ?? 0),
                            borderWidth: 2,
                            fill: false
                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        legend: {
                            position: "top"
                        }

                    },

                    scales: {

                        y: {
                            beginAtZero: true
                        }

                    }

                }

            }

        );

    } catch (error) {

        console.error(error);

        showAlert("Error loading financial ratios.", "danger");

    } finally {

        hideLoader();

    }

}

loadRatios();