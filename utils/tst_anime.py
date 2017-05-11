import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def init():
    #l1, = plt.plot([], [], 'r*-')
    #l2, = plt.plot([], [], 'b*-')
    #l3, = plt.plot([], [], 'g*-')

    return l1, l2, l3

def update_line(num):
    #Setup some dummy data based on num
    x = np.linspace(0, 2, 100)

    #Some if then else condition to decide which line to update
    if num%3:
        y1 = np.sin(2 * np.pi * (x - 0.01 * num))
        l1.set_data(x, y1)
    elif num%2:
        y2 = np.sin(2 * np.pi * (x - 0.01 * num*0.2))
        l2.set_data(x, y2)
    else:
        y3 = np.sin(2 * np.pi * (x - 0.01 * num*0.3))
        l3.set_data(x,y3)

    return l1, l2, l3

#setup figure
fig1 = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))

#Setup three different line objects
l1, = plt.plot([], [], 'r*-')
l2, = plt.plot([], [], 'b*-')
l3, = plt.plot([], [], 'g*-')

#Animate calls update line with num incremented by one each time
line_ani = animation.FuncAnimation(fig1, update_line, init_func=init, interval=50, blit=True)

plt.show()
