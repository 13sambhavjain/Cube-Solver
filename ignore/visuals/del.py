import pygame

def draw_cube_in_window(screen, cube_state_dict, colors, face_layout, sticker_size, gap, padding):
    """Draws the cube state onto the screen without creating a new window."""
    screen.fill((0, 0, 0))  # Clear the screen

    # Draw each face
    for face, (x_pos, y_pos) in face_layout.items():
        for row in range(3):
            for col in range(3):
                color_name = cube_state_dict[face][row][col]
                rect_x = padding + (x_pos * 3 + col) * (sticker_size + gap)
                rect_y = padding + (y_pos * 3 + row) * (sticker_size + gap)
                pygame.draw.rect(screen, colors[color_name], (rect_x, rect_y, sticker_size, sticker_size))

    pygame.display.flip()

def visualize_cube_moves(initial_state, move_sequence):
    """
    Sets up the window and visualizes a series of cube state changes.
    `move_sequence` is a list of cube state dictionaries.
    """
    pygame.init()

    # Define colors
    colors = {
        'white': (255, 255, 255),
        'yellow': (255, 255, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'red': (255, 0, 0),
        'orange': (255, 165, 0)
    }
    
    # Standard cube face layout (net)
    face_layout = {
        'U': (1, 0), 'L': (0, 1), 'F': (1, 1), 'R': (2, 1), 'B': (3, 1), 'D': (1, 2)
    }

    # Window dimensions
    sticker_size = 50
    gap = 5
    padding = 20
    window_width = 4 * sticker_size + 4 * gap + 2 * padding
    window_height = 3 * sticker_size + 3 * gap + 2 * padding
    screen = pygame.display.set_mode((window_width*4, window_height*3))
    pygame.display.set_caption("3x3 Cube Visualizer")

    # The main application loop
    running = True
    current_step = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Example: Advance to the next state on key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_step += 1
                    if current_step >= len(move_sequence):
                        current_step = 0  # Loop back to the start

        # Update the cube's state
        if current_step < len(move_sequence):
            current_state = move_sequence[current_step]
            draw_cube_in_window(screen, current_state, colors, face_layout, sticker_size, gap, padding)
        
        pygame.time.delay(50) # Small delay to prevent high CPU usage

    pygame.quit()

# --- Example of how to use this ---

# 1. Define your initial cube state
initial_cube = {
    'U': [['white', 'white', 'white'], ['white', 'white', 'white'], ['white', 'white', 'white']],
    'L': [['orange', 'orange', 'orange'], ['orange', 'orange', 'orange'], ['orange', 'orange', 'orange']],
    'F': [['green', 'green', 'green'], ['green', 'green', 'green'], ['green', 'green', 'green']],
    'R': [['red', 'red', 'red'], ['red', 'red', 'red'], ['red', 'red', 'red']],
    'B': [['blue', 'blue', 'blue'], ['blue', 'blue', 'blue'], ['blue', 'blue', 'blue']],
    'D': [['yellow', 'yellow', 'yellow'], ['yellow', 'yellow', 'yellow'], ['yellow', 'yellow', 'yellow']]
}

# 2. Simulate some moves and store the resulting states
#    (You would replace this with your actual cube-solving logic)
state_after_move_1 = {
    'U': [['white', 'white', 'green'], ['white', 'white', 'green'], ['white', 'white', 'green']],
    'L': [['orange', 'orange', 'orange'], ['orange', 'orange', 'orange'], ['orange', 'orange', 'orange']],
    'F': [['white', 'white', 'red'], ['green', 'green', 'red'], ['green', 'green', 'red']],
    'R': [['yellow', 'yellow', 'yellow'], ['red', 'red', 'red'], ['red', 'red', 'red']],
    'B': [['blue', 'blue', 'blue'], ['blue', 'blue', 'blue'], ['blue', 'blue', 'blue']],
    'D': [['yellow', 'yellow', 'blue'], ['yellow', 'yellow', 'blue'], ['yellow', 'yellow', 'blue']]
}

state_after_move_2 = {
    'U': [['white', 'white', 'red'], ['white', 'white', 'red'], ['white', 'white', 'red']],
    'L': [['white', 'white', 'orange'], ['orange', 'orange', 'orange'], ['orange', 'orange', 'orange']],
    'F': [['green', 'green', 'green'], ['green', 'green', 'green'], ['green', 'green', 'green']],
    'R': [['yellow', 'yellow', 'yellow'], ['red', 'red', 'red'], ['red', 'red', 'red']],
    'B': [['blue', 'blue', 'blue'], ['blue', 'blue', 'blue'], ['blue', 'blue', 'blue']],
    'D': [['yellow', 'yellow', 'blue'], ['yellow', 'yellow', 'blue'], ['yellow', 'yellow', 'blue']]
}

# 3. Create the sequence of states you want to visualize
move_sequence = [initial_cube, state_after_move_1, state_after_move_2, initial_cube]

# 4. Call the visualization function
visualize_cube_moves(initial_cube, move_sequence)

