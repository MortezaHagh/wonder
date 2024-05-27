import tkinter as tk
from PIL import Image, ImageTk
import json

class PointVisualizerApp:
    def __init__(self, root, point_sets, json_files, image_file, resolution):
        self.root = root
        self.point_sets = point_sets
        self.json_files = json_files
        self.image_file = image_file
        self.resolution = int(resolution)  # Convert resolution to an integer
        self.r = 100  # Set radius to 100
        self.load_image()
        self.create_canvas()

        self.colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']  # You can add more colors if needed
        self.draw_points()
        self.draw_grid()

        self.canvas.bind("<B1-Motion>", self.move_point)



    def load_image(self):
        with open(self.image_file, 'rb') as f:
            pgm = f.read().decode()

        # Split lines and remove comments
        lines = pgm.split('\n')
        lines = [line for line in lines if not line.startswith('#')]

        # Extract width, height, and maximum gray value from PGM header
        self.img_width, self.img_height = map(int, lines[1].split())

        # Calculate canvas size based on image size and resolution
        self.canvas_width = min(int(self.img_width * self.resolution), 1000)  # Limit canvas width to 1000 pixels
        self.canvas_height = min(int(self.img_height * self.resolution), 1000)  # Limit canvas height to 1000 pixels

        # Create image object
        img = Image.new('L', (self.img_width, self.img_height))

        # Extract image data and convert to PNG format
        data = ' '.join(lines[3:])
        pixels = [int(pixel) for pixel in data.split()]
        img.putdata(pixels)

        # Resize image to fit canvas
        img = img.resize((self.canvas_width, self.canvas_height))

        # Convert image to PhotoImage
        self.img = ImageTk.PhotoImage(img)


    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

    def draw_points(self):
        for idx, point_set in enumerate(self.point_sets):
            color = self.colors[idx % len(self.colors)]
            for point in point_set:
                x, y = point['x'], point['y']
                # Scale the coordinates based on the resolution and canvas size
                x_px = int(x * self.resolution)
                y_px = int(y * self.resolution)
                # Offset the coordinates to match the image position on the canvas
                x_offset = (self.canvas_width - self.img_width * self.resolution) // 2
                y_offset = (self.canvas_height - self.img_height * self.resolution) // 2
                # Draw the point on the canvas
                self.canvas.create_oval(x_px - self.r + x_offset, y_px - self.r + y_offset, 
                                        x_px + self.r + x_offset, y_px + self.r + y_offset, fill=color)



    def move_point(self, event):
        x, y = event.x, event.y
        self.canvas.delete("all")
        for point_set, json_file in zip(self.point_sets, self.json_files):
            for point in point_set:
                px, py = point['x'], point['y']
                if abs(px - x) <= self.r and abs(py - y) <= self.r:
                    point['x'] = x / self.resolution
                    point['y'] = y / self.resolution
                    self.save_to_json(point_set, json_file)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        self.draw_points()
        self.draw_grid()

    def draw_grid(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Draw the image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

        # Draw horizontal grid lines and coordinate labels
        for i in range(0, self.canvas_height, self.resolution):
            self.canvas.create_line(0, i, self.canvas_width, i, fill="gray")
            self.canvas.create_text(10, i, text=str(i // self.resolution), anchor=tk.W, fill="black")

        # Draw vertical grid lines and coordinate labels
        for j in range(0, self.canvas_width, self.resolution):
            self.canvas.create_line(j, 0, j, self.canvas_height, fill="gray")
            self.canvas.create_text(j, self.canvas_height - 10, text=str(j // self.resolution), anchor=tk.N, fill="black")

        # Draw X-axis
        self.canvas.create_line(0, self.canvas_height // 2, self.canvas_width, self.canvas_height // 2, fill="black", width=2)

        # Draw Y-axis
        self.canvas.create_line(self.canvas_width // 2, 0, self.canvas_width // 2, self.canvas_height, fill="black", width=2)

        # Draw axis labels
        x_label = "X"
        y_label = "Y"
        x_label_x = self.canvas_width - 20
        x_label_y = self.canvas_height // 2 + 20
        y_label_x = self.canvas_width // 2 - 20
        y_label_y = 10
        self.canvas.create_text(x_label_x, x_label_y, text=x_label, anchor=tk.CENTER, fill="black")
        self.canvas.create_text(y_label_x, y_label_y, text=y_label, anchor=tk.CENTER, fill="black")




    def save_to_json(self, point_set, json_file):
        with open(json_file, 'w') as file:
            json.dump(point_set, file, indent=4)

def main():
    # Configuration
    image_file = 'map.pgm'
    resolution = 1 / 0.05  # Pixel per meter

    # Read points from JSON
    json_files = ['points1.json', 'points2.json']  # Add more JSON files as needed
    point_sets = []
    for json_file in json_files:
        with open(json_file, 'r') as file:
            points = json.load(file)
            point_sets.append(points)

    # Create GUI window
    root = tk.Tk()
    root.title("Point Visualizer")

    # Create and run the application
    app = PointVisualizerApp(root, point_sets, json_files, image_file, resolution)
    root.mainloop()

if __name__ == "__main__":
    main()
