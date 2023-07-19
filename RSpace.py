from needed_imports import *
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

folder_path="C:\\Users\\rebelo\\Desktop\\X0148-6_CC8"
count,file_paths=get_files(folder_path)
angleaxis=np.arange(0,512,120)


for i in range(count):
    filename=file_paths[i]
    file_tag=filename[36:53]
    data=readSpe(filename)
    #wavelengths=data.wavelengths
    data=np.array(data.data)
    data=data[0,0,:,:]
    #wavelengths=np.array(wavelengths) #Extratcs the wavelegnths

    plt.imshow(data, cmap='jet', interpolation='nearest')
    plt.title(file_tag)
    #plt.xlabel("Wavelength")
    #plt.ylabel("Angle")
    #plt.axis('off')
    plt.xlim(700,1300)
    #Axis
    plt.xticks([])
    plt.yticks([])
    #plt.yticks(angleaxis,["0°","5°","10°","15°","20°"])
    plt.annotate("1.1MW/$cm^{2}$",(1150,500),color='white')
    plt.colorbar(label="Optical intensity (a.u)")
    plt.savefig(filename+".png")
    plt.show()
