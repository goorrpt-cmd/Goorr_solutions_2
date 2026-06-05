document.addEventListener("DOMContentLoaded", () => {

    // Fetch KPI data
    fetch("/dashboard/recent-candidates/")
        .then(r => r.json())
        .then(data => {
            document.getElementById("kpi-candidates").innerText = data.total;
        });

    // Example chart
    const ctx = document.getElementById("chartCandidates");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Jan", "Feb", "Mar"],
            datasets: [{
                label: "Candidates",
                data: [5, 12, 20],
                borderColor: "#1e88e5",
                fill: false
            }]
        }
    });
});
