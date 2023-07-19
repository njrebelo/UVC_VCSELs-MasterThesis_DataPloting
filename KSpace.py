from needed_imports import *
import matplotlib.pyplot as plt
import numpy as np

folder_path="Z:\\UVC VCSELs\\Carrier Chips\\CC1_X0187-2\\PL\\X0187-2_CC1_KS\\PLs"
count,file_paths=get_files(folder_path)
angleaxis=np.arange(0,512,120)
wavelenghtaxis=np.arange(0,2047,75)
yaxis=np.zeros(len((wavelenghtaxis)))


for i in range(count):
    filename=file_paths[i]
    if ".spe" in filename: 
        file_tag=filename[65:96]
        data=readSpe(filename)
        wavelengths=data.wavelengths
        data=np.array(data.data)
        data=data[0,0,:,:]
        wavelengths=np.array(wavelengths) #Extratcs the wavelegnths
    
        for j in range(len(wavelenghtaxis)):
            yaxis[j]=round(wavelengths[wavelenghtaxis[j]],2)
        
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if (data[i,j]<=0):
                    data[i,j]=1
        
        #plt.imshow(data, cmap='jet', interpolation='nearest')
        plt.imshow(data, cmap='jet', interpolation='bicubic',norm=matplotlib.colors.LogNorm())
        #plt.title("VCSEL "+file_tag,size=8)
        plt.title("CC1 VCSEL Z3-5")
        plt.xlabel("Wavelength [nm]",size=7)
        plt.ylabel("Angle [°]",size=7)
        #plt.axis('off')
    
        #Axis
        plt.xticks(wavelenghtaxis,yaxis,size=8)
        plt.xlim(300,700)
        #plt.yticks([])
        plt.yticks(angleaxis,["-20°","-10°","0°","10°","20°"],size=8)
        plt.ylim(100,375)
        #plt.annotate("1.1MW/$cm^{2}$",(1680,500),color='white',size=5)
        plt.colorbar(shrink=0.7)
        
        #plt.savefig(filename+".png")
        plt.show()