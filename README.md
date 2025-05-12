![Sphere](https://github.com/user-attachments/assets/02fa427d-04ae-4c32-96a4-e9e72adf61f5)
![Bunny](https://github.com/user-attachments/assets/0d8c0dcb-0724-4cec-85e6-1fa283c1f1d8)
![Teapot](https://github.com/user-attachments/assets/d10c06bc-8f3b-4f02-9ecf-5c42746c451b)

# Purpose
This code uses CPU compute to render 3-dimensional meshes from a primitive object file. Obviously rendering graphics on a CPU is wildly inefficient, but this is just a cool project that I had fun figuring out.

# Install
To run, you'll need Python 3 installed. Then clone the repository and install the needed modules.

```git clone https://github.com/EthanNoble/Python-3D-Renderer.git```

```pip install -r requirements.txt```

# Usage
To run the program, just use ```python main.py```.

In ```main.py``` you'll see that a mesh object is created by passing in a ```.obj``` file name string. You can pass in the name of any file that is in the ```objects``` directory to load the mesh.

You can zoom in and out using the mouse scroll wheel. When you first run the program, the mesh might appear as a tiny dot. Just zoom in until it fills the screen.
