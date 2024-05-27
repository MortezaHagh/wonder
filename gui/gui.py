import tkinter as tk
import json
import matplotlib.pyplot as plt

class PointVisualizerApp:
    def __init__(self, root, points, json_file):
        self.root = root
        self.points = points
        self.json_file = json_file

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.draw_points()

        self.canvas.bind("<B1-Motion>", self.move_point)

    def draw_points(self):
        for point in self.points:
            x, y = point['x'], point['y']
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='blue')

    def move_point(self, event):
        x, y = event.x, event.y
        self.canvas.delete("all")
        for point in self.points:
            px, py = point['x'], point['y']
            if abs(px - x) <= 3 and abs(py - y) <= 3:
                point['x'], point['y'] = x, y
        self.draw_points()
        self.save_to_json()

    def save_to_json(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.points, file, indent=4)

def main():
    # Read points from JSON
    json_file = 'points.json'
    with open(json_file, 'r') as file:
        points = json.load(file)

    # Create GUI window
    root = tk.Tk()
    root.title("Point Visualizer")

    # Create and run the application
    app = PointVisualizerApp(root, points, json_file)
    root.mainloop()

if __name__ == "__main__":
    main()
