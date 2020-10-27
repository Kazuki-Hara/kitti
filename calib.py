import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

points = np.fromfile('000003.bin', dtype=np.float32, count = -1).reshape([-1, 4])
print(points)

ax = plt.axes(projection='3d')
ax.scatter(points[:,0], points[:,1], points[:,2], s = 0.01)
plt.show()