import xlrd
import xlsxwriter
import numpy as np
import re

book = xlrd.open_workbook("Portugal.xlsx") # in my case the directory contains the excel file named excel.xls

# Now to print the number of worksheets in the excel file 
print ("The number of worksheets are ", book.nsheets)

# Choose a specific workbook to import data 
sheet = book.sheet_by_index(0)
workbook = xlsxwriter.Workbook('Data_Portugal.xlsx')
worksheet = workbook.add_worksheet()

# viola you have it 
# Now lets say in my excel sheet data starts with rows = 1 to 3 , and columns =0 to 2
# PS the first row are the titles

roofType = {}
pointClouds = {}

numRows = sheet.nrows

nRoof = 0
nGeom = 0

for i in range(0,numRows):
      if("geometry" in str(sheet.cell_value(i,0)) and "lat" in str(sheet.cell_value(i+1,0))):
          pointCloud = []
          i +=1
          j = 0
          while("lat" in str(sheet.cell_value(i+j,0))):
              numValues = re.findall(r"[-+]?\d*\.\d+|\d+", sheet.cell_value(i+j,0))
              numValues = [float(numValues[0]), float(numValues[1])]
              pointCloud.append(numValues)
              print(j)
              j +=1
          i +=j
          pointClouds[nGeom] = str(np.matrix(pointCloud))
          nGeom += 1
      else:
          if("roof:shape" in str(sheet.cell_value(i,0)) and nGeom == nRoof + 1):
              roofType[nRoof] = sheet.cell_value(i,0)
              nRoof += 1
              
if(nRoof == nGeom):
    for i in range(0,nRoof):
        worksheet.write(i, 0, roofType[i])
        worksheet.write(i, 1, pointClouds[i])
    workbook.close()
else:
    print("nRoof != nGeom")
          