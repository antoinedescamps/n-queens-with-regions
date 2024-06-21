#!/usr/bin/env python
# coding: utf-8

# In[17]:


import tkinter as tk
from tkinter import messagebox

def is_safe(board, row, col, queens_pos):
    for i in range(col):
        if queens_pos[i] == row or abs(queens_pos[i] - row) == abs(i - col):
            return False
    return True

def solve_nqueens_util(board, col, queens_pos, region_count, regions_used):
    if col >= len(board):
        return True

    for i in range(len(board)):
        region = board[i][col]
        if region not in regions_used and is_safe(board, i, col, queens_pos):
            queens_pos[col] = i
            regions_used.add(region)

            if solve_nqueens_util(board, col + 1, queens_pos, region_count, regions_used):
                return True

            queens_pos[col] = -1
            regions_used.remove(region)

    return False

def solve_nqueens(board):
    n = len(board)
    queens_pos = [-1] * n
    region_count = len(set(num for row in board for num in row))

    if solve_nqueens_util(board, 0, queens_pos, region_count, set()):
        return queens_pos  # Return positions of queens
    else:
        return None  # No solution exists

def create_board_input():
    n = int(size_entry.get())
    
    board_window = tk.Toplevel(root)
    board_window.title("Enter Board Configuration")

    board_buttons = []
    board_colors = [["#FFFFFF"] * n for _ in range(n)]
    selected_color = None
    
    color_frame = tk.Frame(board_window)
    color_frame.grid(row=n, columnspan=n)  # No padding specified
    
    for i in range(1, n + 1):  # Create buttons for each region
        color = "#{:02x}{:02x}{:02x}".format((i * 70) % 256, (i * 120) % 256, (i * 170) % 256)  # Generate distinct color
        color_button = tk.Button(color_frame, bg=color, width=4, height=2,
                                 command=lambda color=color: select_color(color))
        color_button.grid(row=0, column=i - 1)  # No padding specified
        color_button.config(highlightthickness=0)  # Remove button highlight
        
    def submit_board():
        nonlocal board_buttons, board_colors
        
        clear_queens()  # Clear previous queens marks
        
        board = []
        color_to_zone = {}
        zone_counter = 1
        
        for i in range(n):
            row = []
            for j in range(n):
                color = board_colors[i][j]
                if color not in color_to_zone:
                    color_to_zone[color] = zone_counter
                    zone_counter += 1
                row.append(color_to_zone[color])
            board.append(row)
        
        queens_positions = solve_nqueens(board)
        if queens_positions is not None:
            for col, row in enumerate(queens_positions):
                board_buttons[row][col].config(text='Q', fg='black', font=('Arial', 8, 'bold'))
        else:
            messagebox.showinfo("No Solution", "No solution exists for the current board configuration.")

    def clear_queens():
        for i in range(n):
            for j in range(n):
                if board_buttons[i][j].cget('text') == 'Q':
                    board_buttons[i][j].config(text='')

    def select_color(color):
        nonlocal selected_color
        selected_color = color

    def colorize_square(row, col):
        if selected_color:
            board_buttons[row][col].config(bg=selected_color)
            board_colors[row][col] = selected_color

    board_buttons = []
    
    for i in range(n):
        row_buttons = []
        for j in range(n):
            button = tk.Button(board_window, bg="#FFFFFF", width=4, height=2,
                               command=lambda i=i, j=j: colorize_square(i, j))
            button.grid(row=i, column=j, padx=1, pady=1)  # Adjusted padding
            row_buttons.append(button)
        board_buttons.append(row_buttons)

    tk.Button(board_window, text="Submit", command=submit_board).grid(row=n+1, columnspan=n)
    tk.Button(board_window, text="Clear Queens", command=clear_queens).grid(row=n+2, columnspan=n)

def main_menu():
    global size_entry
    global root

    root = tk.Tk()
    root.title("N-Queens with Regions Solver")

    tk.Label(root, text="Enter the size of the board (N):").pack()
    size_entry = tk.Entry(root)
    size_entry.pack()

    tk.Button(root, text="Enter Board", command=create_board_input).pack()
    tk.Button(root, text="Exit", command=root.destroy).pack()

    root.mainloop()

if __name__ == "__main__":
    main_menu()

