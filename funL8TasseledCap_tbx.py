#           B2      B3       B4      B5  B6   B7
#Brightness 0.3029 0.2786 0.4733 0.5599 0.508 0.1872
#Greenness -0.2941 -0.243 -0.5424 0.7276 0.0713 -0.1608
#Wetness 0.1511 0.1973 0.3283 0.3407 -0.7117 -0.4559
#TCT4 -0.8239 0.0849 0.4396 -0.058 0.2013 -0.2773
#TCT5 -0.3294 0.0557 0.1056 0.1855 -0.4349 0.8085
#TCT6 0.1079 -0.9023 0.4119 0.0575 -0.0259 0.0252
#
#  Tasseled Cap Transform Coefficients from:
# Muhammad Hasan Ali Baig, Lifu Zhang, Tong Shuai & Qingxi Tong (2014)
#Derivation of a tasselled cap transformation based on Landsat 8 at-satellite reflectance, Remote
#Sensing Letters, 5:5, 423-431, DOI: 10.1080/2150704X.2014.915434

import os, arcpy
arcpy.CheckOutExtension("Spatial")

inputL8Directory = arcpy.GetParameterAsText(0)
full = arcpy.GetParameterAsText(1)

#######################################################################
def tbxPrint(fBad,inStr):
    '''a general purpose function for try/except printing
    inside a toolbox function'''
    try:
        arcpy.AddMessage(inStr)
        #fBad.write(inStr)
    except:
        print inStr
    finally:
        pass
        #fBad.write(inStr+"\n")
#######################################################################

def L8_TCT(inputL8Directory, full):
    '''     Tasseled Cap Transform for L8 OLI data  (from Baig et al 2015)
            see citation in source 
        INPUT:   1) <inputL8Directory> a directory of L8 OLI (full set, not Color Look)
                 optional
                 2) <full = True/False> Calculate all 6 bands
                  
        
    '''            #      B2        B3    B4      B5      B6       B7
    coeffBrightness = ( 0.3029,  0.2786 ,0.4733 ,0.5599 , 0.508 ,  0.1872)
    coeffGreenness =  (-0.2941, -0.243, -0.5424, 0.7276,  0.0713, -0.1608)
    coeffWetness =    ( 0.1511,  0.1973, 0.3283, 0.3407, -0.7117, -0.4559)
    coeffTCT4 =       ( -0.8239, 0.0849, 0.4396, -0.058,  0.2013 ,-0.2773)
    coeffTCT5 =       ( -0.3294, 0.0557, 0.1056, 0.1855 ,-0.4349 , 0.8085)
    coeffTCT6 =       (  0.1079,-0.9023, 0.4119 ,0.0575 ,-0.0259 , 0.0252)
    
    import os, arcpy
    arcpy.CheckOutExtension("Spatial")
    #check directory
    os.chdir(inputL8Directory)
    arcpy.env.workspace = inputL8Directory
    
    arcpy.env.overwriteOutput = True
    
    folderName = os.path.split(inputL8Directory)[1]
    start = folderName.index('LC8')
    l8Code = folderName[start:start+21]
    
    listDir = os.listdir('.')
    print listDir
    listBands = []
    for items in listDir:
        if items.endswith("_B1.TIF"):
            B1 = arcpy.Raster(items)
            listBands.append('B1')
    
        if items.endswith("_B2.TIF"): 
            B2 = arcpy.Raster(items)
            listBands.append('B2')

        if items.endswith("_B3.TIF"):
            B3 = arcpy.Raster(items)
            listBands.append('B3')
            
        if items.endswith("_B4.TIF"):
            B4 = arcpy.Raster(items)
            listBands.append('B4')
            
        if items.endswith("_B5.TIF"):
            B5 = arcpy.Raster(items)
            listBands.append('B5')
            
        if items.endswith("_B6.TIF"):
            B6 = arcpy.Raster(items)
            listBands.append('B6')
            
        if items.endswith("_B7.TIF"):
            B7 = arcpy.Raster(items)
            listBands.append('B7')
            
        if items.endswith("_B8.TIF"):
            B8 = arcpy.Raster(items)   
            listBands.append('B8')
            
        if items.endswith("_B9.TIF"):
            B9 = arcpy.Raster(items)
            listBands.append('B9')
            
        if items.endswith("_B10.TIF"):
            B10 = arcpy.Raster(items)
            listBands.append('B10')
            
        if items.endswith("_B11.TIF"):
            B11 = arcpy.Raster(items)         
            listBands.append('B11')
            
        if items.endswith("_BQA.TIF"):
            BQA = arcpy.Raster(items)         
            listBands.append('BQA')
            
    listBands2 = ['B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','BQA']
    
    for items in listBands2:
        if items in listBands:
            pass
        else:  print items
    
    for band in listBands:
        if band == None:
            print "Error:  Band" 
    #  Do Transform
    arcpy.env.snapRaster = B1
    print "calculating Brightness ..."
    rasBrightness = B2*coeffBrightness[0] + B3*coeffBrightness[1] + B4*coeffBrightness[2] \
                    + B5*coeffBrightness[3] + B6*coeffBrightness[4] + B7*coeffBrightness[5]
    print "calculating Greenness ..."                
    rasGreenness = B2*coeffGreenness[0] + B3*coeffGreenness[1] + B4*coeffGreenness[2] \
                    + B5*coeffGreenness[3] + B6*coeffGreenness[4] + B7*coeffGreenness[5]
    print "calculating Wetness ..."                
    rasWetness = B2*coeffWetness[0] + B3*coeffWetness[1] + B4*coeffWetness[2] \
                    + B5*coeffWetness[3] + B6*coeffWetness[4] + B7*coeffWetness[5]
    if full:
        print "calculating TCT4 ..."                 
        rasTCT4 = B2*coeffTCT4[0] + B3*coeffTCT4[1] + B4*coeffTCT4[2] \
                        + B5*coeffTCT4[3] + B6*coeffTCT4[4] + B7*coeffTCT4[5]
        print "calculating TCT5 ..."                      
        rasTCT5 = B2*coeffTCT5[0] + B3*coeffTCT5[1] + B4*coeffTCT5[2] \
                        + B5*coeffTCT5[3] + B6*coeffTCT5[4] + B7*coeffTCT5[5]
        print "calculating TCT6 ..."                      
        rasTCT6 = B2*coeffTCT6[0] + B3*coeffTCT6[1] + B4*coeffTCT6[2] \
                        + B5*coeffTCT6[3] + B6*coeffTCT6[4] + B7*coeffTCT6[5]
    
    rasBrightness.save(l8Code+'_Brightness.tif')
    rasGreenness.save(l8Code+'_Greenness.tif')
    rasWetness.save(l8Code+'_Wetness.tif')
    if full:
        rasTCT4.save(l8Code+'_rasTCT4.tif')
        rasTCT5.save(l8Code+'_rasTCT5.tif')
        rasTCT6.save(l8Code+'_rasTCT6.tif')
    arcpy.SetParameterAsText(2,rasBrightness)
    arcpy.SetParameterAsText(3,rasGreenness)
    arcpy.SetParameterAsText(4,rasWetness)
    arcpy.SetParameterAsText(5,rasTCT4)
    arcpy.SetParameterAsText(6,rasTCT5)
    arcpy.SetParameterAsText(7,rasTCT6)     
    
L8_TCT(inputL8Directory,full)



