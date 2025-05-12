# Developed in Python 3.12.5

import pygame as pg
from environment import Screen
from environment import RenderSpace
from environment import Mesh
from environment import deg_to_rad

WIDTH = 1000
HEIGHT = 1000

screen = Screen(WIDTH, HEIGHT)
time, time_steps = 0, 110

render_space = RenderSpace()
# Just put in the name of your object file that is in the objects folder
mesh = Mesh(object_file='cat.obj', origin_translate=True)

degree = deg_to_rad(1)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            # Mouse scroll up
            if event.button == 4:
                render_space.zoom += render_space.zoom / render_space.zoom_speed
            # Mouse scroll down
            elif event.button == 5:
                render_space.zoom -= render_space.zoom / render_space.zoom_speed
                # Cap maximum zoom out
                if render_space.zoom <= 0:
                    render_space.zoom = render_space.zoom / render_space.zoom_speed

    # Comment out these three lines to stop mesh from rotating without user input
    mesh.vertices = render_space.rotate_x(mesh.vertices, degree)
    mesh.vertices = render_space.rotate_y(mesh.vertices, degree)
    mesh.vertices = render_space.rotate_z(mesh.vertices, degree)

    keys = pg.key.get_pressed()

    if keys[pg.K_w]:
        mesh.vertices = render_space.rotate_x(mesh.vertices, degree)
    if keys[pg.K_s]:
        mesh.vertices = render_space.rotate_x(mesh.vertices, -degree)
    if keys[pg.K_a]:
        mesh.vertices = render_space.rotate_y(mesh.vertices, -degree)
    if keys[pg.K_d]:
        mesh.vertices = render_space.rotate_y(mesh.vertices, degree)

    # Reset screen
    screen.set()

    # Update
    time_now = pg.time.get_ticks()
    if time_now - time > time_steps:
        # Obviously using the CPU for 3D graphics rendering
        # is laughably awful but who cares
        render_space.render_mesh(mesh, screen)
            
    # Flip() display to update screen
    screen.flip()

    # Limit FPS to 60
    screen.time_step(60)

    # Display FPS
    pg.display.set_caption(f'FPS - {int(screen.clock.get_fps())}')
