const API_BASE = "http://localhost:8000/api";

async function loadDashboard() {
    const response = await fetch(`${API_BASE}/stats`);
    const data = await response.json();

    const stats = data.stats;
    const sessions = data.recent_sessions;

    document.getElementById("totalSessions").innerText = stats.total_sessions;
    document.getElementById("totalReps").innerText = stats.total_reps;

    const minutes = (stats.total_duration_seconds / 60).toFixed(1);
    document.getElementById("trainingTime").innerText = minutes + " min";

    // Most common error
    const errorCounts = {};
    sessions.forEach(s => {
        if (!errorCounts[s.dominant_error]) {
            errorCounts[s.dominant_error] = 0;
        }
        errorCounts[s.dominant_error]++;
    });

    const mostCommon = Object.keys(errorCounts).reduce((a, b) =>
        errorCounts[a] > errorCounts[b] ? a : b
    , "-");

    document.getElementById("commonError").innerText = mostCommon;

    renderTrendChart(sessions);
    renderDistributionChart(sessions);
}

function renderTrendChart(sessions) {
    const labels = sessions.map(s =>
        new Date(s.created_at).toLocaleDateString()
    );
    const reps = sessions.map(s => s.rep_count);

    new Chart(document.getElementById("trendChart"), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Reps per Session",
                data: reps,
                borderColor: "#ff3b3b",
                backgroundColor: "rgba(255,59,59,0.2)",
                tension: 0.3
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: "#aaa" } },
                y: { ticks: { color: "#aaa" } }
            }
        }
    });
}

function renderDistributionChart(sessions) {
    const distribution = {};

    sessions.forEach(s => {
        if (!distribution[s.exercise_type]) {
            distribution[s.exercise_type] = 0;
        }
        distribution[s.exercise_type]++;
    });

    new Chart(document.getElementById("distributionChart"), {
        type: "doughnut",
        data: {
            labels: Object.keys(distribution),
            datasets: [{
                data: Object.values(distribution),
                backgroundColor: ["#ff3b3b", "#444", "#777"]
            }]
        }
    });
}

loadDashboard();
