import xlrd
from shutil import copyfile


book = xlrd.open_workbook("Label/labelsOrien.xlsx") # in my case the directory contains the excel file named excel.xls

# Now to print the number of worksheets in the excel file 
print ("The number of worksheets are ", book.nsheets)

# Choose a specific workbook to import data 
sheet = book.sheet_by_index(0)


for i in range(0,sheet.nrows):
    imgName = "img_%s.png" % (i)
    imgPath = "Image/" + imgName
    
    if(i%4 == 0):
        trainingStep = "Validation/"
    else:
        trainingStep = "Training/"
    
    if(sheet.cell_value(i,0) == "flat" or sheet.cell_value(i,0) == "falt"):
        copyfile(imgPath, "ImageRoofType/" + trainingStep + "Flat/" + imgName)
    elif(sheet.cell_value(i,0) == "gabled"):
        copyfile(imgPath, "ImageRoofType/" + trainingStep + "Gabled/" + imgName)
    elif(sheet.cell_value(i,0) == "half-hipped" or sheet.cell_value(i,0) == "half_hipped"):
        copyfile(imgPath, "ImageRoofType/" + trainingStep + "HalfHipped/" + imgName)    
    elif(sheet.cell_value(i,0) == "hipped"):
        copyfile(imgPath, "ImageRoofType/" + trainingStep + "Hipped/" + imgName)
    elif(sheet.cell_value(i,0) == "mansard" or sheet.cell_value(i,0) == "gambrel" or sheet.cell_value(i,0) == "gimbrel"):
        copyfile(imgPath, "ImageRoofType/" + trainingStep + "Mansard/" + imgName)
    elif(sheet.cell_value(i,0) == "pyramid" or sheet.cell_value(i,0) == "pyramidal"):
        copyfile(imgPath, "ImageRoofType/" + trainingStep + "Pyramid/" + imgName)    
    elif(sheet.cell_value(i,0) == "round"):
        copyfile(imgPath, "ImageRoofType/" + trainingStep + "Round/" + imgName)
