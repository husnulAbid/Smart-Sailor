import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# original paper : https://arxiv.org/pdf/1608.07916.pdf


def lidar_to_2d_front_view(x_lidar, y_lidar, z_lidar, r_lidar, count, v_res, h_res, v_fov, val="depth", cmap="jet", saveto=None, y_fudge=0.0):

    assert len(v_fov) ==2, "v_fov must be list/tuple of length 2"
    assert v_fov[0] <= 0, "first element in v_fov must be 0 or negative"
    assert val in {"depth", "height", "reflectance"}, 'val must be one of {"depth", "height", "reflectance"}'


    d_lidar = np.sqrt(x_lidar ** 2 + y_lidar ** 2)
    v_fov_total = -v_fov[0] + v_fov[1]

    # Convert to Radians
    v_res_rad = v_res * (np.pi/180)
    h_res_rad = h_res * (np.pi/180)

    # Project into image coordinates
    x_img = np.arctan2(y_lidar, x_lidar)/ h_res_rad         # -y_lidar in main code
    y_img = np.arctan2(z_lidar, d_lidar)/ v_res_rad

    # Shift coordinates to make 0,0 
    x_min = -360.0 / h_res / 2          # Theoretical min x value based on sensor specs
    x_img -= x_min                      # Shift
    x_max = 360.0 / h_res               # Theoretical max x value after shifting

    y_min = v_fov[0] / v_res            # theoretical min y value based on sensor specs
    y_img -= y_min                      # Shift
    y_max = v_fov_total / v_res         # Theoretical max x value after shifting

    y_max += y_fudge                    # Fudge factor if the calculations based on
 

    if val == "reflectance":
        pixel_values = r_lidar
    elif val == "height":
        pixel_values = z_lidar
    else:
        pixel_values = -d_lidar

    new_df = pd.DataFrame({'x' : x_img, 'y' : y_img, 'r' : pixel_values})
    new_df.to_csv(f'{output_lidar_csv_folder_name}/new_pcl_{count}.csv',  index=False)

    # plot the image
    cmap = "jet"            # Color map to use
    dpi = 100               # Image resolution

    fig, ax = plt.subplots(figsize=(x_max/dpi, y_max/dpi), dpi=dpi)
    ax.scatter(x_img,y_img, s=1, c=pixel_values, linewidths=0, alpha=1, cmap=cmap)

    ax.set_facecolor((0, 0, 0))         # Set regions with no points to black
    ax.axis('scaled')                   # {equal, scaled}
    ax.xaxis.set_visible(False)  
    ax.yaxis.set_visible(False)    
    plt.xlim([0, x_max])                # prevent drawing empty space outside of horizontal FOV
    plt.ylim([0, y_max])                # prevent drawing empty space outside of vertical FOV

    if saveto is not None:
        fig.savefig(saveto, dpi=dpi, bbox_inches='tight', pad_inches=0.0)
    else:
        fig.show()


if __name__ == '__main__':

    input_lidar_folder_name = 'Input_lidar'
    output_lidar_csv_folder_name = 'Output_lidar_csv'
    output_lidar_image_folder_name = 'Output_lidar_image'

    HRES = 0.3                      # horizontal resolution (assuming 20Hz setting)
    VRES = 0.3                      # vertical res
    VFOV = (-50.0, 50.0)            # Field of view (-ve, +ve) along vertical axis       # main code (-120, 120)
    Y_FUDGE = 5                     # y fudge factor for velodyne HDL 64E

    count = 1
    max_limit = 3

    while(1):
        df = pd.read_csv(f'{input_lidar_folder_name}/pcl_test_{count}.csv', delimiter=' ')

        x_lidar = df['x'].to_numpy()
        y_lidar = df['y'].to_numpy()
        z_lidar = df['z'].to_numpy()
        r_lidar = df['r'].to_numpy()

        lidar_to_2d_front_view(x_lidar, y_lidar, z_lidar, r_lidar, count, v_res=VRES, h_res=HRES, v_fov=VFOV, val="depth",
                            saveto=f'{output_lidar_image_folder_name}/lidar_{count}.png', y_fudge=Y_FUDGE)
        
        count = count + 1
        if count >= max_limit:
            break