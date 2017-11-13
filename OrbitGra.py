from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# how to take data from sqlite db

# connect to DB
conn = sqlite3.connect('orbit_data.db')
c = conn.cursor()

# select x values and save to x list
c.execute('''SELECT x FROM orbit''')
x = c.fetchall()
# remove tuples from list
x = [i[0] for i in x]

# same thing as above
c.execute('''SELECT y FROM orbit''')
y = c.fetchall()
y = [j[0] for j in y]

c.execute('''SELECT z FROM orbit''')
z = c.fetchall()
z = [k[0] for k in z]

# close connection
conn.close()

X = x[2880:5760]
Y = y[2880:5760]
Z = z[2880:5760]

def randrange(X, Y, Z, vmin, vmax):
    return (vmax - vmin) * np.random.rand(n) + vmin


fig = plt.figure(figsize=(7, 7), dpi=100)


plt.rcParams['toolbar'] = 'None'


ax = fig.add_subplot(111, projection='3d')

ax.disable_mouse_rotation()

for angle in range(0, 360):
    ax.view_init(90, angle)

n = 2880

for c, m, zlow, zhigh in [('r', 'o', -3000, -3000), ('b', '^', -3000, -3000)]:
    xs = X
    ys = Y
    zs = Z
    ax.scatter(xs, ys, zs, c=c, marker=m)

plt.axis('off')

ax.set_facecolor('grey')
ax.set_facecolor((.25,.25,.25))

plt.show()
