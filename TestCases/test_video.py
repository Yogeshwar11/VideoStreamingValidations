import os
from Pages.video_page import VideoPage

# Path to your videos folder
video_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "videos")

# Collect videos Sample 1.mp4 to Sample 7.mp4
videos = [os.path.join(video_folder, f"Sample {i}.mp4") for i in range(1, 8)]

results = []

for video in videos:
    if not os.path.exists(video):
        results.append((video, "File not found"))
        continue

    print(f"Validating video: {video}")
    vp = VideoPage(video)
    status, message = vp.validate_video()
    results.append((video, message))
    print(message)
    print("-"*50)

# Print summary table
print("\nSummary:")
print("{:<25} | {:<50}".format("Video", "Result"))
print("-"*80)
for video, message in results:
    print("{:<25} | {:<50}".format(os.path.basename(video), message))
