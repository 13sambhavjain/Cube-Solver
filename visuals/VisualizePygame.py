import pygame
from Colors import *
def draw_cube_state(cube_state_dict):
    """
    Visualizes a 3x3 cube state using Pygame.
    The cube state is expected to be a dictionary like yours.
    """
    pygame.init()

    # Define colors
    colors = {
        w: (255, 255, 255),
        y: (255, 255, 0),
        g: (0, 255, 0),
     b: (0, 0, 255),
        r: (255, 0, 0),
        o: (255, 165, 0)
    }
    
    # Standard cube face layout (net)
    face_layout = {
        w: (0, 0), b: (0, 1), o: (1, 1), y: (1, 2), g: (2, 2), r: (2, 3)
    }

    # Set up the screen
    sticker_size = 50
    gap = 5
    padding = 20
    window_width = 4 * sticker_size + 4 * gap + 2 * padding
    window_height = 3 * sticker_size + 3 * gap + 2 * padding
    screen = pygame.display.set_mode((window_width*2, window_height*3.5))
    pygame.display.set_caption("3x3 Cube Visualizer")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0)) # Fill background with black

        # Draw each face
        for face, (x_pos, y_pos) in face_layout.items():
            for row in range(3):
                for col in range(3):
                    color_name = cube_state_dict[face][row][col]
                    rect_x = padding + (x_pos * 3 + col) * (sticker_size + gap)
                    rect_y = padding + (y_pos * 3 + row) * (sticker_size + gap)
                    pygame.draw.rect(screen, colors[color_name], (rect_x, rect_y, sticker_size, sticker_size))

        pygame.display.flip()

    pygame.quit()

# Your cube state example
my_cube_state = {
    w: [[w, w, w], [w, w, w], [w, w, w]],
    o: [[o, o, o], [o, o, o], [o, o, o]],
    g: [[g, g, g], [g, g, g], [g, g, g]],
    r: [[r, r, r], [r, r, r], [r, r, r]],
    b: [[b, b, b], [b, b, b], [b, b, b]],
    y: [[y, y, y], [y, y, y], [y, y, y]]
}

# To run the visualization, simply call the function
draw_cube_state(my_cube_state)
