import open3d as o3d
import numpy as np
import cv2

class MapVisualizer:
    def __init__(self, width=960, height=720):
        # self.vis = o3d.visualization.Visualizer()
        # self.vis.create_window(window_name='3D Map (Real-Time)', width=width, height=height)
        self.vis = None
        
        # Camera trajectory (LineSet)
        self.trajectory = o3d.geometry.LineSet()
        # self.vis.add_geometry(self.trajectory)
        
        # Feature Points (PointCloud) - Now capable of handling dense clouds
        self.pcd = o3d.geometry.PointCloud()
        # self.vis.add_geometry(self.pcd)
        
        # Coordinate Frame (Origin)
        axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])
        # self.vis.add_geometry(axis)
        
        # Data storage
        self.poses = []
        # We NO LONGER store self.points as a python list. 
        # We mainly rely on self.pcd
        
        # View Control (DISABLED FOR 2D ONLY MODE)
        # self.ctr = self.vis.get_view_control()
        # self.ctr.set_constant_z_far(1000)
        self.ctr = None

    def update(self, current_pose, new_points3d=None, dense_color=None):
        """
        current_pose: 4x4 matrix (Global pose)
        new_points3d: Nx3 array of 3D points (Global coordinates)
        dense_color: Nx3 array of RGB colors (0-1) corresponding to points
        """
        # --- Update Trajectory ---
        # Add current position
        self.poses.append(current_pose[:3, 3])
        
        # --- Update Point Cloud ---
        # Note: We rely on self.pcd (Open3D PointCloud) for storage and optimization
        
        # --- 3D Visualization (Open3D) ---
        if self.vis is not None and len(self.poses) > 1:
            points = np.array(self.poses)
            lines = [[i, i+1] for i in range(len(self.poses)-1)]
            self.trajectory.points = o3d.utility.Vector3dVector(points)
            self.trajectory.lines = o3d.utility.Vector2iVector(lines)
            self.trajectory.colors = o3d.utility.Vector3dVector([[0, 0, 1] for _ in lines]) # Blue path
            self.vis.update_geometry(self.trajectory)

        if new_points3d is not None and len(new_points3d) > 0:
            new_pcd = o3d.geometry.PointCloud()
            new_pcd.points = o3d.utility.Vector3dVector(new_points3d)
            if dense_color is not None:
                 new_pcd.colors = o3d.utility.Vector3dVector(dense_color)
            else:
                 colors = np.tile([0, 1, 0], (len(new_points3d), 1))
                 new_pcd.colors = o3d.utility.Vector3dVector(colors)
            new_pcd = new_pcd.voxel_down_sample(voxel_size=0.05)
            self.pcd += new_pcd
            if len(self.pcd.points) > 500000 or len(self.poses) % 30 == 0:
                 self.pcd = self.pcd.voxel_down_sample(voxel_size=0.05)
            if self.vis is not None:
                self.vis.update_geometry(self.pcd)
            
        if self.vis is not None:
             self.vis.poll_events()
             self.vis.update_renderer()

    def draw_2d_map(self, map_size=800, scale=50):
        """
        Draws a 2D X-Z map (Top-Down View).
        map_size: Pixel size of the map image (square).
        scale: Scale factor to convert meters to pixels.
        """
        # Create blank canvas (White background)
        map_img = np.ones((map_size, map_size, 3), dtype=np.uint8) * 255
        
        center_x = map_size // 2
        center_z = map_size // 2
        
        # Draw Coordinate Grid
        cv2.line(map_img, (0, center_z), (map_size, center_z), (200, 200, 200), 1)
        cv2.line(map_img, (center_x, 0), (center_x, map_size), (200, 200, 200), 1)
        
        # Draw Map Points (X, Z) - Ignore Y
        # Use Open3D Point Cloud Data (which is already downsampled)
        if self.pcd.has_points():
            points = np.asarray(self.pcd.points)
            if len(points) > 0:
                # Filter points based on Y (height) to get a "slice" or just project all
                # Assuming camera connects to robot at Y=0 approx, we project everything.
                # Convert X, Z to pixel coordinates
                # X -> X (Right), Z -> Y (Forward/Up in 2D image)
                
                # Optimization: Vectorized transform
                # X is index 0, Z is index 2
                pts_x = (points[:, 0] * scale).astype(np.int32) + center_x
                pts_z = center_z - (points[:, 2] * scale).astype(np.int32) # Z is forward, so subtract from center_z (up)
                
                # Bound check
                valid = (pts_x >= 0) & (pts_x < map_size) & (pts_z >= 0) & (pts_z < map_size)
                
                # Draw points (as small circles or direct pixels)
                # For speed, direct pixel access might be faster but circle is clearer for sparse points
                # Check point count - if too many > 10000, use pixel manipulation if possible or just circles
                # For now stick to circle, it's visibly nice
                for px, pz in zip(pts_x[valid], pts_z[valid]):
                    cv2.circle(map_img, (px, pz), 1, (0, 0, 0), -1) # Black dots
                
        # Draw Trajectory
        if len(self.poses) > 1:
            traj_pts = []
            for pose in self.poses:
                x = int(pose[0] * scale) + center_x
                z = center_z - int(pose[2] * scale)
                traj_pts.append((x, z))
            
            # Draw lines
            for i in range(len(traj_pts) - 1):
                cv2.line(map_img, traj_pts[i], traj_pts[i+1], (0, 0, 255), 2) # Red trajectory
                
        # Draw Current Pose Arrow
        if len(self.poses) > 0:
            curr_pos = self.poses[-1]
            cx = int(curr_pos[0] * scale) + center_x
            cz = center_z - int(curr_pos[2] * scale)
            cv2.circle(map_img, (cx, cz), 3, (255, 0, 0), -1) # Blue dot for robot
            
        return map_img

    def save_pose_graph(self, filename='pose_graph.png'):
        """
        Saves the final trajectory and map to a high-quality image file using Matplotlib.
        Mimics the 'Pose Graph' style.
        """
        import matplotlib.pyplot as plt
        
        if len(self.poses) < 2:
            print("Not enough pose data to save graph.")
            return

        poses = np.array(self.poses)
        # X and Z coordinates
        x = poses[:, 0]
        z = poses[:, 2]
        
        plt.figure(figsize=(10, 10))
        
        # Plot Trajectory (Blue line)
        plt.plot(x, z, 'b-', linewidth=2, label='Trajectory')
        plt.plot(x[0], z[0], 'go', label='Start')
        plt.plot(x[-1], z[-1], 'ro', label='End')
        
        # Plot Map Points (Pink/Magenta dots)
        if hasattr(self, 'map_points') and len(self.map_points) > 0:
            # Filter standard Y-range for cleanliness if needed, or just plot all X-Z
            # Let's plot all
            mx = self.map_points[:, 0]
            mz = self.map_points[:, 2]
            
            # Downsample for plotting speed if massive
            if len(mx) > 10000:
                idx = np.random.choice(len(mx), 10000, replace=False)
                mx = mx[idx]
                mz = mz[idx]
                
            plt.scatter(mx, mz, c='m', s=1, alpha=0.5, label='Map Points')

        plt.title('Pose Graph (Top-Down X-Z)')
        plt.xlabel('X (meters)')
        plt.ylabel('Z (meters)')
        plt.legend()
        plt.grid(True)
        plt.axis('equal')
        
        plt.savefig(filename)
        plt.close()
        print(f"Pose Graph saved to {filename}")

    def close(self):
        if self.vis is not None:
            self.vis.destroy_window()
