import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_trajectory(trajectory_path='trajectory.npy'):
    """3D trajectory görselleştir"""
    trajectory = np.load(trajectory_path)
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Trajectory çiz
    ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 
           'b-', linewidth=2, label='Camera Path')
    
    # Başlangıç ve bitiş noktaları
    ax.scatter(trajectory[0, 0], trajectory[0, 1], trajectory[0, 2], 
              c='g', s=100, marker='o', label='Start')
    ax.scatter(trajectory[-1, 0], trajectory[-1, 1], trajectory[-1, 2], 
              c='r', s=100, marker='X', label='End')
    
    # Eksen etiketleri
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Camera Trajectory - 3D Map')
    ax.legend()
    
    # Grid
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('trajectory_3d.png', dpi=300)
    plt.show()
    
    print(f"Trajectory görselleştirildi: {len(trajectory)} poses")
    print(f"Total distance: {np.sum(np.linalg.norm(np.diff(trajectory, axis=0), axis=1)):.2f} m")

if __name__ == "__main__":
    visualize_trajectory()
