import tkinter as tk
from tkinter import messagebox
import random
import time
import json
from datetime import datetime

class Shape:
    def __init__(self, canvas, shape_type, color, x, y, size):
        self.canvas = canvas
        self.shape_type = shape_type
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.shape_id = self.draw()
        self.creation_time = time.time()

    def draw(self):
        if self.shape_type == "square":
            return self.canvas.create_rectangle(
                self.x - self.size,
                self.y - self.size,
                self.x + self.size,
                self.y + self.size,
                fill=self.color,
                tags="shape"
            )
        elif self.shape_type == "circle":
            return self.canvas.create_oval(
                self.x - self.size,
                self.y - self.size,
                self.x + self.size,
                self.y + self.size,
                fill=self.color,
                tags="shape"
            )
        else:  # triangle
            points = [
                self.x, self.y - self.size,
                self.x - self.size, self.y + self.size,
                self.x + self.size, self.y + self.size
            ]
            return self.canvas.create_polygon(points, fill=self.color, tags="shape")

class ReactionTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Reaction Test")
        
        # Configure window
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(root, width=800, height=550, bg='white')
        self.canvas.pack(pady=10)
        
        # Game variables
        self.shapes = {}
        self.score = 0
        self.clicks = []
        self.game_duration = 30  # seconds
        self.start_time = None
        
        # Create score label
        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 16))
        self.score_label.pack()
        
        # Start button
        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=5)
        
        # Bind click event
        self.canvas.bind("<Button-1>", self.on_click)

    def start_game(self):
        self.start_button.config(state="disabled")
        self.score = 0
        self.clicks = []
        self.shapes.clear()
        self.canvas.delete("all")
        self.start_time = time.time()
        self.spawn_shape()
        self.root.after(self.game_duration * 1000, self.end_game)

    def spawn_shape(self):
        if self.start_time and (time.time() - self.start_time) < self.game_duration:
            shape_type = random.choice(["square", "circle", "triangle"])
            color = random.choice(["blue", "red", "green", "yellow"])
            x = random.randint(50, 750)
            y = random.randint(50, 500)
            size = random.randint(20, 40)
            
            shape = Shape(self.canvas, shape_type, color, x, y, size)
            self.shapes[shape.shape_id] = shape
            
            # Schedule next shape spawn
            self.root.after(random.randint(1000, 2000), self.spawn_shape)

    def on_click(self, event):
        if not self.start_time:
            return
            
        clicked_id = self.canvas.find_closest(event.x, event.y)
        if clicked_id:
            shape_id = clicked_id[0]
            if shape_id in self.shapes:
                shape = self.shapes[shape_id]
                reaction_time = time.time() - shape.creation_time
                
                click_data = {
                    "timestamp": time.time(),
                    "shape_type": shape.shape_type,
                    "color": shape.color,
                    "reaction_time": reaction_time,
                    "correct": shape.shape_type == "square" and shape.color == "blue"
                }
                self.clicks.append(click_data)
                
                if shape.shape_type == "square" and shape.color == "blue":
                    self.score += 1
                    self.score_label.config(text=f"Score: {self.score}")
                
                self.canvas.delete(shape_id)
                del self.shapes[shape_id]

    def end_game(self):
        self.start_time = None
        self.start_button.config(state="normal")
        self.canvas.delete("all")
        
        # Save results
        results = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": self.score,
            "clicks": self.clicks
        }
        
        with open(f"results_{int(time.time())}.json", "w") as f:
            json.dump(results, f, indent=2)
        
        messagebox.showinfo("Game Over", 
            f"Game Over!\nFinal Score: {self.score}\n"
            f"Results have been saved to file.")

if __name__ == "__main__":
    root = tk.Tk()
    game = ReactionTest(root)
    root.mainloop()