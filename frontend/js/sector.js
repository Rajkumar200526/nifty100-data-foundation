const API_URL = "http://127.0.0.1:8000";
function showLoader() {
    console.log("Loading...");
}

function hideLoader() {
    console.log("Done.");
}

function showAlert(message, type = "info") {
    alert(message);
}
checkAuth();
const token = getToken();

let chart = null;
let sectorData = [];
Chart.register(ChartDataLabels);

async function loadSectorAnalytics() {

    showLoader();

    try {

        const response = await fetch(`${API_URL}/sector-analysis`, {
    headers: getAuthHeaders()
});

        if (!response.ok) {
            throw new Error("Failed to fetch sector analytics");
        }

        const data = await response.json();
        sectorData = data;
       
    // Populate sector filter
const sectorFilter = document.getElementById("sectorFilter");

if (sectorFilter) {

    sectorFilter.innerHTML = '<option value="All">All Sectors</option>';

    data.forEach(item => {
        sectorFilter.innerHTML += `
            <option value="${item.sector}">
                ${item.sector}
            </option>
        `;
    });

}



        updateDashboard(data);

  } catch (err) {

    console.error(err);
    showAlert("Unable to load sector analytics.", "danger");

} finally {

    hideLoader();

}

}

function drawChart(labels, values) {

    const ctx = document.getElementById("sectorChart");

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
           datasets: [{
    label: "Companies",
    data: values,

    backgroundColor: [
        "#0d6efd",   // Blue
        "#198754",   // Green
        "#ffc107",   // Yellow
        "#dc3545",   // Red
        "#6f42c1",   // Purple
        "#20c997"    // Teal
    ],

    borderColor: "#ffffff",
    borderWidth: 2,
    hoverOffset: 12
}]
        },
        options: {

    responsive: true,

    maintainAspectRatio: false,

    animation: {

        animateRotate: true,

        animateScale: true

    },

    plugins: {

        title: {

            display: true,

            text: "Sector Distribution of N100 Companies",

            color: "#212529",

            font: {

                size: 20,

                weight: "bold"

            }

        },

        legend: {

            position: "bottom",

            labels: {

                padding: 20,

                boxWidth: 20,

                font: {

                    size: 14

                }

            }
            

        },
        datalabels: {

    color: "#fff",

    font: {

        weight: "bold",
        size: 14

    },

    formatter: (value, context) => {

        const data = context.chart.data.datasets[0].data;

        const total = data.reduce((a, b) => a + b, 0);

        const percentage = ((value / total) * 100).toFixed(1);

        return percentage + "%";

    }

}

    }

}
    });

}

loadSectorAnalytics();

const sectorFilterElement = document.getElementById("sectorFilter");

if (sectorFilterElement) {
    sectorFilterElement.addEventListener("change", filterSector);
}

const searchSectorElement = document.getElementById("searchSector");

if (searchSectorElement) {
    searchSectorElement.addEventListener("keyup", searchSector);
}
function filterSector() {

    const selectedSector = document.getElementById("sectorFilter").value;

    let filteredData;

    if (selectedSector === "All") {

        filteredData = sectorData;

    } else {

        filteredData = sectorData.filter(item => item.sector === selectedSector);

    }

    updateDashboard(filteredData);

}
function updateDashboard(data) {
    // Update summary cards
document.getElementById("totalSectors").textContent = data.length;

const totalCompanies = data.reduce((sum, item) => sum + item.companies, 0);
document.getElementById("totalCompanies").textContent = totalCompanies;

const highestROE = data.length > 0
    ? Math.max(...data.map(item => item.avg_roe))
    : 0;

document.getElementById("highestROE").textContent =
    highestROE.toFixed(2) + "%";

    const table = document.getElementById("sectorTable");
    table.innerHTML = "";

    const labels = [];
    const values = [];

    data.forEach(item => {

        table.innerHTML += `
            <tr class="text-center">
                <td>${item.sector}</td>
                <td>${item.companies}</td>
                <td class="text-end">₹${Number(item.avg_sales).toLocaleString()}</td>
                <td class="text-end">₹${Number(item.avg_profit).toLocaleString()}</td>
                <td class="${item.avg_roe >= 30 ? 'text-success fw-bold' : 'fw-bold'}">
                    ${Number(item.avg_roe).toFixed(2)}%
                </td>
            </tr>
        `;

        labels.push(item.sector);
        values.push(item.companies);

    });

    drawChart(labels, values);

}
function searchSector() {

    const searchText = document
        .getElementById("searchSector")
        .value
        .toLowerCase();

    const filteredData = sectorData.filter(item =>
        item.sector.toLowerCase().includes(searchText)
    );

    updateDashboard(filteredData);

}