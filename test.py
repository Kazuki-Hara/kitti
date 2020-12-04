import numpy as np
import matplotlib.pyplot as plt
from kitti_utils.calibration import Calibration
from PIL import Image
from mayavi import mlab
<<<<<<< HEAD:test.py
import torch
import math
=======
import math


object_class_list = [
    'Car', 'Cyclist', 'Pedestrian'
]

>>>>>>> b91b39d927c44f19c10d456ceab304599d8c3950:calib.py

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
    

<<<<<<< HEAD:test.py
    for data in label_data:
        object_class = data[0]
        if object_class == 'Pedestrian' or object_class == 'Cyclist':
            flag = check_object_in_range(data)
            if not flag:
                continue
            
=======
    for i, data in enumerate(label_data):
>>>>>>> b91b39d927c44f19c10d456ceab304599d8c3950:calib.py
        length = float(data[10])
        height = float(data[8])
        width = float(data[9])
        
        x = float(data[13])
        y = float(data[11])
        z = float(data[12])
        pi = float(data[14])
<<<<<<< HEAD:test.py
        y *= -1
        z *= -1

=======

        y *= -1
        z *= -1
        #print(x, y, z)
>>>>>>> b91b39d927c44f19c10d456ceab304599d8c3950:calib.py
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
<<<<<<< HEAD:test.py
=======
        print(vertex.shape)
        '''
        points_in_3dbox = np.array([point for point in points if check_point_in_3dbox(point, vertex)])
        if len(points_in_3dbox) == 0:
            continue
        color = points_in_3dbox[:, 2]

        mlab.points3d(points_in_3dbox[:, 0], points_in_3dbox[:, 1], points_in_3dbox[:, 2], color, color=None,
           
                  mode='point', colormap='Oranges', scale_factor=0.3, figure=fig)
        '''
>>>>>>> b91b39d927c44f19c10d456ceab304599d8c3950:calib.py

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


<<<<<<< HEAD:test.py
def point_in_label(point, vertex):
    x = point[0]
    y = point[1]
    z = point[2]
    res = vertex[0, 0] <= x <= vertex[1, 0] and vertex[0, 1] <= y <= vertex[2, 1] and vertex[0, 2] <= z <= vertex[4, 2]
    return res


=======
>>>>>>> b91b39d927c44f19c10d456ceab304599d8c3950:calib.py
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

<<<<<<< HEAD:test.py
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
=======

def check_point_in_3dbox(point, vertex_list):
    vertex_list = vertex_list[:4]
    vertex_list = np.append(vertex_list, vertex_list[0]).reshape(5, 3)
    print(vertex_list)

    outer_count = 0

    for i in range(4):
        x1 = vertex_list[i, 0]
        x2 = vertex_list[i + 1, 0]
        y1 = vertex_list[i, 1]
        y2 = vertex_list[i + 1, 1]
        px = point[0]
        py = point[1]
        outer = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
        if outer >= 0:
            outer_count += 1
    if outer_count == 0 or outer_count == 4:
        return True
    else:
        return False
    


def save_image_in_bbox(file_name):
    label_data = get_label_info(file_name)
    image_path = 'image2/' + file_name + '.png'
    image = np.array(Image.open(image_path))
    for i, label in enumerate(label_data):
        minx = int(float(label[4]))
        miny = int(float(label[5]))
        maxx = int(float(label[6]))
        maxy = int(float(label[7]))

        occlusion = int(label[2])
        difficulty = caluc_difficluty(maxy, miny, occlusion)

        image = draw_rectangle(image, minx, miny, maxx, maxy, difficulty)
        
    
    Image.fromarray(image).save('image_in_bbox/test_' + file_name + '.png')


def draw_rectangle(image, minx, miny, maxx, maxy, difficulty):
    if difficulty == 'easy':
        color = (0,0,255)
    elif difficulty == 'normal':
        color = (255,255,0)
    elif difficulty == 'hard':
        color = (255,0,0)
    else:
        return image
    image[miny:maxy, minx] = color
    image[miny:maxy, maxx] = color
    image[miny, minx:maxx] = color
    image[maxy, minx:maxx] = color
    return image


def caluc_difficluty(maxy, miny, occlusion):
    height = maxy - miny
    if height > 40 and occlusion == 0:
        difficulty = 'easy'
    elif height > 25 and occlusion <= 1:
        difficulty = 'normal'
    elif height > 25 and occlusion <= 2:
        difficulty = 'hard'
    else:
        difficulty = 'none'
    return difficulty


def get_label_info(file_name):
    label_file_path = 'label/' + file_name + '.txt'
    
    with open(label_file_path, 'r') as f:
        lines = f.readlines()
    label_data = [line.strip().split(' ') for line in lines]
    label_data = [data for data in label_data if data[0] in object_class_list]
    if len(label_data) == 0:
        return False
    else:
        return label_data


        

if __name__ == "__main__":
    '''
    with open('label/002155.txt', 'r') as f:
        lines = f.readlines()
    label_data = [line.strip().split(' ') for line in lines if line[0] != 'DontCare']
    label_data = [data for data in label_data if data[0] != 'DontCare']
    #print(label_data)
    points = np.fromfile('velodyne/002155.bin', dtype=np.float32, count = -1).reshape([-1, 4])
>>>>>>> b91b39d927c44f19c10d456ceab304599d8c3950:calib.py
    draw_point_cloud(points, label_data)
    '''
    save_image_in_bbox('005541')


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