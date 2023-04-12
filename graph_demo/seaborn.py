import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Create sample data
x1 = [0, 1, 2, 3]
y1 = [0, 1, 2, 3]
z1 = [0, 1, 2, 3]
text1 = 'This is the first sentence.'

x2 = [3, 4, 5, 6]
y2 = [3, 4, 5, 6]
z2 = [3, 4, 5, 6]
text2 = 'This is the second sentence.'

x3 = [6, 7, 1, 9]
y3 = [6, 7, 1, 9]
z3 = [6, 7, 1, 9]
text3 = 'This is the third sentence.'

# Create a 3D figure
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Hide the grid and axis
ax.grid(False)
ax.set_axis_off()

# Define the coordinates for each box
box_coords = np.array([
    [x1[-1], y1[-1], z1[-1]],
    [x2[0], y2[0], z2[0]],
    [x3[0], y3[0], z3[0]]
])

# Define the text for each box
box_text = [
    text1,
    text2,
    text3
]

# Define the connections between the boxes
box_connections = np.array([
    [0, 1],
    [1, 2]
])

# Create a list to store the boxes and lines
box_visuals = []
line_visuals = []

# Create a box for each set of coordinates
for i, coords in enumerate(box_coords):
    box = ax.scatter(coords[0], coords[1], coords[2], s=500, marker='s', color='white', edgecolors='black', picker=True)
    box_text_visual = ax.text(coords[0], coords[1], coords[2], box_text[i], fontsize=20, ha='center', va='center', color='black')
    box_visuals.append(box)
    box_visuals.append(box_text_visual)

# Create a line for each connection
for i, conn in enumerate(box_connections):
    start = box_coords[conn[0]]
    end = box_coords[conn[1]]
    line = ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], linewidth=5, color='blue')
    line_visuals.append(line)

# Function to handle box selection
def on_pick(event):
    box_index = event.ind[0]
    box = box_visuals[box_index*2]
    box.set_color('red')
    plt.draw()

# Bind the function to the pick event
fig.canvas.mpl_connect('pick_event', on_pick)
# Show the figure
plt.show()