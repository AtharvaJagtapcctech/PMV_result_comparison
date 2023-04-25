import vtk
import numpy as np


left_corner_x_coordinate = 3.125999927520752
left_corner_y_coordinate = 82.37400817871094
left_corner_z_coordinate = 0.0
delta_x = 0.011137546955283542
delta_y = 0.01109062296851783
delta_z = 0.011200163315753548
grid_dimensions = [ 808, 674, 246]
xmax=left_corner_x_coordinate +(delta_x * grid_dimensions[0])
ymax=left_corner_y_coordinate +(delta_y * grid_dimensions[1])
zmax=left_corner_z_coordinate +(delta_z * grid_dimensions[2])

pmv = []

def Get_nearest_coordinate(coordinate:float,left_corner_x_coordinate:float,delta)->float:
    temp=0
    if coordinate<left_corner_x_coordinate:
        return 0
    temp = coordinate-left_corner_x_coordinate
    temp/=delta
    temp = round(temp)
    return temp


filename = "D:\\STL_code\\PMV_Validation\\PMV_Validation\\PPOEUu4\\p3CZ0C9_26cC55c_mWFrUpu\\updatedTriangulation_ManikinSeatingSingle.stl"
reader = vtk.vtkSTLReader()
reader.SetFileName(filename)
reader.Update()
polyData = reader.GetOutput()

# Open the binary file
with open('D:\\STL_code\\PMV_Validation\\PMV_Validation\\PPOEUu4\\p3CZ0C9_26cC55c_mWFrUpu\\Grid3D_ThermalPMV_Data.dat', 'rb') as f:
    # Read the binary data into a 1D array
    data_array = np.fromfile(f, dtype=np.float32)

# Reshape the 1D array into a 3D array
data_shape = (808,674,246) 
data_array = np.reshape(data_array, data_shape)

rows = []

bounds = polyData.GetBounds()

# Compute the center of the bounds
center = [
    (bounds[0] + bounds[1]) / 2,
    (bounds[2] + bounds[3]) / 2,
    (bounds[4] + bounds[5]) / 2,
]

#Move the object to a new location
#newCenter = [5.4864004990275, 87.7823066019169, 0.61346875]
#newCenter = [10.0584004990275, 84.7343066019169, 0.61346875]
#newCenter = [9.753601372593173, 87.7823066019169, 0.61346875]
newCenter = [5.486401372593173, 84.7343066019169, 0.61346875]
translation = [newCenter[i] - center[i] for i in range(3)]
transform = vtk.vtkTransform()
transform.Translate(translation[0], translation[1], 0)
transformFilter = vtk.vtkTransformPolyDataFilter()
transformFilter.SetInputData(polyData)
transformFilter.SetTransform(transform)
transformFilter.Update()
polyData = transformFilter.GetOutput()

facets = polyData.GetPolys()

points = polyData.GetPoints()
# Loop through each facet and print the indices of its vertices
facetIndex = 0
offset=0
total_averagepmv=0 
while True:
    pointIds = vtk.vtkIdList()
    
    if not facets.GetNextCell(pointIds):
        break
    #print("Facet", facetIndex, "with", pointIds.GetNumberOfIds(), "vertices:")
    average_pmv=0
    
    for i in range(pointIds.GetNumberOfIds()):
        outbond=True
       # print("    Vertex", i+1, "index:", pointIds.GetId(i))
        x, y, z = points.GetPoint(pointIds.GetId(i))
        if z<0:
            outbond=False
            offset+=1
            break
        new_x=Get_nearest_coordinate(x,left_corner_x_coordinate,delta_x)
        new_y=Get_nearest_coordinate(y,left_corner_y_coordinate,delta_y)
        new_z=Get_nearest_coordinate(z,left_corner_z_coordinate,delta_z)
        #print(new_x," ",new_y," ",new_z)
        average_pmv+=data_array[new_x,new_y,new_z]
    #print("Average PMV ",average_pmv/3)
    # if outbond==False:
    #      break  
    total_averagepmv+=(average_pmv/3)
    if outbond==True:     
     facetIndex += 1

total_averagepmv=total_averagepmv/(facetIndex)

print("Location 4")
print("Averaged PMV =",total_averagepmv)
print("Total facets out of bond ",offset)
print(facetIndex)
# massProperties = vtk.vtkMassProperties()
# massProperties.SetInputData(polyData)
# massProperties.Update()
# surfaceArea = massProperties.GetSurfaceArea()