import xml.etree.ElementTree as ET
import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import griddata

def get_files(dir_path):
    # folder path
    file_paths = []
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
            filepath = os.path.join(dir_path, path)
            file_paths.append(filepath) 
    return count,file_paths

def files_into_array(count,file_paths):
    final_data=[]
    for path in file_paths:
        temp=readSpe(path)
        wavelengths=temp.wavelengths
        temp=np.array(temp.data)
        wavelengths=np.array(wavelengths) #Extratcs the wavelegnths
        intensities=np.zeros(2048)
        for j in range(2048):
            intensities[j]=np.average(temp[0,0,:,j])
        final_data.append(intensities)
    final_data.append(wavelengths)
    return final_data

def plot_data(data,names):
    guide=len(data)
    for i in range(guide-1):
        temp=data[i]
        wavelengths=data[guide-1]
        plt.plot(wavelengths,temp,label=names[i][61:68])
    plt.title("Wavelength Intensities")
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Intensity (a.u)")
    plt.legend()
    
class ROI:
    def __init__(self,width,height,stride):
        self.width=width
        self.height=height
        self.stride=stride
        
class dataContainer:
    def __init__(self,data,**kwargs):
        self.data=data
        self.__dict__.update(kwargs)
        
def readSpe(filePath):
    dataTypes = {'MonochromeUnsigned16':np.uint16, 'MonochromeUnsigned32':np.uint32, 'MonochromeFloating32':np.float32}
    
    with open(filePath) as f:
        f.seek(678)
        xmlLoc = np.fromfile(f,dtype=np.uint64,count=1)[0]
        f.seek(1992)
        speVer = np.fromfile(f,dtype=np.float32,count=1)[0]
    
    if speVer==3:
        with open(filePath, encoding="utf8") as f:
            f.seek(xmlLoc)
            xmlFooter = f.read()
            xmlRoot = ET.fromstring(xmlFooter)            
            #print(xmlRoot[0][0].attrib)
            readoutStride=np.int((xmlRoot[0][0].attrib)['stride'])
            numFrames=np.int((xmlRoot[0][0].attrib)['count'])
            pixFormat=(xmlRoot[0][0].attrib)['pixelFormat']
            #find number of regions
            #regions = list(xmlRoot[0][0])
            regionList=list()
            for child in xmlRoot[0][0]:
                regStride=np.int((child.attrib)['stride'])
                regWidth=np.int((child.attrib)['width'])
                regHeight=np.int((child.attrib)['height'])
                regionList.append(ROI(regWidth,regHeight,regStride))
            dataList=list()
            regionOffset=0
            
            #read entire datablock
            f.seek(0)
            bpp = np.dtype(dataTypes[pixFormat]).itemsize
            numPixels = np.int((xmlLoc-4100)/bpp)  
            totalBlock = np.fromfile(f,dtype=dataTypes[pixFormat],count=numPixels,offset=4100)
            for i in range(0,len(regionList)):
                offLen=list()                
                if i>0:
                    regionOffset += (regionList[i-1].stride)/bpp                    
                for j in range(0,numFrames):
                    offLen.append((np.int(regionOffset+(j*readoutStride/bpp)),regionList[i].width*regionList[i].height))     
                regionData = np.concatenate([totalBlock[offset:offset+length] for offset,length in offLen])
                dataList.append(np.reshape(regionData,(numFrames,regionList[i].height,regionList[i].width),order='C'))

            calFlag=False                
            for child in xmlRoot[1]:
                if 'Wavelength' in child.tag:
                    if 'Error' in child[0].tag:     #handle the case where errors are reported in pair with the WL
                        wavelengths = np.array([])
                        wlText = child[0].text.rsplit()
                        for elem in wlText:
                            wavelengths = np.append(wavelengths,np.fromstring(elem,sep=',')[0])
                    else:
                        wavelengths=np.fromstring(child[0].text,sep=',')
                    calFlag=True
                if 'SensorMapping' in child.tag and calFlag==True:
                    startX = int(child.attrib['x'])
                    xWidth = int(child.attrib['width'])
                    wavelengths = wavelengths[startX:(startX+xWidth)]                
            if calFlag==False:
                totalData=dataContainer(dataList,xmlFooter=xmlFooter)
            else:
                totalData=dataContainer(dataList,xmlFooter=xmlFooter,wavelengths=wavelengths)
            return totalData

        
    elif speVer<3:
        dataTypes2 = {0:np.float32, 1:np.int32, 2:np.int16, 3:np.uint16, 5:np.float64, 6:np.uint8, 8:np.uint32}
        with open(filePath, encoding="utf8") as f:
            f.seek(108)
            datatype=np.fromfile(f,dtype=np.int16,count=1)[0]
            f.seek(42)
            frameWidth=np.int(np.fromfile(f,dtype=np.uint16,count=1)[0])
            f.seek(656)
            frameHeight=np.int(np.fromfile(f,dtype=np.uint16,count=1)[0])
            f.seek(1446)
            numFrames=np.fromfile(f,dtype=np.int32,count=1)[0]
            numPixels = frameWidth*frameHeight*numFrames
            bpp = np.dtype(dataTypes2[datatype]).itemsize
            dataList=list()            
            f.seek(0)
            totalBlock = np.fromfile(f,dtype=dataTypes2[datatype],count=numPixels,offset=4100)
            offLen=list()
            for j in range(0,numFrames):
                offLen.append((np.int((j*frameWidth*frameHeight)),frameWidth*frameHeight))
            regionData = np.concatenate([totalBlock[offset:offset+length] for offset,length in offLen])
            dataList.append(np.reshape(regionData,(numFrames,frameHeight,frameWidth),order='C'))
            totalData=dataContainer(dataList)
            return totalData

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def find_maximums(data):
    guide=len(data)
    alfa=guide-1
    maximums=[]
    for f in range(guide-1):
        temp=data[f]
        wavelengths=data[alfa]
        max=temp.max()
        location=np.where(temp==max)
        location=location[0][0]
        data_final=[temp[location],wavelengths[location]]
        maximums.append(data_final)
    return maximums

def plot_maximums(maximums):
    maximums=np.array(maximums)
    plt.scatter(maximums[:,1],maximums[:,0])
    guide=maximums.shape[0]
    for i in range(guide):
        plt.text(maximums[i,1],maximums[i,0],f'{round(maximums[i,1],3)} nm',fontsize=7)

def pump_power_density(fwhm,pump_power,loss_ratio,pump_avereging):
    """
    

    Parameters
    ----------
    fwhm : Float
        Beam spto size, should be in um.
    pump_power : Float
        Raw power read in the powermeter, should be in uW.
    loss_ratio : Float
        Loss between all the optics from the source till the objective.
    pump_avereging : Float
        Propreties of the pulsed laser.

    Returns
    -------
    peak : Float
        Returns.

    """
    
    peak=(((pump_power/loss_ratio)*pump_avereging)*10**(-12))/(np.pi*((fwhm*10**(-4))/2)**2)
    peak=np.round(peak,2)
    return peak