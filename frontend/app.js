const API_BASE = "/api";

async function analyzeVideo() {
    const fileInput = document.getElementById("videoInput");

    if (!fileInput) {
        console.error("videoInput element not found");
        return;
    }

    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a video file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("exercise_type", "squat");

    document.getElementById("loading").classList.remove("hidden");

    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        document.getElementById("repCount").innerText =
            data.metrics.rep_count;

        document.getElementById("duration").innerText =
            data.metrics.duration_seconds + " sec";

        document.getElementById("dominantError").innerText =
            data.analysis.dominant_error;

        document.getElementById("recommendation").innerText =
            data.recommendations?.[0] || "Improve your form.";

        document.getElementById("results").classList.remove("hidden");
    } catch (error) {
        alert("Error analyzing video.");
        console.error(error);
    }

    document.getElementById("loading").classList.add("hidden");
}
