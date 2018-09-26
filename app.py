import random
import tkinter as tk
from math import sin, cos, pi, atan2


class App(tk.Frame):
    """Tkinter frame which contains our other widgets.
    """

    def __init__(self, resolution):
        super().__init__(None)

        # Set the title of the windows.
        self.winfo_toplevel().title('Triangle in circle')
        # Resolution of the frame in pixel.
        self.resolution = resolution
        self.half = resolution / 2
        # Radius of the circle.
        self.r = self.half - 50
        # Iteration count. Default 0.
        self.iter_count = tk.StringVar()
        self.iter_count.set(0)
        # Probabolity calculated from the iterations.
        self.probability = tk.StringVar()
        self.probability.set('-')
        # Result of each iteration.
        self.results = []

        # Add (pack) this instace to its parent.
        self.pack()
        # Init the UI.
        self.create_ui()

    def create_ui(self):
        '''Initialize the user interface.
        '''

        # Start button.
        self.button_start = tk.Button(self, text='Start', command=self.start)
        self.button_start.grid(row=0, column=0)

        # Label which displays how many iteration we've already did.
        self.l_count = tk.Label(self, textvariable=self.iter_count)
        self.l_count.grid(row=0, column=1)

        # Label which displays the probability from the iterations.
        self.l_res = tk.Label(self, textvariable=self.probability)
        self.l_res.grid(row=0, column=2)

        # Canvas for drawing.
        self.canvas = tk.Canvas(self, bg='grey', height=self.resolution, width=self.resolution)
        self.canvas.grid(row=1, column=0, columnspan=3)

        # Basic shapes.
        self.circle = self.canvas.create_oval(50, 50, self.resolution - 50, self.resolution - 50)
        self.circle_mid = self.canvas.create_oval(self.half-2, self.half-2, self.half+2, self.half+2, fill='black')

    def start(self):
        """Start the iteration.
        """

        self.break_iteration = False
        self.button_start.config(text='Pause', command=self.stop)
        self.iterate()

    def stop(self):
        """Stop the iteration.
        """

        self.break_iteration = True
        self.button_start.config(text='Continue', command=self.start)

    def iterate(self):
        """Calculate and draw the results.
        """

        self.canvas.delete('all')
        # Basic shapes. I found better in performance if we clear the whole canvas and redraw this two circle,
        # than store each object and delete them one by one.
        self.circle = self.canvas.create_oval(50, 50, self.resolution - 50, self.resolution - 50)
        self.circle_mid = self.canvas.create_oval(self.half-2, self.half-2, self.half+2, self.half+2, fill='black')

        # Basic shapes.
        self.canvas.create_oval(50, 50, self.resolution - 50, self.resolution - 50)
        self.canvas.create_oval(self.half-2, self.half-2, self.half+2, self.half+2, fill='black')

        points = []

        for i in range(3):
            r = random.randint(0, 360)
            px = self.half + sin(r*2*pi/360) * self.r
            py = self.half + cos(r*2*pi/360) * self.r

            points.append((px, py))

            if i < 2:
                self.canvas.create_oval(px-4, py-4, px+4, py+4, fill='red')
            else:
                self.canvas.create_oval(px-4, py-4, px+4, py+4, fill='green')

        px1 = points[0][0] + 2 * abs(points[0][0]-self.half) if points[0][0] < self.half else points[0][0] - 2 * abs(points[0][0]-self.half)
        py1 = points[0][1] + 2 * abs(points[0][1]-self.half) if points[0][1] < self.half else points[0][1] - 2 * abs(points[0][1]-self.half)

        px2 = points[1][0] + 2 * abs(points[1][0]-self.half) if points[1][0] < self.half else points[1][0] - 2 * abs(points[1][0]-self.half)
        py2 = points[1][1] + 2 * abs(points[1][1]-self.half) if points[1][1] < self.half else points[1][1] - 2 * abs(points[1][1]-self.half)

        self.canvas.create_oval(px1-2, py1-2, px1+2, py1+2, fill='blue')
        self.canvas.create_oval(px2-2, py2-2, px2+2, py2+2, fill='blue')

        p3x = points[2][0]
        p3y = points[2][1]

        py1 = (py1-self.half) * -1
        px1 = (px1-self.half)
        py2 = (py2-self.half) * -1
        px2 = (px2-self.half)
        p3y = (p3y-self.half) * -1
        p3x = (p3x-self.half)

        p1a = atan2(py1, px1) * (180/pi)

        p2a = atan2(py2, px2) * (180/pi)

        p3a = atan2(p3y, p3x) * (180/pi)

        ps = sorted([p1a, p2a])

        if abs(p1a - p2a) < 180:
            if ps[0] < p3a and p3a < ps[1]:
                check = True
            else:
                check = False
        else:
            if ps[0] < p3a and p3a < ps[1]:
                check = False
            else:
                check = True


        if check:
            self.canvas.create_polygon(points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1], fill='green')
        else:
            self.canvas.create_polygon(points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1], fill='red')



        self.results.append(check)

        results_count = len(self.results)

        self.iter_count.set(results_count)
        self.probability.set(round(self.results.count(True)/results_count, 3))

        if not self.break_iteration: self.after(100, self.iterate)


if __name__ == '__main__':
    # Our tkinkter app.
    app = App(600)
    # and start it.
    app.mainloop()