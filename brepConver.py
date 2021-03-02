
# gmsh conversion file from .brep to fenics ready mesh
# Ryan Budde CID 2021
print('start')
import gmsh
import sys

# variables
fileName = 'd4out.brep'
scaleFactor = 0.001 # mm
fullDim = 3 # 3D

# intialize
gmsh.initialize()
gmsh.model.add('testGeom')
gmsh.option.setNumber("Geometry.OCCScaling", scaleFactor) #brep files do not include scale information



# load shapes into model
volumes = gmsh.model.occ.importShapes(fileName)
gmsh.model.occ.synchronize() # this must DIRECTLY follow  import step

# volume numbering
# main cube = 1
# medium cylinder = 2
# small sphere = 3

# setup 3 volume groups for our 3 objects
t1 = gmsh.model.addPhysicalGroup(fullDim, [1], 1)
t2 = gmsh.model.addPhysicalGroup(fullDim, [2], 2)
t3 = gmsh.model.addPhysicalGroup(fullDim, [3], 3)
print(t1)
print(t2)
print(t3)
gmsh.model.setPhysicalName(fullDim, t1, 'bigCube')
gmsh.model.setPhysicalName(fullDim, t2, 'medCyl')
gmsh.model.setPhysicalName(fullDim, t3, 'lilSph')

# add some hard coded surface groups
t1 = gmsh.model.addPhysicalGroup(fullDim-1, [1], 1) # left wall of cube
t2 = gmsh.model.addPhysicalGroup(fullDim-1, [6], 2) # right wall of cube
gmsh.model.setPhysicalName(fullDim-1, t1, 'leftWall')
gmsh.model.setPhysicalName(fullDim-1, t2, 'rightWall')

# make mesh finer
lc = 5e-4
gmsh.model.mesh.setSize(gmsh.model.getBoundary([(fullDim,1)], recursive=True), lc)
gmsh.model.mesh.setSize(gmsh.model.getBoundary([(fullDim,2)], recursive=True), lc)
gmsh.model.mesh.setSize(gmsh.model.getBoundary([(fullDim,3)], recursive=True), lc)

# check
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)
gmsh.write('d4.msh')
gmsh.fltk.run()
gmsh.finalize()


print('end')
