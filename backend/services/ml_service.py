from ml.inference import PostureInference


class MLService:

    def __init__(self):
        self.model = PostureInference()

    def analyze_video(self, path: str):
        return self.model.analyze_video(path)
