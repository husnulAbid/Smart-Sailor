import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_lidar_2d_with_image(lidar_file, image_file):
    df = pd.read_csv(lidar_file, delimiter=',')
    image_1 = plt.imread(image_file)

    df['x'] = df['x'] - 400
    df = df[(df['x'] >= 0) & (df['x'] <= 460)]
    df['x'] = df['x'] * (720.0/460.0)

    df['y'] = 900-df['y']

    plt.imshow(image_1)
    print(image_1.shape)

    plt.scatter(df['x'], df['y'], s=1, c=df['r'], linewidths=0, alpha=1, cmap='jet')
    plt.show()


if __name__ == '__main__':
    file_number = 1

    lidar_point_file_name = f'Input_2d_lidar_points/new_pcl_{file_number}.csv'
    image_file_name = f'Input_image/{file_number}.png'

    plot_lidar_2d_with_image(lidar_point_file_name, image_file_name)




    # x_points = df['x'].to_numpy()
    # y_points = df['y'].to_numpy()
    # r_point = df['r'].to_numpy()

    # y_points = 600-y_points
    # x_points = (x_points - 460)
    # x_points = x_points[np.where(x_points >= 0)]
    # x need to match between 0 to 720
    # df['x'] = df['x'] - 400                         # Lidar covers from 440 to 900
    # df = df[(df['x'] >= 0) & (df['x'] <= 460)]
    # df['x'] = df['x'] * (720.0/460.0)

    # # y need to match between 0 to 480
    # df['y'] = 900-df['y']

    # image_1 = plt.imread(f'Input_image/{photo_number}.png')
    # plt.imshow(image_1)

    # plt.scatter(df['x'], df['y'], s=1, c=df['r'], linewidths=0, alpha=1, cmap='jet')
    # plt.show()
    
