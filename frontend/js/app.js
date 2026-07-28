const API = "http://127.0.0.1:8000";

fetch(API + "/company-scores")
.then(res => res.json())
.then(data => {

    document.getElementById("companies").innerHTML = data.length;

    let total = 0;
    let max = 0;
    let min = 999;

    let rows = "";

    let labels = [];
    let values = [];

    let sectorData = {};
    let recData = {};

    data.forEach(item => {

        total += item["Investment Score"];

        if(item["Investment Score"] > max)
            max = item["Investment Score"];

        if(item["Investment Score"] < min)
            min = item["Investment Score"];

        rows += `
        <tr>
            <td>${item.Rank}</td>
            <td>${item.company_name}</td>
            <td>${item.broad_sector}</td>
            <td>${item["Investment Score"].toFixed(2)}</td>
            <td>${item.Recommendation}</td>
        </tr>
        `;

        labels.push(item.company_name);
        values.push(item["Investment Score"]);

        sectorData[item.broad_sector] =
            (sectorData[item.broad_sector] || 0) + 1;

        recData[item.Recommendation] =
            (recData[item.Recommendation] || 0) + 1;

    });

    document.getElementById("tableBody").innerHTML = rows;

    document.getElementById("avgscore").innerHTML =
        (total / data.length).toFixed(2);

    document.getElementById("highest").innerHTML =
        max.toFixed(2);

    document.getElementById("lowest").innerHTML =
        min.toFixed(2);

    // Investment Score Chart
    new Chart(document.getElementById("scoreChart"), {

        type: "bar",

        data: {
            labels: labels,
            datasets: [{
                label: "Investment Score",
                data: values
            }]
        }

    });

    // Sector Chart
    new Chart(document.getElementById("sectorChart"), {

        type: "pie",

        data: {

            labels: Object.keys(sectorData),

            datasets: [{
                data: Object.values(sectorData)
            }]

        }

    });

    // Recommendation Chart
    new Chart(document.getElementById("recommendChart"), {

        type: "doughnut",

        data: {

            labels: Object.keys(recData),

            datasets: [{
                data: Object.values(recData)
            }]

        }

    });

    // Search
    document.getElementById("searchBox")
    .addEventListener("keyup", function () {

        const value = this.value.toLowerCase();

        document.querySelectorAll("#tableBody tr")
        .forEach(row => {

            row.style.display =
                row.innerText.toLowerCase().includes(value)
                ? ""
                : "none";

        });

    });

});

// Auto Refresh every 60 seconds
setTimeout(() => {
    location.reload();
}, 60000);