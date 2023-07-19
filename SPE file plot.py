from needed_imports import *
import matplotlib.pyplot as plt
import numpy as np
import mpld3

folder_path="Z:\\UVC VCSELs\\Half-cavities\\CC7_X0187-5\\PL"
count,file_paths=get_files(folder_path)
angleaxis=np.arange(0,512,120)


for i in range(count):
    filename=file_paths[i]
    if ".spe" in filename:
        file_tag=filename[39:47]
        data=readSpe(filename)
        label=filename[0:7]
        wavelengths=data.wavelengths
        data=np.array(data.data)
        data=data[0,0,:,:]
        wavelengths=np.array(wavelengths) #Extratcs the wavelegnths

        plt.imshow(data, cmap='jet', interpolation='spline16')
        plt.title(filename[70:76].translate({ord(i): ' ' for i in '_'}))
    #plt.xlabel("Wavelength")
    #plt.ylabel("Angle")
    
    #plt.axis('off')
    #plt.xlim(800,1200)
    #plt.ylim(400,0)
    #Axis
    plt.xticks([])
    plt.yticks([])
    #plt.yticks(angleaxis,["0°","5°","10°","15°","20°"])
    #plt.colorbar(label="Optical intensity (a.u)")
    #plt.savefig(filename+".png")
    plt.show()
