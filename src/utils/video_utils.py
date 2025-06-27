import os.path
import shutil
import subprocess

import cv2

from configs.folder_configs import OUTPUT_LOG_FILE


def extract_frames(input_video, output_folder):
    print(f"Extracting frames from {input_video}")

    outer_path = input_video.split("/")[0: -2]
    stdout_path = os.path.join("/", *outer_path, OUTPUT_LOG_FILE)

    ffmpeg_command = ['ffmpeg', '-i', input_video, f"{output_folder}/%05d.png"]
    with open(stdout_path, "a") as f:
        subprocess.run(ffmpeg_command, stdout=f, stderr=subprocess.STDOUT)

    # todo, use ffmpeg package, cleaner
    # (
    #     ffmpeg.input(input_video)
    #     .output(os.path.join(output_folder, "%d.png"))
    #     .run()
    # )

def create_video(input_folder):

    name = os.path.basename(input_folder)
    outer_folder = os.path.dirname(input_folder)
    video_name = f"{name}.mp4"
    video_path = os.path.join(outer_folder, video_name)

    images = sorted(os.listdir(input_folder), key=lambda x: int(os.path.splitext(x)[0]))
    frame = cv2.imread(os.path.join(input_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 30  # Adjust frame rate as needed
    video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(input_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    video.release()
    cv2.destroyAllWindows()

