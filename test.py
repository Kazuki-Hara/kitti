import numpy as np
import matplotlib.pyplot as plt
from kitti_utils.calibration import Calibration
from PIL import Image
from mayavi import mlab
import torch
import math

def draw_point_cloud(points, label_data, colors=None):
    '''Draw draw point cloud.

    Args:
      pc: (np.array) point cloud, sized (n,3) of XYZ.
      boxes: (list(np.array)) list of 3D bounding boxes, each sized [8,3].
      colors: (list(tuple)) list of RGB colors.
    '''

    fig = mlab.figure(figure=None, bgcolor=(0, 0, 0),
                      fgcolor=None, engine=None, size=(1600, 1000))
    color = points[:, 2]
    
    mlab.points3d(points[:, 0], points[:, 1], points[:, 2], color, color=None,
                  mode='point', colormap='Oranges', scale_factor=0.3, figure=fig)
    

    for data in label_data:
        object_class = data[0]
        if object_class == 'Pedestrian' or object_class == 'Cyclist':
            flag = check_object_in_range(data)
            if not flag:
                continue
            
        length = float(data[10])
        height = float(data[8])
        width = float(data[9])
        
        x = float(data[13])
        y = float(data[11])
        z = float(data[12])
        pi = float(data[14])
        y *= -1
        z *= -1

        vertex = np.array([
            [x - length / 2, y-width/2, z],
            [x + length / 2, y-width/2, z],
            [x + length / 2, y+width/2, z],
            [x - length / 2, y+width/2, z],
            [x - length / 2, y-width/2, z+height],
            [x + length / 2, y-width/2, z+height],
            [x + length / 2, y+width/2, z+height],
            [x - length / 2, y+width/2, z+height],
        ])
        vertex = rotation(x, y, z, vertex, pi)

        mlab.points3d(vertex[:, 0], vertex[:, 1], vertex[:, 2], color=(0, 1, 1), mode='sphere', scale_factor=0.2)
        '''
        points_in_object = np.array([point for point in points if point_in_label(point, vertex)], dtype=np.float32)
        #print(points_in_object.shape)
        #print(points_in_object)
        #mlab.points3d(vertex[:, 0], vertex[:, 1], vertex[:, 2], color=(0, 1, 1), mode='sphere', scale_factor=0.2)
        color = points_in_object[:, 2]
        mlab.points3d(points_in_object[:, 0], points_in_object[:, 1], points_in_object[:, 2], color, color=None,
                  mode='point', colormap='Oranges', scale_factor=0.3, figure=fig)
        '''


    # draw origin
    mlab.points3d(0, 0, 0, color=(1, 1, 1), mode='sphere', scale_factor=0.2)
    mlab.view(azimuth=180, elevation=70, focalpoint=[
              12.0909996, -1.04700089, -2.03249991], distance=62.0, figure=fig)

    mlab.show()


def point_in_label(point, vertex):
    x = point[0]
    y = point[1]
    z = point[2]
    res = vertex[0, 0] <= x <= vertex[1, 0] and vertex[0, 1] <= y <= vertex[2, 1] and vertex[0, 2] <= z <= vertex[4, 2]
    return res


def rotation(x, y, z, vertex_list, rad):
    #rad = deg * np.pi / 180
    rad = -math.pi / 2 - rad
    rot = np.array([[np.cos(rad), -np.sin(rad)],
                    [np.sin(rad), np.cos(rad)]])
    for vertex in vertex_list:
        vertex_x = vertex[0] - x
        vertex_y = vertex[1] - y
        rotated_vertex = np.dot(rot, np.array([vertex_x, vertex_y]))
        vertex[0] = rotated_vertex[0] + x
        vertex[1] = rotated_vertex[1] + y
    
    return vertex_list

def check_object_in_range(label):
    x = float(label[13])
    y = float(label[11])
    if 0 <= x <= 48 and -20 <= y <= 20:
        return True
    else:
        return False


if __name__ == "__main__":
    file_name = '007347'
    with open('label/' + file_name + '.txt', 'r') as f:
        lines = f.readlines()
    label_data = [line.strip().split(' ') for line in lines if line[0] != 'DontCare']
    label_data = [data for data in label_data if data[0] != 'DontCare']
    print(label_data)
    points = np.fromfile('velodyne/' + file_name + '.bin', dtype=np.float32, count = -1).reshape([-1, 4])
    draw_point_cloud(points, label_data)



    '''
    png_img = np.array(Image.open('image2/000003.png'))
    HEIGHT = png_img.shape[0]
    WIDTH = png_img.shape[1]
    #print(HEIGHT, WIDTH)


    calibration = Calibration('calib/000003.txt')
    points = np.fromfile('velodyne/000003.bin', dtype=np.float32, count = -1).reshape([-1, 4])
    print(points.shape)
    cam0 = calibration.project_velo_to_ref(points)

    cam2 = calibration.project_ref_to_cam(cam0)
    #print(cam0)
    #print(cam2)
    img = calibration.project_cam_to_img(cam2)
    #print(img)
    #draw_point_cloud(points)
    #print(img.shape)
    points_in_pic = []
    for i, point in enumerate(points):
        x = int(img[i][0])
        y = int(img[i][1])
        #print(x, y)
        if 0<= x < WIDTH and 0<= y < HEIGHT and point[0] >= 0:
            points_in_pic.append(point)
        #else:
        #    points_in_pic.append(np.zeros(3))
    points_in_pic_array = np.stack(points_in_pic)
    '''