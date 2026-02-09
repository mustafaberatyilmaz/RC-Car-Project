import cv2
import numpy as np

class OccupancyGrid:
    def __init__(self, size=800, resolution=0.05):
        """
        size: Grid size in pixels (Square)
        resolution: Meters per pixel
        """
        self.size = size
        self.resolution = resolution
        self.center = size // 2
        
        # Probabilistic Grid
        # visits: How many times a ray passed through or hit this cell
        # occupied: How many times a ray hit this cell (obstacle)
        self.visits = np.zeros((size, size), dtype=np.uint32)
        self.occupied = np.zeros((size, size), dtype=np.uint32)
        
        # Thresholds
        self.min_visits = 3 # Minimum observations to determine state
        self.prob_threshold = 0.3 # Ratio > 0.3 means Occupied
        
    def update(self, current_pose, map_points):
        """
        current_pose: 4x4 matrix
        map_points: Nx3 array
        """
        if len(map_points) == 0:
            return

        # Camera Position (X, Z) in Grid Coords
        cx = int(current_pose[0, 3] / self.resolution) + self.center
        cz = self.center - int(current_pose[2, 3] / self.resolution)
        
        # Check camera bounds
        if not (0 <= cx < self.size and 0 <= cz < self.size):
            return

        # Vectorized transform to Grid Coords
        pts_x = (map_points[:, 0] / self.resolution).astype(np.int32) + self.center
        pts_z = self.center - (map_points[:, 2] / self.resolution).astype(np.int32)
        
        # Valid bounds
        valid = (pts_x >= 0) & (pts_x < self.size) & (pts_z >= 0) & (pts_z < self.size)
        pts_x = pts_x[valid]
        pts_z = pts_z[valid]
        
        if len(pts_x) == 0:
            return
            
        # --- Raytracing (Bresenham optimized with OpenCV) ---
        
        # 1. Update VISITS (Ray passing through)
        # We draw lines from Camera to Points on a temp mask, then add to global
        # To avoid saturation in one frame, we cap update or just add 1.
        # Efficient way: Draw all lines on a uint8 temp, then add.
        # Problem: Overlapping lines in one frame? 
        # Simpler: Just loop and draw. Python loop might be slow for 5000 points.
        # But we can limit points.
        
        # Sampling optimization: If too many points, subsample
        if len(pts_x) > 2000:
             indices = np.random.choice(len(pts_x), 2000, replace=False)
             pts_x = pts_x[indices]
             pts_z = pts_z[indices]

        camera_pt = (cx, cz)
        
        # We will use a temp buffer to accumulate visits for this frame
        # to avoid slow python loops update if possible, but cv2.line is fast.
        # Let's iterate.
        
        # Create a temp mask for 'visits' in this frame to allow batch add?
        # Actually, standard cv2.line on a numpy array is very fast.
        
        for px, pz in zip(pts_x, pts_z):
            # Draw Line: Increment Visits
            # We assume 'line' includes endpoints.
            # We want to increment 'visits' for all cells on the line.
            # Using cv2.line on integer array? cv2.line works on image.
            # Let's use a temporary uint8 layer for this batch
            
            # Note: We can't easily add '1' to specific cells with cv2.line directly on int32.
            # Workaround: Draw white lines on black image, then find non-zero? No, we need count.
            # Correct Way: Bresenham Iterator.
            # Fast Approximation: Use cv2.lineIterator? 
            # Fastest Pythonic way for dense map:
            # Just draw 'Free' space as White on a visual map? 
            # No, user wants probabilistic.
            
            # Let's stick to a simpler "Counter" approach.
            # Step 1: Draw ALL rays on a temp "visit_mask" (add 1 per ray? No, binary is enough for FOV)
            # Actually, if 5 rays pass through a cell in one frame, is it 1 visit or 5?
            # Usually 1 'scan' counts as 1 visit per frame.
            
            pass 
        
        # OPTIMIZED APPROACH:
        # 1. VISITS: Draw lines on a temp mask (0 or 1). 
        #    If a cell is covered by ANY ray in this frame, count it as +1 visit.
        temp_visits = np.zeros((self.size, self.size), dtype=np.uint8)
        
        # Draw all rays
        # To do this fast without loops: 
        # Can we draw multiple lines? cv2.polylines? No.
        # Loop is necessary.
        for px, pz in zip(pts_x, pts_z):
            cv2.line(temp_visits, camera_pt, (px, pz), 1, 1)
            
        self.visits += temp_visits
        
        # 2. OCCUPIED: Mark endpoints
        temp_occupied = np.zeros((self.size, self.size), dtype=np.uint8)
        temp_occupied[pts_z, pts_x] = 1 # Advanced indexing
        
        self.occupied += temp_occupied
            
    def get_map_image(self):
        # Generate Display Image
        # Gray (127) = Unknown (Visits < min_visits)
        # White (255) = Free (Occupied/Visits < Threshold)
        # Black (0) = Occupied (Occupied/Visits > Threshold)
        
        # default gray
        display_map = np.ones((self.size, self.size), dtype=np.uint8) * 127
        
        # Mask where we have enough data
        known_mask = self.visits >= self.min_visits
        
        if np.any(known_mask):
            # Calculate probability P = occupied / visits
            # Avoid division by zero (handled by mask, visits >= 3 implies >0)
            occupancy_prob = np.zeros_like(self.visits, dtype=np.float32)
            np.divide(self.occupied, self.visits, out=occupancy_prob, where=known_mask)
            
            # Apply Thresholds
            # Free
            free_mask = (occupancy_prob < self.prob_threshold) & known_mask
            display_map[free_mask] = 255 # White
            
            # Occupied
            occ_mask = (occupancy_prob >= self.prob_threshold) & known_mask
            display_map[occ_mask] = 0 # Black
            
        # Draw Camera
        # (Optional, maybe caller draws it)
            
        return display_map
