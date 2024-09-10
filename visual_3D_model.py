from pythreejs import *
import numpy as np
from IPython.display import display

# Load your 3D model file
model_path = '3D_model/model.obj'

# Create a scene
scene = Scene()
camera = PerspectiveCamera(position=[0, 0, 5], fov=70, aspect=1.5)
renderer = Renderer(camera=camera, scene=scene, controls=[OrbitControls(controlling=camera)])

# Load model
with open(model_path, 'r') as file:
    obj_data = file.read()

# Add model to scene
geometry = Geometry.from_obj(obj_data)
material = MeshBasicMaterial(color='red')
mesh = Mesh(geometry=geometry, material=material)
scene.add(mesh)

# Display
display(renderer)
