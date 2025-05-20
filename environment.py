import pygame as pg
from enum import Enum
from numpy import cross
from numpy import array
from numpy import dot
from numpy import linalg
from math import sin
from math import cos
from math import pi

class Color(Enum):
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    LIGHT_GRAY = (200, 200, 200)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

class Screen:
    def __init__(self, width, height, color=Color.BLACK.value):
        self.width = width
        self.height = height
        self.color = color
        self.screen = None
        self.clock = None
        self.dt = None
        self.init_screen()
    
    def __call__(self):
        return self.screen

    def init_screen(self):
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.dt = 0
    
    def set(self):
        self.screen.fill(self.color) # Reset screen
    
    def flip(self):
        pg.display.flip()

    def time_step(self, fps):
        self.dt = self.clock.tick(fps) / 1000

class RenderSpace:
    def __init__(self):
        self.zoom = 1
        self.zoom_speed = 10 # How fast you can zoom in/out
        self.light_source = [1, 0, 1]
        self.light_color = Color.LIGHT_GRAY.value

    def render_mesh(self, mesh, surface):
        buffer = []
        for polygon in mesh.polygons:
            # Build polygon vertices
            vert_1 = mesh.vertices[polygon[0]-1]
            vert_2 = mesh.vertices[polygon[1]-1]
            vert_3 = mesh.vertices[polygon[2]-1]
            # Render polygon based on normal vector direction
            polygon_normal = cross((array(vert_2) - array(vert_1)), (array(vert_3) - array(vert_1)))
            if polygon_normal[2] > 0:
                points = []
                for point in [vert_1, vert_2, vert_3]:
                    x = point[0]
                    y = point[1]
                    z = point[2]

                    x_proj = (x * self.zoom) + (surface.width // 2)
                    y_proj = (y * self.zoom) + (surface.height // 2)
                    # Keeping unprojected z for buffering
                    points.append((x_proj, y_proj, z))
                # Shade polygon based on dot product of polygon normal and light normal
                shade_intensity = dot(normalize(polygon_normal), normalize(self.light_source))
                shade_intensity = max(shade_intensity, 0.02)
                color = (self.light_color[0] * shade_intensity, self.light_color[1] * shade_intensity, self.light_color[2] * shade_intensity)
                buffer.append({'rgb': color, 'verts': points})

        # Sort polygons based on z value to avoid overlapping
        # by returning average position of all three vertices
        # TODO: This method is definitely not the way to do it
        # but it some what works
        def sortVertices(polygon):
            vert1_z = polygon['verts'][0][2]
            vert2_z = polygon['verts'][1][2]
            vert3_z = polygon['verts'][2][2]
            return (vert1_z + vert2_z + vert3_z) / 3
        buffer.sort(key=sortVertices)

        for polygon in buffer:
            point1 = polygon['verts'][0][0:2]
            point2 = polygon['verts'][1][0:2]
            point3 = polygon['verts'][2][0:2]
            pg.draw.polygon(surface(), polygon['rgb'], (point1, point2, point3))

class Mesh:
    def __init__(self, object_file: str, origin_translate=False, preload_normals=False):
        self.polygons, self.vertices = load_obj_file(object_file)
        # Translates mesh roughly to origin for better
        # rotations around the origin
        if origin_translate:
            self.translate_to_origin()
        if preload_normals:
            self.__preload_normals()
    
    def rotate_x(self, theta):
        self.vertices = self.vertices @ array([
            [1, 0, 0],
            [0, cos(theta), sin(theta)],
            [0, -sin(theta), cos(theta)]
        ])

    def rotate_y(self, theta):
        self.vertices = self.vertices @ array([
            [cos(theta), 0, -sin(theta)],
            [0, 1, 0],
            [sin(theta), 0, cos(theta)]
        ])

    def rotate_z(self, theta):
        self.vertices = self.vertices @ array([
            [cos(theta), sin(theta), 0],
            [-sin(theta), cos(theta), 0],
            [0, 0, 1]
        ])

    def translate_to_origin(self):
        x_sum, y_sum, z_sum = 0, 0, 0
        for vertex in self.vertices:
            x_sum += vertex[0]
            y_sum += vertex[1]
            z_sum += vertex[2]

        # Basically just calculating average
        # position of all vertices
        x_origin = x_sum / len(self.vertices)
        y_origin = y_sum / len(self.vertices)
        z_origin = z_sum / len(self.vertices)

        for i in range(len(self.vertices)):
            self.vertices[i][0] -= x_origin
            self.vertices[i][1] -= y_origin
            self.vertices[i][2] -= z_origin
    
    def __preload_normals(self):
        pass

def deg_to_rad(degree):
    return (degree%361) * (pi/180)

def normalize(vector):
    norm = linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def load_obj_file(filename):
    def parse_face(face):
        simple_parse = '/' not in face
        if simple_parse: # If only vertices are referenced in face
            return list(map(int, face.split(' ')[1:]))
        else:
            face = face.replace('f ', '').replace('\n', '')
            face = face.split(' ')
            # Only grab face vertices
            # TODO: Grab other information like normals if present
            return [int(vertex_index.split('/')[0]) for vertex_index in face if vertex_index != '']

    vertices = []
    faces = []
    with open(f'objects/{filename}', 'r') as file:
        lines = file.readlines()
        vertices = [list(map(float, vertex.split(' ')[1:])) for vertex in lines if vertex.startswith('v ')]
        faces = [parse_face(face) for face in lines if face.startswith('f ')]

    return [faces, vertices]
