from backend import backAlgs
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

X_io, Y_io, Z_io, X_eur, Y_eur, Z_eur, gd_list = backAlgs.pull_sqldata()

X_io = np.array(X_io, dtype='float64')
Y_io = np.array(Y_io, dtype='float64')
Z_io = np.array(Z_io, dtype='float64')
X_eur = np.array(X_eur, dtype='float64')
Y_eur = np.array(Y_eur, dtype='float64')
Z_eur = np.array(Z_eur, dtype='float64')

fig = plt.figure()
fig.patch.set_antialiased(True)
fig.patch.set_facecolor('black')

# First plot with orbit line
ax = fig.add_subplot(121, projection='3d')
ax.patch.set_facecolor('grey')
ax.plot([0], [0], [0], marker='o', markersize=65, color="orange")
ax.plot(X_io[0:2550], Y_io[0:2550], Z_io[0:2550])
ax.plot(X_eur[0:5200], Y_eur[0:5200], Z_eur[0:5200])
ax.view_init(-3, 10)
ax.set_xlim(-.0035, .0035)
ax.set_ylim(-.0035, .0035)
ax.set_zlim(-.015, .015)
ax.axis('on')

# Second plot with single point at May 24th, 2017 01:00:00 UTC
ax = fig.add_subplot(122, projection='3d')
ax.patch.set_facecolor('grey')
ax.plot([0], [0], [0], marker='o', markersize=65, color="orange")
ax.scatter(X_io[0], Y_io[0], Z_io[0], marker='o', color="blue")
ax.scatter(X_eur[0], Y_eur[0], Z_eur[0], marker='o', color="orange")
ax.view_init(-3, 10)
ax.set_xlim(-.0035, .0035)
ax.set_ylim(-.0035, .0035)
ax.set_zlim(-.015, .015)
ax.axis('on')

fig.tight_layout()
plt.show()
