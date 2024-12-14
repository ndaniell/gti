"""
Conway's Game of Life - Enhanced Edition

A cellular automaton simulation following Conway's Game of Life rules,
with enhanced visual features including color gradients, cell aging, and glow effects.

Rules:
1. Any live cell with fewer than two live neighbors dies (underpopulation)
2. Any live cell with two or three live neighbors lives on to the next generation
3. Any live cell with more than three live neighbors dies (overpopulation)
4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction)

Controls:
- Space: Pause/Resume simulation
- R: Randomize grid
- Click: Toggle cell state
- ESC: Quit
- H: Toggle UI visibility
"""

import pygame
import numpy as np
import colorsys

# Initialize Pygame
pygame.init()

# Set up the display with comfortable viewing dimensions
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life - Enhanced Edition")

# Color definitions for visual elements
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GRID_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (20, 20, 20)

# Grid configuration
cell_size = 12  # Size of each cell in pixels
cols = width // cell_size  # Number of columns in grid
rows = height // cell_size  # Number of rows in grid

# Initialize grid with random state (15% chance of live cells)
grid = np.random.choice([0, 1], size=(rows, cols), p=[0.85, 0.15])
next_grid = np.zeros((rows, cols))

def generate_color_palette(n):
    """
    Generate a smooth color palette for cell aging visualization.
    
    Args:
        n (int): Number of colors to generate
        
    Returns:
        list: List of RGB color tuples
    """
    colors = []
    for i in range(n):
        hue = i / n
        rgb = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
        colors.append([int(255 * x) for x in rgb])
    return colors

# Initialize color palette and cell age tracking
color_palette = generate_color_palette(256)
cell_ages = np.zeros((rows, cols))

def count_neighbors(grid, x, y):
    """
    Count the number of live neighbors for a cell.
    
    Args:
        grid (numpy.array): The current grid state
        x (int): Row index of the cell
        y (int): Column index of the cell
        
    Returns:
        int: Number of live neighbors (0-8)
    """
    rows, cols = grid.shape
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:  # Skip the cell itself
                continue
            row = (x + i) % rows  # Simplified wrapping
            col = (y + j) % cols
            total += grid[row, col]
    return total

def update_grid():
    """
    Update the grid according to Conway's Game of Life rules.
    Also handles cell aging for visual effects.
    """
    global grid, cell_ages
    next_grid = grid.copy()
    
    for i in range(rows):
        for j in range(cols):
            neighbors = count_neighbors(grid, i, j)
            
            if grid[i, j] == 1:  # Rules for live cells
                if neighbors < 2 or neighbors > 3:
                    next_grid[i, j] = 0  # Cell dies
                    cell_ages[i, j] = 0
                else:
                    cell_ages[i, j] = min(255, cell_ages[i, j] + 1)  # Cell ages
            else:  # Rules for dead cells
                if neighbors == 3:
                    next_grid[i, j] = 1  # Cell becomes alive
                    cell_ages[i, j] = 0
    
    grid = next_grid

def draw_grid():
    """
    Draw the current state of the grid with enhanced visuals including
    cell colors based on age and glow effects.
    """
    screen.fill(BACKGROUND_COLOR)
    
    # Draw cells with color based on age and glow effect
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 1:
                age = int(cell_ages[i, j])
                color = color_palette[age]
                
                # Create glow effect with three layers
                cell_rect = pygame.Rect(j*cell_size, i*cell_size, cell_size-1, cell_size-1)
                pygame.draw.rect(screen, [c//3 for c in color],
                               cell_rect.inflate(4, 4))  # Outer glow
                pygame.draw.rect(screen, [c//2 for c in color],
                               cell_rect.inflate(2, 2))  # Middle glow
                pygame.draw.rect(screen, color, cell_rect)  # Cell center

    # Draw grid lines for better cell visibility
    if cell_size > 4:
        for i in range(rows + 1):
            pygame.draw.line(screen, GRID_COLOR, (0, i * cell_size),
                           (width, i * cell_size), 1)
        for j in range(cols + 1):
            pygame.draw.line(screen, GRID_COLOR, (j * cell_size, 0),
                           (j * cell_size, height), 1)

def draw_ui():
    """
    Draw user interface elements including control instructions.
    """
    font = pygame.font.Font(None, 24)
    controls = [
        "Controls:",
        "Space: Pause/Resume",
        "R: Random Grid",
        "Click: Toggle Cell",
        "Esc: Quit"
    ]
    
    y = 10
    for text in controls:
        surface = font.render(text, True, WHITE)
        screen.blit(surface, (10, y))
        y += 25

def main():
    """
    Main game loop handling user input and simulation updates.
    """
    running = True
    paused = False
    show_ui = True
    clock = pygame.time.Clock()

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    grid[:] = np.random.choice([0, 1], size=(rows, cols), p=[0.85, 0.15])
                    cell_ages.fill(0)
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle cell state on click
                x, y = pygame.mouse.get_pos()
                i, j = y // cell_size, x // cell_size
                if 0 <= i < rows and 0 <= j < cols:
                    grid[i, j] = not grid[i, j]
                    cell_ages[i, j] = 0

        # Update simulation if not paused
        if not paused:
            update_grid()
        
        # Draw everything
        draw_grid()
        if show_ui:
            draw_ui()
        
        pygame.display.flip()
        clock.tick(30)  # Control frame rate

    pygame.quit()

if __name__ == '__main__':
    main()