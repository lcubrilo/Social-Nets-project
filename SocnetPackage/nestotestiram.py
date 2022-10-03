fig, axs = plt.subplots(2, 2, constrained_layout = True)
y_axis = [22, 4, 51, 6, 73, 72, 101, 69]

n = len(y_axis)
for i in list(range(n-1, 0, -1)):
    y_axis[i-1] += y_axis[i]

print(y_axis)
ax.scatter(x_axis, y_axis)