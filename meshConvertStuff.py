"""
The following is the first attempt to convert the
gmsh .msh file into a more usable meshio file format
for eventual import in fenics
"""

""" 
this file is entirely reproduced work from
Jorgen Dokken on the fenics discourse page
"""

import meshio
import numpy

def create_mesh(mesh, cell_type, prune_z=False):
    cells = mesh.get_cells_type(cell_type)
    cell_data = mesh.get_cell_data("gmsh:physical", cell_type)
    out_mesh = meshio.Mesh(points=mesh.points, cells={cell_type: cells}, cell_data={"name_to_read":[cell_data]})
    if prune_z:
        out_mesh.prune_z_0()
    return out_mesh

msh = meshio.read("d4.msh")
triangleMesh = create_mesh(msh, "triangle", False)
tetraMesh = create_mesh(msh, "tetra", False)

meshio.write("d4_triag.xdmf", triangleMesh)
meshio.write("d4_tetra.xdmf", tetraMesh)

from dolfin import * 
mesh = Mesh()
print(mesh.topology().dim())
mvc = MeshValueCollection("size_t", mesh, 3)
with XDMFFile("d4_tetra.xdmf") as infile:
   infile.read(mesh)
   infile.read(mvc, "name_to_read")
cf = cpp.mesh.MeshFunctionSizet(mesh, mvc)

mvc = MeshValueCollection("size_t", mesh, 2)
with XDMFFile("d4_triag.xdmf") as infile:
    infile.read(mvc, "name_to_read")
mf = cpp.mesh.MeshFunctionSizet(mesh, mvc)
