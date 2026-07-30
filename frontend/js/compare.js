
console.log("compare.js loaded");
checkAuth();

const token = getToken();

const urlParams = new URLSearchParams(window.location.search);
const selectedCompany = urlParams.get("id");

// Load companies into dropdowns
async function loadCompanies() {

    console.log("loadCompanies() called");
    showLoader();

    try {

        const response = await fetch(`${API}/company-scores`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            showAlert("Unable to load companies.", "danger");
            return;
        }

        const companies = await response.json();
        console.log("Companies:", companies);

        const company1 = document.getElementById("company1");
        const company2 = document.getElementById("company2");

        company1.innerHTML = "";
        company2.innerHTML = "";

        companies.forEach(company => {

            const option1 = document.createElement("option");
            option1.value = company.company_id;
            option1.textContent = company.company_name;
            company1.appendChild(option1);

            const option2 = document.createElement("option");
            option2.value = company.company_id;
            option2.textContent = company.company_name;
            company2.appendChild(option2);

        });

        if (selectedCompany) {

            company1.value = selectedCompany;

            for (let i = 0; i < company2.options.length; i++) {

                if (company2.options[i].value !== selectedCompany) {

                    company2.selectedIndex = i;
                    break;

                }

            }

        } else {

            company1.selectedIndex = 0;

            if (company2.options.length > 1) {
                company2.selectedIndex = 1;
            }

        }

        compareCompanies();

    } catch (err) {

        console.error(err);

        showAlert("Error loading companies.", "danger");

    } finally {

        hideLoader();

    }

}

// Compare companies
async function compareCompanies() {

    showLoader();

    try {

        const id1 = document.getElementById("company1").value;
        const id2 = document.getElementById("company2").value;

        if (id1 === id2) {
            showAlert("Please select two different companies.", "warning");
            return;
        }

        const response = await fetch(
            `${API}/compare?company1=${id1}&company2=${id2}`,
            {
                headers: getAuthHeaders()
            }
        );

        if (!response.ok) {
            showAlert("Unable to compare companies.", "danger");
            return;
        }

        const data = await response.json();
        console.log("Compare:", data);
        console.log("Compare API Response:", data);

        if (!Array.isArray(data) || data.length < 2) {
            showAlert("Comparison data not found.", "warning");
            return;
        }

        const companyA = data[0];
        const companyB = data[1];

        document.getElementById("companyName1").innerText = companyA.company_name;
        document.getElementById("companyName2").innerText = companyB.company_name;

        const sales1 = document.getElementById("sales1");
        const sales2 = document.getElementById("sales2");

        sales1.innerText = Number(companyA.sales).toLocaleString();
        sales2.innerText = Number(companyB.sales).toLocaleString();

        const profit1 = document.getElementById("profit1");
        const profit2 = document.getElementById("profit2");

        profit1.innerText = Number(companyA.net_profit).toLocaleString();
        profit2.innerText = Number(companyB.net_profit).toLocaleString();

        const roe1 = document.getElementById("roe1");
        const roe2 = document.getElementById("roe2");

        roe1.innerText = companyA.roe != null
            ? Number(companyA.roe).toFixed(2)
            : "N/A";

        roe2.innerText = companyB.roe != null
            ? Number(companyB.roe).toFixed(2)
            : "N/A";

       const roce1 = document.getElementById("roce1");
const roce2 = document.getElementById("roce2");

roce1.innerText = companyA.roce != null
    ? Number(companyA.roce).toFixed(2)
    : "N/A";

roce2.innerText = companyB.roce != null
    ? Number(companyB.roce).toFixed(2)
    : "N/A";

        const debt1 = document.getElementById("debt1");
        const debt2 = document.getElementById("debt2");

        debt1.innerText = companyA.debt_to_equity != null
            ? Number(companyA.debt_to_equity).toFixed(2)
            : "N/A";

        debt2.innerText = companyB.debt_to_equity != null
            ? Number(companyB.debt_to_equity).toFixed(2)
            : "N/A";

        drawChart(companyA, companyB);

        showWinner(companyA, companyB);

        highlightWinner(companyA, companyB);

    } catch (error) {

        console.error(error);

        showAlert("Error comparing companies.", "danger");

    } finally {

        hideLoader();

    }

}

// ===============================
// Draw Comparison Chart
// ===============================

let chart = null;
let ratioChart = null;


