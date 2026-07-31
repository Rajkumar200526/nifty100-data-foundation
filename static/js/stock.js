const API = "https://nifty-financial-analytics-platform-ikzb.onrender.com";

let chart = null;

async function loadStockTrend(companyId) {

    const response = await fetch(`${API}/stock-trends/${companyId}`);

    const data = await response.json();

    const labels = data.map(item => item.trade_date);

    const prices = data.map(item => item.close_price);

    if (chart) {
        chart.destroy();
    }

    const ctx = document.getElementById("stockChart").getContext("2d");

    chart = new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [{

                label: "Close Price",

                data: prices,

                borderWidth: 2,
                fill: false

            }]
        }

    });

}

document.getElementById("companySelect").addEventListener("change", function () {

    loadStockTrend(this.value);

});

loadStockTrend(1);