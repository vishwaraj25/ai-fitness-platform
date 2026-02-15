import random

class PostureInference:

    def __init__(self):
        pass

    def analyze_video(self, path: str):
        rep_count = random.randint(5, 15)
        duration_seconds = random.randint(20, 60)

        dominant_errors = [
            "knees_caving",
            "leaning_forward",
            "shallow_depth",
            "good_form"
        ]

        dominant_error = random.choice(dominant_errors)

        return {
            "rep_count": rep_count,
            "duration_seconds": duration_seconds,
            "analysis": {
                "dominant_error": dominant_error
            },
            "recommendations": [
                "Focus on controlled movement.",
                "Keep your back straight.",
                "Engage your core."
            ]
        }
