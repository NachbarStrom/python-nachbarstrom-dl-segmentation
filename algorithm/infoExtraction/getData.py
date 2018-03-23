import xlrd
import xlsxwriter
import numpy as np
from boundary_box import minBoundingRect
from getMapsImg import satImgDownload

book = xlrd.open_workbook("Data_Rest.xlsx") # in my case the directory contains the excel file named excel.xls

# Now to print the number of worksheets in the excel file 
print ("The number of worksheets are ", book.nsheets)

# Choose a specific workbook to import data 
sheet = book.sheet_by_index(0)
workbook = xlsxwriter.Workbook('Label/labelsRest.xlsx')
worksheet = workbook.add_worksheet()

# viola you have it 
# Now lets say in my excel sheet data starts with rows = 1 to 3 , and columns = 0 to 2
# PS the first row are the titles

label = {}
points = {}

for i in range(0,sheet.nrows):
      label[i] = sheet.cell_value(i,0)
      points[i] = sheet.cell_value(i,1)
 
for i in range(0,sheet.nrows):
    point = np.matrix(points[i])
    pointCloud = np.zeros([int(np.size(point,1)/2),2])
    for j in range(0,int(np.size(point,1)/2)):
        pointCloud[j,0] = point[0,j*2]
        pointCloud[j,1] = point[0,j*2+1]
        
    (minLon, maxLon, minLat, maxLat, orientation, area, center) = minBoundingRect(pointCloud)
    satImgDownload(center[0], center[1], i)

    worksheet.write(i, 0, label[i])
    worksheet.write(i, 1, area)
    worksheet.write(i, 2, orientation)
    
workbook.close()