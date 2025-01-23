import tkinter as tk
from collections import deque
import random

CELL_SIZE = 40  # Size of each cell in pixels

class MicromouseMaze:
    def __init__(self, root, grid_width, grid_height):
        self.root = root
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid = [[EMPTY for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.start = None
        self.goal = None
        self.current_mode = EMPTY

        # Center the maze
        canvas_width = self.grid_width * CELL_SIZE
        canvas_height = self.grid_height * CELL_SIZE
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(pady=20)

        self.canvas = tk.Canvas(self.canvas_frame, width=canvas_width, height=canvas_height, bg="black")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        # Buttons below the maze
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        self.select_obstacle_button = tk.Button(self.buttons_frame, text="Select Obstacle", command=self.select_obstacle)
        self.select_obstacle_button.grid(row=0, column=0, padx=5)

        self.random_obstacles_button = tk.Button(self.buttons_frame, text="Random Obstacles", command=self.generate_random_obstacles)
        self.random_obstacles_button.grid(row=0, column=1, padx=5)

        self.select_start_button = tk.Button(self.buttons_frame, text="Start", command=self.select_start)
        self.select_start_button.grid(row=0, column=2, padx=5)

        self.select_goal_button = tk.Button(self.buttons_frame, text="Goal", command=self.select_goal)
        self.select_goal_button.grid(row=0, column=3, padx=5)

        self.solve_button = tk.Button(self.buttons_frame, text="Solve", command=self.solve_maze)
        self.solve_button.grid(row=0, column=4, padx=5)

        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_maze)
        self.reset_button.grid(row=0, column=5, padx=5)

        # Grid resizing controls
        self.resize_frame = tk.Frame(root)
        self.resize_frame.pack(pady=10)

        tk.Label(self.resize_frame, text="Grid Width:").grid(row=0, column=0, padx=5)
        self.width_entry = tk.Entry(self.resize_frame, width=5)
        self.width_entry.insert(0, str(self.grid_width))
        self.width_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.resize_frame, text="Grid Height:").grid(row=0, column=2, padx=5)
        self.height_entry = tk.Entry(self.resize_frame, width=5)
        self.height_entry.insert(0, str(self.grid_height))
        self.height_entry.grid(row=0, column=3, padx=5)

        self.resize_button = tk.Button(self.resize_frame, text="Resize Grid", command=self.resize_grid)
        self.resize_button.grid(row=0, column=4, padx=5)

        self.draw_grid()

    def select_obstacle(self):
        self.current_mode = OBSTACLE  

    def select_start(self):
        self.current_mode = START  

    def select_goal(self):
        self.current_mode = GOAL 

    def draw_grid(self):
        self.canvas.delete("all")
        self.canvas.config(width=self.grid_width * CELL_SIZE, height=self.grid_height * CELL_SIZE)
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                color = "white"
                if self.grid[i][j] == OBSTACLE:
                    color = "black"
                elif self.grid[i][j] == START:
                    color = "green"
                elif self.grid[i][j] == GOAL:
                    color = "red"
                self.canvas.create_rectangle(j * CELL_SIZE, i * CELL_SIZE,
                                              (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
                                              fill=color, outline="gray")

    def on_click(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        if 0 <= row < self.grid_height and 0 <= col < self.grid_width:
            if self.current_mode == OBSTACLE:
                self.grid[row][col] = OBSTACLE
            elif self.current_mode == START:
                if self.start: 
                    self.grid[self.start[0]][self.start[1]] = EMPTY
                self.grid[row][col] = START
                self.start = (row, col)
            elif self.current_mode == GOAL:
                if self.goal: 
                    self.grid[self.goal[0]][self.goal[1]] = EMPTY
                self.grid[row][col] = GOAL
                self.goal = (row, col)

            self.draw_grid()

    def reset_maze(self):
        self.start = None
        self.goal = None
        self.grid = [[EMPTY for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.draw_grid()

    def solve_maze(self):
        if not self.start or not self.goal:
            print("Start or goal not set!")
            return

        path = self.bfs(self.start, self.goal)
        if path:
            self.snake_movement(path)
        else:
            print("No path found!")

    def bfs(self, start, goal):
        queue = deque([start])
        parent_map = {start: None}
        visited = set()
        visited.add(start)

        while queue:
            current = queue.popleft()
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = parent_map[current]
                path.reverse()
                return path
            for direction in DIRECTIONS:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if 0 <= neighbor[0] < self.grid_height and 0 <= neighbor[1] < self.grid_width:
                    if neighbor not in visited and self.grid[neighbor[0]][neighbor[1]] != OBSTACLE:
                        visited.add(neighbor)
                        parent_map[neighbor] = current
                        queue.append(neighbor)

        return None 

    def snake_movement(self, path):
        # Animate the snake-like movement along the path
        def move_snake(step):
            if step < len(path):
                r, c = path[step]
                if (r, c) != self.start and (r, c) != self.goal:
                    self.canvas.create_rectangle(
                        c * CELL_SIZE, r * CELL_SIZE,
                        (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE,
                        fill="yellow", outline="gray"
                    )
                self.root.after(200, move_snake, step + 1)  # Delay for the next step

        move_snake(0)  # Start the movement

    def resize_grid(self):
        try:
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())
            if new_width > 0 and new_height > 0:
                self.grid_width = new_width
                self.grid_height = new_height
                self.reset_maze()  
            else:
                print("Width and Height must be positive integers!")
        except ValueError:
            print("Invalid input! Please enter valid integers for width and height.")

    def generate_random_obstacles(self):
        self.reset_maze()
        obstacle_count = (self.grid_width * self.grid_height) // 4
        for _ in range(obstacle_count):
            row = random.randint(0, self.grid_height - 1)
            col = random.randint(0, self.grid_width - 1)
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = OBSTACLE
        self.draw_grid()


# Constants
EMPTY = 'E'
OBSTACLE = 'O'
START = 'S'
GOAL = 'G'
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Create and run the application
root = tk.Tk()
root.title("Micromouse Maze Solver")

# Default maze dimensions
GRID_WIDTH = 15  # Initial width
GRID_HEIGHT = 15  # Initial height

maze = MicromouseMaze(root, GRID_WIDTH, GRID_HEIGHT)
root.mainloop()
