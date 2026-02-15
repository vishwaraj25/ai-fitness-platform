from inference import PostureInference

model = PostureInference()

result = model.analyze_video("test.mp4")

print("Prediction:", result)
