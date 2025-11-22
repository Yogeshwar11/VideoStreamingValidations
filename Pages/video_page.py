import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import subprocess

class VideoPage:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

    # def check_video_stuck(self, threshold_sec=6):
    #     fps = self.cap.get(cv2.CAP_PROP_FPS) or 25
    #     stuck_frames = 0
    #     prev_frame = None
    #     total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    #     for i in range(total_frames):
    #         ret, frame = self.cap.read()
    #         if not ret:
    #             break

    #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #         if prev_frame is not None:
    #             score = ssim(gray, prev_frame)
    #             if score > 0.995:
    #                 stuck_frames += 1
    #             else:
    #                 stuck_frames = 0

    #         if stuck_frames >= threshold_sec * fps:
    #             return False, "Video is unacceptable because of stuck while streaming"

    #         prev_frame = gray

    #     return True, "Video is acceptable"

    def check_video_stuck(self, threshold_sec=6):
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        stuck_frames = 0
        prev_frame = None
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for i in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_frame is not None:
                score = ssim(gray, prev_frame)
                if score > 0.995:
                    stuck_frames += 1
                else:
                    stuck_frames = 0
            if stuck_frames >= threshold_sec * fps:
                cap.release()
                return False, "Video is unacceptable because of stuck while streaming"
            prev_frame = gray

        cap.release()
        return True, "Video is acceptable"


    # def check_blank_screen(self, threshold_sec=6):
    #     fps = self.cap.get(cv2.CAP_PROP_FPS) or 25
    #     blank_frames = 0
    #     self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    #     total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    #     for i in range(total_frames):
    #         ret, frame = self.cap.read()
    #         if not ret:
    #             break

    #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #     # Check if almost all pixels are black or white
    #         black_ratio = np.sum(gray < 15) / gray.size
    #         white_ratio = np.sum(gray > 240) / gray.size

    #         if black_ratio > 0.95 or white_ratio > 0.95:
    #             blank_frames += 1
    #         else:
    #             blank_frames = 0

    #         if blank_frames >= threshold_sec * fps:
    #             return False, "Video is unacceptable because of white/black screen while streaming"

    #     return True, "Screen check passed"

    def check_blank_screen(self, threshold_sec=6):
    # Create a fresh capture so it starts from the first frame
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        blank_frames = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for i in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Check if almost all pixels are black or white
            black_ratio = np.sum(gray < 15) / gray.size
            white_ratio = np.sum(gray > 240) / gray.size

            if black_ratio > 0.95 or white_ratio > 0.95:
                blank_frames += 1
            else:
                blank_frames = 0

            if blank_frames >= threshold_sec * fps:
                cap.release()
                return False, "Video is unacceptable because of white/black screen while streaming"

        cap.release()
        return True, "Screen check passed"


    def check_audio(self):
        cmd = [
            "ffmpeg",
            "-i", self.video_path,
            "-map", "0:a",
            "-c", "copy",
            "-f", "null",
            "-"
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True, "Audio is present"
        except subprocess.CalledProcessError:
            return False, "Video is unacceptable because of no audio"


    def validate_video(self):
    # Check blank/white/black screen first
        screen_status, msg = self.check_blank_screen()
        if not screen_status:
            return False, msg

    # Then check stuck frames
        video_status, msg = self.check_video_stuck()
        if not video_status:
            return False, msg

    # Then check audio
        audio_status, msg = self.check_audio()
        if not audio_status:
            return False, msg

        return True, "Video is acceptable"

