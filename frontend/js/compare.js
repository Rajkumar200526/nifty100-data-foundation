const API_URL = "http://127.0.0.1:8000";
// Get company ID from URL
const urlParams = new URLSearchParams(window.location.search);
const selectedCompany = urlParams.get("id");

// Load companies into dropdowns
async function loadCompanies() {
    try {
       const token = localStorage.getItem("token");

       const response = await fetch(`${API_URL}/company-scores`, {
        headers: {
        "Authorization": `Bearer ${token}`
    }
});
        const companies = await response.json();

        const company1 = document.getElementById("company1");
        const company2 = document.getElementById("company2");

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

        // Default selection
   if (selectedCompany) {
    company1.value = selectedCompany;

    // Select the first different company for Company 2
    for (let i = 0; i < company2.options.length; i++) {
        if (company2.options[i].value !== selectedCompany) {
            company2.selectedIndex = i;
            break;
        }
    }
} else {
    company1.selectedIndex = 0;
    company2.selectedIndex = 1;
}
// Automatically compare after selecting companies
compareCompanies();

    } catch (err) {
        console.error(err);
    }
}

// Compare companies
async function compareCompanies() {
    const token = localStorage.getItem("token");

    const id1 = document.getElementById("company1").value;
    const id2 = document.getElementById("company2").value;

    if (id1 === id2) {
        alert("Please select two different companies.");
        return;
    }

    const response = await fetch(
    `${API_URL}/compare?company1=${id1}&company2=${id2}`,
    {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }
);
    if (!response.ok) {
    alert("Unable to compare companies.");
    return;
}

const data = await response.json();
if (!Array.isArray(data) || data.length < 2) {
    alert("Comparison data not found.");
    return;
}

    const companyA = data[0];
    const companyB = data[1];

    document.getElementById("companyName1").innerText = companyA.company_name;
    document.getElementById("companyName2").innerText = companyB.company_name;
// =========================
// Sales
// =========================
const sales1 = document.getElementById("sales1");
const sales2 = document.getElementById("sales2");

sales1.innerText = Number(companyA.sales).toLocaleString();
sales2.innerText = Number(companyB.sales).toLocaleString();

// =========================
// Net Profit
// =========================
const profit1 = document.getElementById("profit1");
const profit2 = document.getElementById("profit2");

profit1.innerText = Number(companyA.net_profit).toLocaleString();
profit2.innerText = Number(companyB.net_profit).toLocaleString();

// =========================
// ROE
// =========================
const roe1 = document.getElementById("roe1");
const roe2 = document.getElementById("roe2");

roe1.innerText = companyA.roe != null
    ? Number(companyA.roe).toFixed(2)
    : "N/A";

roe2.innerText = companyB.roe != null
    ? Number(companyB.roe).toFixed(2)
    : "N/A";

// =========================
// ROA
// =========================
const roa1 = document.getElementById("roa1");
const roa2 = document.getElementById("roa2");

roa1.innerText = companyA.roa != null
    ? Number(companyA.roa).toFixed(2)
    : "N/A";

roa2.innerText = companyB.roa != null
    ? Number(companyB.roa).toFixed(2)
    : "N/A";

// =========================
// Debt to Equity
// =========================
const debt1 = document.getElementById("debt1");
const debt2 = document.getElementById("debt2");

debt1.innerText = companyA.debt_to_equity != null
    ? Number(companyA.debt_to_equity).toFixed(2)
    : "N/A";

debt2.innerText = companyB.debt_to_equity != null
    ? Number(companyB.debt_to_equity).toFixed(2)
    : "N/A";

// Draw Chart
drawChart(companyA, companyB);

// Winner Summary
showWinner(companyA, companyB);

// Highlight Better Values
highlightWinner(companyA, companyB);
}

// Draw comparison chart
let chart;

