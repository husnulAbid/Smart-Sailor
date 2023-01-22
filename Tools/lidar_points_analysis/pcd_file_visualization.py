import math
import itertools
import numpy as np
import open3d as o3d


def plot_whole_cloud_points(pcd_file_name):
    pcd = o3d.io.read_point_cloud(pcd_file_name)
    o3d.visualization.draw_geometries([pcd])


def plot_partial_cloud_points(pcd_file_name):
    pcd = o3d.io.read_point_cloud(pcd_file_name)

    # bounds = [[0, math.inf], [0, -math.inf], [-math.inf, math.inf]]
    # bounds = [[-5000, 5000], [-5000, 5000], [-math.inf, math.inf]]
    
    bounds = [[-5000, 5000], [-1500, 1500], [-math.inf, math.inf]]
    bounding_box_points = list(itertools.product(*bounds)) 

    bounding_box = o3d.geometry.AxisAlignedBoundingBox.create_from_points(
        o3d.utility.Vector3dVector(bounding_box_points)) 

    pcd_croped = pcd.crop(bounding_box)
    o3d.visualization.draw_geometries([pcd_croped])


if __name__ == '__main__':
    input_folder_name = 'input_folder'
    pcd_file_name = f'{input_folder_name}/1.pcd'

    plot_whole_cloud_points(pcd_file_name)
    
    plot_partial_cloud_points(pcd_file_name)