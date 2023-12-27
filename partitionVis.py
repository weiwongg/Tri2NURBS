"""

convert the quad mesh to the NURBS surface

"""
import numpy as np
import os
import argparse
import meshio
from src.utils import correct_faces
from src.patches_search import find_complex_base, find_patches




# import quad mesh
parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Path to input quadmesh obj file.')


args = parser.parse_args()
input = args.input

mesh = meshio.read(args.input)
input_points = mesh.points
input_faces = mesh.cells_dict['quad']
input_faces = correct_faces(input_faces)
input_faces = [face.tolist() for face in input_faces]

singularities, complex_base_nodes, complex_base_traces = find_complex_base(input_points, input_faces)

## Summary Info
patches, total_control_pts = find_patches(input_faces, complex_base_nodes, complex_base_traces)
print('#### Summary')
print('#### The number of vertices and singularities are {0} and {1}'.format(len(input_points), len(singularities)))
print('#### The number of faces and patches are {0} and {1}'.format(len(input_faces), int(len(patches))))


# visualization
import pyvista as  pv
mesh = pv.PolyData(np.array(input_points), np.hstack([[4] + face for face in input_faces]))
p = pv.Plotter()
p.add_mesh(mesh, lighting = True)

#visualize singularities
p.add_points(input_points[singularities], color="r", render_points_as_spheres=True, point_size=20.0)

#visualize complex_base_traces
quad_layout_lines = []
for trace in complex_base_traces:
    for i in range(len(trace)-1):
        quad_layout_lines.append([2, trace[i], trace[i+1]])
quad_layout_mesh = pv.PolyData(np.array(input_points), np.hstack(quad_layout_lines))
p.add_mesh(quad_layout_mesh, line_width=10, style="wireframe", color="g",render_lines_as_tubes=True)


patch_lines = []
# show one random patch
for patch in patches:
    for side in patch:
        for i in range(4):
            patch_lines.append([2, input_faces[side][i], input_faces[side][(i+1)%4]])
patch_mesh = pv.PolyData(np.array(input_points), np.hstack(patch_lines))
p.add_mesh(patch_mesh, line_width=5, style="wireframe", color="b")
p.show()



