import sys

sys.path.append('../../external/Easi3R')

from demo import get_reconstructed_scene
import torch
from dust3r.utils.device import to_numpy


class Easi3rWrapper:
    def __init__(self, config, dust3r_model=None):
        # Store the config and model reference
        self.config = config
        self.dust3r_model = dust3r_model

    def generate_dynamic_pointclouds(self, video_frames_or_path):
        """
        Extract point clouds from video frames using Easi3r pipeline

        Args:
            video_frames_or_path: Either list of frame paths or video file path

        Returns:
            List of point clouds (one per frame)
        """
        # Call Easi3r's reconstruction function
        scene, outfile, temp_video_path, temp_attn_video_path, temp_cluster_video_path = get_reconstructed_scene(
            args=self.config.args,  # You'll need to pass the args
            outdir=self.config.output_dir,
            model=self.dust3r_model,  # Use injected DUSt3R model
            device=self.config.device,
            silent=self.config.silent,
            image_size=self.config.image_size,
            filelist=video_frames_or_path,
            # ... other parameters from your config
        )

        # Extract point clouds from scene
        point_clouds = self.extract_point_clouds_from_scene(scene)

        return point_clouds, scene  # Return both for flexibility

    def extract_point_clouds_from_scene(self, scene):
        """Extract individual point clouds for each frame"""
        # Get 3D points and colors
        pts3d = to_numpy(scene.get_pts3d(raw_pts=True))  # Shape: (num_frames, H, W, 3)
        rgbimg = scene.imgs  # RGB images
        masks = to_numpy(scene.get_masks())  # Confidence masks

        point_clouds = []
        for i in range(len(rgbimg)):
            # Extract point cloud for frame i
            points = pts3d[i]  # (H, W, 3)
            colors = rgbimg[i]  # (H, W, 3)
            mask = masks[i]  # (H, W)

            # Flatten and filter by mask
            valid_mask = mask > 0
            valid_points = points[valid_mask]
            valid_colors = colors[valid_mask]

            point_cloud = {
                'points': valid_points,  # (N, 3)
                'colors': valid_colors,  # (N, 3)
                'mask': mask,  # (H, W) - for spatial reference
                'camera_pose': scene.get_im_poses()[i].cpu().numpy(),
                'focal_length': scene.get_focals()[i].cpu().numpy(),
                'frame_idx': i
            }
            point_clouds.append(point_cloud)

        return point_clouds