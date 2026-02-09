import torch
import cv2
import numpy as np

class DepthEstimator:
    def __init__(self, model_type="MiDaS_small"):
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        print(f"Depth AI Device: {self.device}")
        
        # Load MiDaS model from Torch Hub
        self.model = torch.hub.load("intel-isl/MiDaS", model_type)
        self.model.to(self.device)
        self.model.eval()
        
        # Transforms
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        if model_type == "MiDaS_small":
            self.transform = midas_transforms.small_transform
        else:
            self.transform = midas_transforms.dpt_transform

    def estimate(self, img):
        """
        img: OpenCV BGR image
        Returns: Depth map (numpy array, normalized relative depth)
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        input_batch = self.transform(img_rgb).to(self.device)
        
        with torch.no_grad():
            prediction = self.model(input_batch)
            
            # Resize to original resolution
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()
            
            depth_map = prediction.cpu().numpy()
            
            # Normalize (Optional, depends on use case. MiDaS gives relative inverse depth)
            # For visualization, we might want to invert it?
            ## MiDaS output is inverse depth (disparity-like). 
            ## Real Depth ~= 1 / Prediction
            
            # Prevent division by zero
            depth_map = np.maximum(depth_map, 1e-2)
            
            # Convert to metric-like scale (Unknown scale factor in Monocular)
            # We assume some scale. 
            # Invert to get Z
            depth_metric = 1000.0 / depth_map # Arbitrary scale
            
            return depth_metric
