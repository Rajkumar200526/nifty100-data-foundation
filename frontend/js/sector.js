checkAuth();

let chart = null;
let sectorData = [];

#Chart.register(ChartDataLabels);

async function loadSectorAnalytics() {

    showLoader();

    try {

        const response = await fetch(
            `${window.API}/sector-analysis`,
            {
                headers: getAuthHeaders()
            }
        );

        if (!response.ok) {
            throw new Error("Failed to fetch sector analytics");
        }

        const data = await response.json();

        sectorData = data;

        // --------------------------
        // Populate Sector Filter
        // --------------------------

        const sectorFilter = document.getElementById("sectorFilter");

        if (sectorFilter) {

            sectorFilter.innerHTML =
                '<option value="All">All Sectors</option>';

            data.forEach(item => {

                sectorFilter.innerHTML += `
                    <option value="${item.sector}">
                        ${item.sector}
                    </option>
                `;

            });

        }

        updateDashboard(data);

    } catch (error) {

        console.error(error);

        showAlert("Unable to load sector analytics.", "danger");

    } finally {

        hideLoader();

    }

}

// ====================================
// Draw Doughnut Chart
// ====================================

function drawChart(labels, values) {

    const ctx = document.getElementById("sectorChart");

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels,

            datasets: [

                {

                    label: "Companies",

                    data: values,

                    backgroundColor: [

                        "#0d6efd",
                        "#198754",
                        "#ffc107",
                        "#dc3545",
                        "#6f42c1",
                        "#20c997"

                    ],

                    borderColor: "#ffffff",

                    borderWidth: 2,

                    hoverOffset: 12

                }

            ]

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

                    text: "Sector Distribution",

                    font: {

                        size: 20,

                        weight: "bold"

                    }

                },

                legend: {

                    position: "bottom"

                },

               

            }

        }

    });

}

// ====================================
// Update Dashboard
// ====================================

function updateDashboard(data) {

    document.getElementById("totalSectors").textContent =
        data.length;

    const totalCompanies =
        data.reduce((sum, item) => sum + item.companies, 0);

    document.getElementById("totalCompanies").textContent =
        totalCompanies;

    const highestROE =
        data.length
            ? Math.max(...data.map(item => item.avg_roe))
            : 0;

    document.getElementById("highestROE").textContent =
        highestROE.toFixed(2) + "%";

    const table =
        document.getElementById("sectorTable");

    table.innerHTML = "";

    const labels = [];
    const values = [];

    data.forEach(item => {

        table.innerHTML += `

            <tr class="text-center">

                <td>${item.sector}</td>

                <td>${item.companies}</td>

                <td class="text-end">
                    ₹${Number(item.avg_sales).toLocaleString()}
                </td>

                <td class="text-end">
                    ₹${Number(item.avg_profit).toLocaleString()}
                </td>

                <td class="${
                    item.avg_roe >= 30
                        ? "text-success fw-bold"
                        : "fw-bold"
                }">

                    ${Number(item.avg_roe).toFixed(2)}%

                </td>

            </tr>

        `;

        labels.push(item.sector);

        values.push(item.companies);

    });

    drawChart(labels, values);

}

// ====================================
// Filter
// ====================================

function filterSector() {

    const selected =
        document.getElementById("sectorFilter").value;

    if (selected === "All") {

        updateDashboard(sectorData);

        return;

    }

    const filtered =
        sectorData.filter(item => item.sector === selected);

    updateDashboard(filtered);

}

// ====================================
// Search
// ====================================

function searchSector() {

    const search =
        document
            .getElementById("searchSector")
            .value
            .toLowerCase();

    const filtered =
        sectorData.filter(item =>
            item.sector.toLowerCase().includes(search)
        );

    updateDashboard(filtered);

}

// ====================================
// Events
// ====================================

const sectorFilter =
    document.getElementById("sectorFilter");

if (sectorFilter) {

    sectorFilter.addEventListener(
        "change",
        filterSector
    );

}

const searchBox =
    document.getElementById("searchSector");

if (searchBox) {

    searchBox.addEventListener(
        "keyup",
        searchSector
    );

}

// ====================================
// Initialize
// ====================================

loadSectorAnalytics();