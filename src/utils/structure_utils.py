import os
import shutil

from configs.folder_configs import CAMERA_FRAMES_DIR, INPUTS_DIR, RESULTS_DIR, SEPERATED_CAMERAS_DIR, \
    ORIGINAL_VIDEOS_DIR, DIFFUSION_FRAMES, RENDER_FRAMES
from .video_utils import extract_frames, create_video

def create_folder_structure(folders):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print('Created folder:', folder)

def setup_structure(source_videos_path, output_directory):
    frames_path = os.path.join(output_directory, CAMERA_FRAMES_DIR)
    all_frames_path = os.path.join(output_directory, INPUTS_DIR)
    results_path = os.path.join(output_directory, RESULTS_DIR)
    cameras_path = os.path.join(output_directory, SEPERATED_CAMERAS_DIR)

    all_folders = [frames_path, all_frames_path, results_path, cameras_path]
    create_folder_structure(all_folders)

    # copy video folder
    video_path = os.path.join(output_directory, ORIGINAL_VIDEOS_DIR)
    num_videos = len(os.listdir(source_videos_path))
    shutil.copytree(source_videos_path, video_path)
    print(f"Copying {num_videos} videos from {source_videos_path} to {video_path}")

    # extract frames
    for video in os.listdir(source_videos_path):
        video_name, video_ext = os.path.splitext(video)
        new_path = os.path.join(frames_path, video_name)
        os.makedirs(new_path)
        extract_frames(os.path.join(source_videos_path, video), new_path)

    frame_folders = sorted(os.listdir(frames_path))
    folder_paths = [os.path.join(frames_path, folder) for folder in frame_folders]
    folder_files = [sorted(os.listdir(folder)) for folder in folder_paths]

    num_frames = len(folder_files[0])
    num_folders = len(folder_files)

    for frame_counter in range(num_frames):
        frame_counter_folder = os.path.join(all_frames_path, str(frame_counter))
        os.mkdir(frame_counter_folder)

        for i in range(num_folders):
            src_path = os.path.join(folder_paths[i], folder_files[i][frame_counter])
            dest_path = os.path.join(frame_counter_folder, f"{i}.png")
            shutil.copyfile(src_path, dest_path)

    # todo think about saving guidance image?

def separate_cameras(results_folder, cameras_folder): # todo think about naming
    frame_types = [DIFFUSION_FRAMES, RENDER_FRAMES] # todo nicer solution needed

    for frame_number in os.listdir(results_folder):
        if not os.path.isdir(os.path.join(results_folder, frame_number)):
            continue

        for frame_type in frame_types:
            frame_folder = os.path.join(results_folder, frame_number, frame_type)
            for camera in os.listdir(frame_folder):
                file_name = os.path.join(frame_folder, camera)
                name, ext = os.path.splitext(camera)
                name = name.split("_")[1]

                name_folder = os.path.join(cameras_folder, frame_type, f"camera_{name}")
                # print(name_folder, "--", file_name)
                if not os.path.exists(name_folder):
                    os.makedirs(name_folder)

                shutil.copyfile(file_name, f"{name_folder}/{frame_number}.png")

    print("Creating Videos") # todo move to video utils
    for frame_type in frame_types:
        camera_files = [f for f in os.listdir(os.path.join(cameras_folder, frame_type))]
        for file in camera_files:
            create_video(os.path.join(cameras_folder, frame_type, file))