function drawChart(companyA, companyB) {

    const ctx = document.getElementById("compareChart");

    if (chart) {
        chart.destroy();
    }
    if (ratioChart) {
    ratioChart.destroy();
}

    chart = new Chart(ctx, {

        type: "bar",

        data: {

            labels: [
                "Sales",
                "Net Profit",
                "Free Cash Flow"
            ],

            datasets: [

                {
                    label: companyA.company_name,
                    data: [
                        companyA.sales ?? 0,
                        companyA.net_profit ?? 0,
                        companyA.free_cash_flow ?? 0
                    ]
                },

                {
                    label: companyB.company_name,
                    data: [
                        companyB.sales ?? 0,
                        companyB.net_profit ?? 0,
                        companyB.free_cash_flow ?? 0
                    ]
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

    });
    const ratioCtx = document.getElementById("ratioChart");

ratioChart = new Chart(ratioCtx, {

    type: "bar",

    data: {

        labels: [
            "ROE",
            "ROCE",
            "Debt / Equity"
        ],

        datasets: [

            {
                label: companyA.company_name,

                data: [
                    companyA.roe ?? 0,
                    companyA.roce ?? 0,
                    companyA.debt_to_equity ?? 0
                ]
            },

            {
                label: companyB.company_name,

                data: [
                    companyB.roe ?? 0,
                    companyB.roce ?? 0,
                    companyB.debt_to_equity ?? 0
                ]
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

});
}


// ===============================
// Winner Summary
// ===============================

function showWinner(companyA, companyB) {

    let scoreA = 0;
    let scoreB = 0;

    const winnerSales = document.getElementById("winnerSales");
    const winnerProfit = document.getElementById("winnerProfit");
    const winnerROE = document.getElementById("winnerROE");
    const winnerDebt = document.getElementById("winnerDebt");
    const overallWinner = document.getElementById("overallWinner");

    // Higher Sales
    if ((companyA.sales ?? 0) > (companyB.sales ?? 0)) {
        scoreA++;
        winnerSales.innerHTML =
            `✅ Higher Sales : <b>${companyA.company_name}</b>`;
    } else {
        scoreB++;
        winnerSales.innerHTML =
            `✅ Higher Sales : <b>${companyB.company_name}</b>`;
    }

    // Higher Profit
    if ((companyA.net_profit ?? 0) > (companyB.net_profit ?? 0)) {
        scoreA++;
        winnerProfit.innerHTML =
            `✅ Higher Net Profit : <b>${companyA.company_name}</b>`;
    } else {
        scoreB++;
        winnerProfit.innerHTML =
            `✅ Higher Net Profit : <b>${companyB.company_name}</b>`;
    }

    // Better ROE
    if ((companyA.roe ?? 0) > (companyB.roe ?? 0)) {
        scoreA++;
        winnerROE.innerHTML =
            `✅ Better ROE : <b>${companyA.company_name}</b>`;
    } else {
        scoreB++;
        winnerROE.innerHTML =
            `✅ Better ROE : <b>${companyB.company_name}</b>`;
    }

    // Lower Debt
    if ((companyA.debt_to_equity ?? 9999) < (companyB.debt_to_equity ?? 9999)) {
        scoreA++;
        winnerDebt.innerHTML =
            `✅ Lower Debt : <b>${companyA.company_name}</b>`;
    } else {
        scoreB++;
        winnerDebt.innerHTML =
            `✅ Lower Debt : <b>${companyB.company_name}</b>`;
    }

    if (scoreA > scoreB) {
        overallWinner.innerHTML =
            `🏆 Overall Winner : <b>${companyA.company_name}</b>`;
    }
    else if (scoreB > scoreA) {
        overallWinner.innerHTML =
            `🏆 Overall Winner : <b>${companyB.company_name}</b>`;
    }
    else {
        overallWinner.innerHTML =
            `🤝 Overall Result : <b>Tie</b>`;
    }

}
// ===============================
// Highlight Winner
// ===============================
function highlightWinner(companyA, companyB) {

    const sales1 = document.getElementById("sales1");
    const sales2 = document.getElementById("sales2");

    const profit1 = document.getElementById("profit1");
    const profit2 = document.getElementById("profit2");

    const roe1 = document.getElementById("roe1");
    const roe2 = document.getElementById("roe2");

 const roce1 = document.getElementById("roce1");
const roce2 = document.getElementById("roce2");

    const debt1 = document.getElementById("debt1");
    const debt2 = document.getElementById("debt2");

   [
    sales1, sales2,
    profit1, profit2,
    roe1, roe2,
    roce1, roce2,
    debt1, debt2
].forEach(cell => {
    if (cell) {
        cell.classList.remove("table-success", "table-danger");
    }
});
    // Sales
    if ((companyA.sales ?? 0) > (companyB.sales ?? 0)) {
        sales1.classList.add("table-success");
        sales2.classList.add("table-danger");
    } else {
        sales2.classList.add("table-success");
        sales1.classList.add("table-danger");
    }

    // Net Profit
    if ((companyA.net_profit ?? 0) > (companyB.net_profit ?? 0)) {
        profit1.classList.add("table-success");
        profit2.classList.add("table-danger");
    } else {
        profit2.classList.add("table-success");
        profit1.classList.add("table-danger");
    }

    // ROE
    if ((companyA.roe ?? 0) > (companyB.roe ?? 0)) {
        roe1.classList.add("table-success");
        roe2.classList.add("table-danger");
    } else {
        roe2.classList.add("table-success");
        roe1.classList.add("table-danger");
    }

    // ROCE
if ((companyA.roce ?? 0) > (companyB.roce ?? 0)) {
    roce1.classList.add("table-success");
    roce2.classList.add("table-danger");
} else {
    roce2.classList.add("table-success");
    roce1.classList.add("table-danger");
}

    // Debt (Lower is better)
    if ((companyA.debt_to_equity ?? 9999) < (companyB.debt_to_equity ?? 9999)) {
        debt1.classList.add("table-success");
        debt2.classList.add("table-danger");
    } else {
        debt2.classList.add("table-success");
        debt1.classList.add("table-danger");
    }

}

// ===============================
// Initialize
// ===============================

loadCompanies();

const company1Select = document.getElementById("company1");
const company2Select = document.getElementById("company2");

if (company1Select) {
    company1Select.addEventListener("change", compareCompanies);
}

if (company2Select) {
    company2Select.addEventListener("change", compareCompanies);
}