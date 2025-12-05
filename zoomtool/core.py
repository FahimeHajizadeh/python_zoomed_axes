import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

class DraggableZoom:
    """
    Add a draggable & resizable zoom window to any Matplotlib axes.

    Usage:
        from zoomtool import zoom_window
        zoom_window(ax)
    """
    def __init__(self, ax, zoom_width=0.15, zoom_height=0.15, inset_size="30%"):
        self.ax = ax
        self.fig = ax.figure

        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        w = (x1 - x0) * zoom_width
        h = (y1 - y0) * zoom_height

        # Main draggable rectangle
        self.rect = Rectangle((x0 + w, y0 + h), w, h,
                              fill=False, edgecolor='red', linewidth=1.5)
        ax.add_patch(self.rect)

        # Inset (zoom window)
        self.inset = inset_axes(ax, width=inset_size, height=inset_size, loc="upper right")
        self.update_inset()

        # State variables
        self.press = None
        self.resizing = False
        self.resize_margin = 0.03  # corner sensitivity

        # Event connections
        self.cid_press = self.fig.canvas.mpl_connect("button_press_event", self.on_press)
        self.cid_release = self.fig.canvas.mpl_connect("button_release_event", self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

    # ------------------------------------------------------------

    def in_resize_zone(self, event):
        """Checks if user clicked close to bottom-right corner."""
        x, y = self.rect.get_xy()
        w, h = self.rect.get_width(), self.rect.get_height()
        xr, yr = x + w, y + h
        tol_x = w * self.resize_margin
        tol_y = h * self.resize_margin
        return abs(event.xdata - xr) < tol_x and abs(event.ydata - yr) < tol_y

    # ------------------------------------------------------------

    def on_press(self, event):
        if event.inaxes != self.ax:
            return

        # Check for resize
        if self.in_resize_zone(event):
            self.resizing = True
            self.press = (self.rect.get_width(), self.rect.get_height(),
                          event.xdata, event.ydata)
            return

        # Check for dragging
        contains, _ = self.rect.contains(event)
        if contains:
            self.press = (self.rect.xy, event.xdata, event.ydata)

    # ------------------------------------------------------------

    def on_release(self, event):
        self.press = None
        self.resizing = False
        self.update_inset()
        self.fig.canvas.draw_idle()

    # ------------------------------------------------------------

    def on_motion(self, event):
        if self.press is None or event.inaxes != self.ax:
            return

        # Resizing
        if self.resizing:
            w0, h0, x0, y0 = self.press
            self.rect.set_width(w0 + (event.xdata - x0))
            self.rect.set_height(h0 + (event.ydata - y0))
            self.update_inset()
            self.fig.canvas.draw_idle()
            return

        # Dragging
        (x0, y0), xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.rect.set_xy((x0 + dx, y0 + dy))
        self.update_inset()
        self.fig.canvas.draw_idle()

    # ------------------------------------------------------------

    def update_inset(self):
        """Redraw the zoom window."""
        x, y = self.rect.get_xy()
        w, h = self.rect.get_width(), self.rect.get_height()

        self.inset.clear()

        for line in self.ax.get_lines():
            self.inset.plot(line.get_xdata(), line.get_ydata(),
                            color=line.get_color(),
                            linewidth=line.get_linewidth())

        self.inset.set_xlim(x, x + w)
        self.inset.set_ylim(y, y + h)
        self.inset.set_title("Zoom", fontsize=8)

# ============================================================
# PUBLIC FUNCTION
# ============================================================

def zoom_window(ax, zoom_width=0.15, zoom_height=0.15, inset_size="30%"):
    """
    Simple API: Add zoom window to any axes.
    
    Example:
        fig, ax = plt.subplots()
        ax.plot(x, y)
        zoom_window(ax)
    """
    return DraggableZoom(ax, zoom_width, zoom_height, inset_size)
