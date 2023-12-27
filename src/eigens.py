"""

Compute Eigen functions of Laplace-Beltrami operator on surface triangle mesh.

Copyright (C) 2022
 
"""
import igl
import scipy as sp
import numpy as np
from scipy.sparse import identity
import os
from copy import deepcopy
from src.io import read_vtk_file
from src.io import triangle_faces_to_VTK

def eigens(filename, out_file, num):
    ## Load a mesh
    if filename.endswith(".vtp"):
        v,quad_f = read_vtk_file(filename)
        tri_f = []
        for quad in quad_f:
            tri_f.append([quad[1],quad[2],quad[3]])
            tri_f.append([quad[3],quad[4],quad[1]])
        f = np.array(tri_f)
    else:
        v,f = igl.read_triangle_mesh(filename)
    l = -igl.cotmatrix(v, f)
    m = igl.massmatrix(v, f, igl.MASSMATRIX_TYPE_VORONOI)
    d, u = sp.sparse.linalg.eigsh(l, num, m, sigma=0.1, which="LM")
    u = (u - np.min(u)) / (np.max(u) - np.min(u))
    pd = {"EigenFunctions" : u}
    x = deepcopy(v[:,0])
    y = deepcopy(v[:,1])
    z = deepcopy(v[:,2])
    triangle_faces_to_VTK(out_file, x, y, z, f, pd)
