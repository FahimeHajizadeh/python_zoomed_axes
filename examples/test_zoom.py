import numpy as np
import matplotlib.pyplot as plt
import zoomtool
 
from zoomtool import zoom_window

# Desired signals
x = np.linspace(0, 10, 5000)
y1 = np.sin(8 * x)
y2 = np.sin(8 * x + 0.1) * 0.97   # slightly shifted & scaled → to show error

# Compute relative L2 error
num = np.linalg.norm(y1 - y2, 2)
den = np.linalg.norm(y1, 2)
rel_error = num / den

print(f"Relative L2 Error Norm = {rel_error:.6f}")

# Plot
fig, ax = plt.subplots()
ax.plot(x, y1, 'b', linewidth=1.2, label="Signal 1")
ax.plot(x, y2, 'r--', linewidth=1.2, label="Signal 2")
ax.legend()
ax.set_title("Two Superimposed Waveforms")

# dz = zoom_window(ax)
dz = zoomtool.zoom_window(ax)

plt.show()