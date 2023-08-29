from numpy import load
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
file0 = 'D:\\output\\10fish_group\\10fish_group_15minacc_2023-08-25-151156-0000_fish0.npz'
file1 = 'D:\\output\\10fish_group\\10fish_group_15minacc_2023-08-25-151156-0000_fish1.npz'
file2 = 'D:\\output\\10fish_group\\10fish_group_15minacc_2023-08-25-151156-0000_fish2.npz'
file3 = 'D:\\output\\10fish_group\\10fish_group_15minacc_2023-08-25-151156-0000_fish3.npz'
file4 = 'D:\\output\\10fish_group\\10fish_group_15minacc_2023-08-25-151156-0000_fish4.npz'
file5 = 'D:\\output\\10fish_group\\10fish_group_15minacc_2023-08-25-151156-0000_fish5.npz'
file6 = 'D:\\output\\10fish_group\\10fish_group_15minacc_2023-08-25-151156-0000_fish6.npz'
file7 = 'D:\\output\\10fish_group\\10fish_group_15minacc_2023-08-25-151156-0000_fish7.npz'
file8 = 'D:\\output\\10fish_group\\10fish_group_15minacc_2023-08-25-151156-0000_fish8.npz'
file9 = 'D:\\output\\10fish_group\\10fish_group_15minacc_2023-08-25-151156-0000_fish9.npz'

global length
length = 9
def open_file(file_name):
    data = load(file_name)
    lst = data.files
    #print(lst)
    xpos=[]
    ypos=[]
    vx=[]
    vy = []
    for item in lst:
        print(item)
        #print(data[item])
        if item == 'X':
            for pos in data[item]:
                #print(pos)
                xpos.append(pos)
        if item == 'Y':
            for pos in data[item]:
                #print(pos)
                ypos.append(pos)
            
        if item == 'VX':
            for pos in data[item]:
                #print(pos)
                vx.append(pos)
        if item == 'VY':
            for pos in data[item]:
                #print(pos)
                vy.append(pos)
    positions=np.stack((xpos, ypos), axis=-1)
    directions = np.stack((vx, vy), axis = -1)
    norms = np.linalg.norm(directions,axis=1)
    norms[norms == 0] = 1
    for i in range(len(directions)):
        directions[i]=directions[i]/norms[i]
    return positions, directions
positions0, directions0 = open_file(file0)
positions1, directions1 = open_file(file1)
positions2, directions2 = open_file(file2)
positions3, directions3 = open_file(file3)
positions4, directions4 = open_file(file4)
positions5, directions5 = open_file(file5)
positions6, directions6 = open_file(file6)
positions7, directions7 = open_file(file7)
positions8, directions8 = open_file(file8)
positions9, directions9 = open_file(file9)
positions=[positions0, positions1, positions2, positions3, positions4, positions5, positions6, positions7, positions8, positions9]
directions=[directions0, directions1, directions2, directions3, directions4, directions4, directions5, directions6, directions7, directions8, directions9]



def plot_quiver(positions, directions, sc=1.0, ratio=1.0, title=None):
    """
    Plot a quiver plot of positions and directions.

    Parameters:
        positions (numpy.ndarray): An array of shape (N, 2) containing x and y positions.
        directions (numpy.ndarray): An array of shape (N, 2) containing x and y directions.
        scale (float, optional): Scaling factor for the arrow length. Default is 1.0.
        title (str, optional): Title of the plot. Default is None.
    """
    fig, ax = plt.subplots()
    for i in range(len(positions[0])):
        ax.clear()
        circle = Circle([length/2,length/2], length/2, edgecolor='b', facecolor='none')
        plt.gca().add_patch(circle)
        ax.quiver(ratio*positions[0][i, 0], ratio*positions[0][i, 1], sc*directions[0][i, 0], sc*directions[0][i, 1], scale=2)
        ax.quiver(ratio*positions[1][i, 0], ratio*positions[1][i, 1], sc*directions[1][i, 0], sc*directions[1][i, 1], scale=2)
        ax.quiver(ratio*positions[2][i, 0], ratio*positions[2][i, 1], sc*directions[2][i, 0], sc*directions[2][i, 1], scale=2)
        ax.quiver(ratio*positions[3][i, 0], ratio*positions[3][i, 1], sc*directions[3][i, 0], sc*directions[3][i, 1], scale=2)
        ax.quiver(ratio*positions[4][i, 0], ratio*positions[4][i, 1], sc*directions[4][i, 0], sc*directions[4][i, 1], scale=2)
        ax.quiver(ratio*positions[5][i, 0], ratio*positions[5][i, 1], sc*directions[5][i, 0], sc*directions[5][i, 1], scale=2)
        ax.quiver(ratio*positions[6][i, 0], ratio*positions[6][i, 1], sc*directions[6][i, 0], sc*directions[6][i, 1], scale=2)
        ax.quiver(ratio*positions[7][i, 0], ratio*positions[7][i, 1], sc*directions[7][i, 0], sc*directions[7][i, 1], scale=2)
        ax.quiver(ratio*positions[8][i, 0], ratio*positions[8][i, 1], sc*directions[8][i, 0], sc*directions[8][i, 1], scale=2)
        ax.quiver(ratio*positions[9][i, 0], ratio*positions[9][i, 1], sc*directions[9][i, 0], sc*directions[9][i, 1], scale=2)

        ax.set_aspect('equal')
        ax.set_xlim((0,length))
        ax.set_ylim((0,length))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        if title:
            ax.set_title(title)
        plt.pause(0.0001)
        

    plt.show()
len_ratio = length/30
plot_quiver(positions, directions, sc=0.1, ratio = len_ratio, title="Quiver Plot Example")