function drawChart(companyA, companyB) {

    const ctx = document.getElementById("compareChart");

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [
                "Sales",
                "Net Profit",
                "ROE",
                "ROCE",
                "Free Cash Flow"
            ],
            datasets: [
                {
                    label: companyA.company_name,
                    data: [
                        companyA.sales,
                        companyA.net_profit,
                        companyA.roe,
                        companyA.roce,
                        companyA.free_cash_flow
                    ]
                },
                {
                    label: companyB.company_name,
                    data: [
                        companyB.sales,
                        companyB.net_profit,
                        companyB.roe,
                        companyB.roce,
                        companyB.free_cash_flow
                    ]
                }
            ]
        },
        options: {
            responsive: true
        }
    });
}
function showWinner(companyA, companyB) {

    let scoreA = 0;
    let scoreB = 0;

    // Sales
    if (companyA.sales > companyB.sales) {
        scoreA++;
        document.getElementById("winnerSales").innerHTML =
            `✅ Higher Sales : <b>${companyA.company_name}</b>`;
    } else {
        scoreB++;
        document.getElementById("winnerSales").innerHTML =
            `✅ Higher Sales : <b>${companyB.company_name}</b>`;
    }

    // Net Profit
    if (companyA.net_profit > companyB.net_profit) {
        scoreA++;
        document.getElementById("winnerProfit").innerHTML =
            `✅ Higher Net Profit : <b>${companyA.company_name}</b>`;
    } else {
        scoreB++;
        document.getElementById("winnerProfit").innerHTML =
            `✅ Higher Net Profit : <b>${companyB.company_name}</b>`;
    }

    // ROE
    if (companyA.roe > companyB.roe) {
        scoreA++;
        document.getElementById("winnerROE").innerHTML =
            `✅ Better ROE : <b>${companyA.company_name}</b>`;
    } else {
        scoreB++;
        document.getElementById("winnerROE").innerHTML =
            `✅ Better ROE : <b>${companyB.company_name}</b>`;
    }

    // Debt (Lower is better)
    if (companyA.debt_to_equity < companyB.debt_to_equity) {
        scoreA++;
        document.getElementById("winnerDebt").innerHTML =
            `✅ Lower Debt : <b>${companyA.company_name}</b>`;
    } else {
        scoreB++;
        document.getElementById("winnerDebt").innerHTML =
            `✅ Lower Debt : <b>${companyB.company_name}</b>`;
    }

    if (scoreA > scoreB) {
        document.getElementById("overallWinner").innerHTML =
            `🏆 Overall Winner : ${companyA.company_name}`;
    }
    else if (scoreB > scoreA) {
        document.getElementById("overallWinner").innerHTML =
            `🏆 Overall Winner : ${companyB.company_name}`;
    }
    else {
        document.getElementById("overallWinner").innerHTML =
            "🤝 Overall Result : Tie";
    }
}
function highlightWinner(companyA, companyB) {
    const roa1 = document.getElementById("roa1");
    const roa2 = document.getElementById("roa2");

    // Get table cells
    const sales1 = document.getElementById("sales1");
    const sales2 = document.getElementById("sales2");

    const profit1 = document.getElementById("profit1");
    const profit2 = document.getElementById("profit2");

    const roe1 = document.getElementById("roe1");
    const roe2 = document.getElementById("roe2");

    const debt1 = document.getElementById("debt1");
    const debt2 = document.getElementById("debt2");

    // Remove old colors
    [
    sales1, sales2,
    profit1, profit2,
    roe1, roe2,
    roa1, roa2,
    debt1, debt2
].forEach(cell => {
        cell.classList.remove("table-success", "table-danger");
    });

    // Sales (Higher is better)
    if (companyA.sales > companyB.sales) {
        sales1.classList.add("table-success");
        sales2.classList.add("table-danger");
    } else {
        sales2.classList.add("table-success");
        sales1.classList.add("table-danger");
    }

    // Net Profit (Higher is better)
    if (companyA.net_profit > companyB.net_profit) {
        profit1.classList.add("table-success");
        profit2.classList.add("table-danger");
    } else {
        profit2.classList.add("table-success");
        profit1.classList.add("table-danger");
    }

    // ROE (Higher is better)
    if (companyA.roe > companyB.roe) {
        roe1.classList.add("table-success");
        roe2.classList.add("table-danger");
    } else {
        roe2.classList.add("table-success");
        roe1.classList.add("table-danger");
    }
    // ROA (Higher is better)
if ((companyA.roa ?? 0) > (companyB.roa ?? 0)) {
    roa1.classList.add("table-success");
    roa2.classList.add("table-danger");
} else {
    roa2.classList.add("table-success");
    roa1.classList.add("table-danger");
}

    // Debt to Equity (Lower is better)
    if (companyA.debt_to_equity < companyB.debt_to_equity) {
        debt1.classList.add("table-success");
        debt2.classList.add("table-danger");
    } else {
        debt2.classList.add("table-success");
        debt1.classList.add("table-danger");
    }
}

loadCompanies();

document.getElementById("company1").addEventListener("change", compareCompanies);
document.getElementById("company2").addEventListener("change", compareCompanies);