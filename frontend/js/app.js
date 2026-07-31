checkAuth();

fetch(window.API + "/company-scores", {
    headers: getAuthHeaders()
})
.then(res => {

    if (!res.ok) {
        throw new Error("Unable to load company scores");
    }

    return res.json();

})
.then(data => {

    document.getElementById("companies").innerHTML = data.length;

    let total = 0;
    let max = 0;
    let min = Number.MAX_VALUE;

    let rows = "";

    let labels = [];
    let values = [];

    let sectorData = {};
    let recData = {};

    data.forEach(item => {

        const score = Number(item.investment_score ?? 0);

        total += score;

        if (score > max) max = score;
        if (score < min) min = score;

        rows += `
        <tr>
            <td>${item.rank ?? "-"}</td>
            <td>${item.company_name}</td>
            <td>${item.broad_sector}</td>
            <td>${score.toFixed(2)}</td>
            <td>${item.recommendation ?? "-"}</td>
        </tr>
        `;

        labels.push(item.company_name);
        values.push(score);

        sectorData[item.broad_sector] =
            (sectorData[item.broad_sector] || 0) + 1;

        recData[item.recommendation] =
            (recData[item.recommendation] || 0) + 1;

    });

    document.getElementById("tableBody").innerHTML = rows;

    document.getElementById("avgscore").innerHTML =
        data.length ? (total / data.length).toFixed(2) : "0";

    document.getElementById("highest").innerHTML =
        max.toFixed(2);

    document.getElementById("lowest").innerHTML =
        min === Number.MAX_VALUE ? "0" : min.toFixed(2);

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

})
.catch(error => {

    console.error(error);

    showAlert("Unable to load dashboard data.", "danger");

});

// Auto Refresh every 60 seconds
setTimeout(() => {
    location.reload();
}, 60000);