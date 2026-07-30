

checkAuth();

const token = getToken();

const params = new URLSearchParams(window.location.search);
const companyId = params.get("id");
const portfolioBtn = document.getElementById("portfolioBtn");

portfolioBtn.addEventListener("click", addToPortfolio);
const recommendationBtn = document.getElementById("recommendationBtn");

if (recommendationBtn) {
    recommendationBtn.href = `recommendation.html?id=${companyId}`;
}

if (!companyId) {
    showAlert("Company ID not found.", "warning");

    setTimeout(() => {
        window.location.href = "dashboard.html";
    }, 1500);

    throw new Error("Missing company id");
}

// Set button links
document.getElementById("compareLink").href = `compare.html?id=${companyId}`;
document.getElementById("ratioLink").href = `ratios.html?id=${companyId}`;

async function loadCompany() {

    showLoader();

    try {

      const response = await fetch(`${API}/companies/${companyId}`, {
    headers: getAuthHeaders()
});

        if (!response.ok) {

            showAlert("Unable to load company details.", "danger");

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1500);

            return;
        }

        const company = await response.json();

        // Main Card
        document.getElementById("companyName").textContent =
            company.company_name;

        document.getElementById("sector").textContent =
            company.broad_sector;

        document.getElementById("score").textContent =
            company.investment_score;

        document.getElementById("recommendation").textContent =
    company.recommendation;

document.getElementById("rank").textContent =
    company.rank;

        // Summary Table
        document.getElementById("companyNameTable").textContent =
            company.company_name;

        document.getElementById("sectorTable").textContent =
            company.broad_sector;

        document.getElementById("scoreTable").textContent =
            company.investment_score;

        document.getElementById("recommendationTable").textContent =
    company.recommendation;

document.getElementById("rankTable").textContent =
    company.rank;

    } catch (error) {

        console.error(error);

        showAlert("Server connection failed.", "danger");

    } finally {

        hideLoader();

    }

}


loadCompany();
async function addToPortfolio(event) {

    event.preventDefault();

    const token = localStorage.getItem("token");

    const response = await fetch(

        `${API}/portfolio/${companyId}`,

        {

            method: "POST",

            headers: {

                "Authorization": `Bearer ${token}`

            }

        }

    );

    const result = await response.json();

    alert(result.message);

}