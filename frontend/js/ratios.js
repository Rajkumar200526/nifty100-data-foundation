const API = "http://127.0.0.1:8000";

const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "login.html";
}

const params = new URLSearchParams(window.location.search);
const companyId = params.get("id");

async function loadRatios() {

    try {

        const response = await fetch(`${API}/company/${companyId}/ratios`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            alert("Unable to load financial ratios.");
            return;
        }

        const data = await response.json();

        // Latest year data
        const latest = data[data.length - 1];

        // Company Details
        document.getElementById("companyName").innerHTML = latest.company_name;

        document.getElementById("roe").innerHTML = latest.roe + " %";
        document.getElementById("roa").innerHTML = latest.roa + " %";
        document.getElementById("debt").innerHTML = latest.debt_to_equity;

        // Not available in database
        document.getElementById("current").innerHTML = "N/A";
        document.getElementById("pe").innerHTML = "N/A";
        document.getElementById("eps").innerHTML = "N/A";
        document.getElementById("marketcap").innerHTML = "N/A";

        // Arrays for charts
        const years = data.map(item => item.year);
        const sales = data.map(item => item.sales);
        const profits = data.map(item => item.net_profit);
        const roe = data.map(item => item.roe);
        const freeCashFlow = data.map(item => item.free_cash_flow);

        // Sales Chart
        new Chart(document.getElementById("salesChart"), {
            type: "line",
            data: {
                labels: years,
                datasets: [{
                    label: "Sales",
                    data: sales,
                    borderWidth: 3,
                    fill: false
                }]
            }
        });

        // Net Profit Chart
        new Chart(document.getElementById("profitChart"), {
            type: "bar",
            data: {
                labels: years,
                datasets: [{
                    label: "Net Profit",
                    data: profits
                }]
            }
        });

        // ROE Chart
        new Chart(document.getElementById("roeChart"), {
            type: "line",
            data: {
                labels: years,
                datasets: [{
                    label: "ROE %",
                    data: roe,
                    borderWidth: 3,
                    fill: false
                }]
            }
        });

        // Free Cash Flow Chart
        new Chart(document.getElementById("fcfChart"), {
            type: "bar",
            data: {
                labels: years,
                datasets: [{
                    label: "Free Cash Flow",
                    data: freeCashFlow
                }]
            }
        });

    } catch (error) {
        console.error(error);
        alert("Error loading financial data.");
    }

}

loadRatios();