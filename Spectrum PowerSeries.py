from needed_imports import *
import matplotlib.pyplot as plt
import numpy as np

folder_path="Z:\\UVC VCSELs\\Carrier Chips\\CC1_X0187-2\\PL\\Z1-11"
count,file_paths=get_files(folder_path)
chip_name="CC1"
intensities=np.zeros(2048)


def annot_max(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = y.max()
    text= "$\lambda$={:.3f}nm".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=10")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.30,0.96), **kw)


for i in range(count):
    filename=file_paths[i]
    if ".spe" in filename: 
        laser_tag=filename[54:58]
        power=float(laser_tag.translate({ord(i): None for i in 'uW_RSm'}).translate({ord(i): "." for i in 'p'}))
        print(f"tag:{laser_tag} {power}mW")
    
        data=readSpe(filename)
        wavelengths=data.wavelengths
        data=np.array(data.data)
        data=data[0,0,:,:]
        data=data[200:280:1,:]
        wavelengths=np.array(wavelengths) #Extratcs the wavelegnths
    
        pump_power=pump_power_density(10,power,2.38,2162162)
    
    
        for k in range(2048):
            intensities[k]=np.average(data[:,k])
        plt.plot(wavelengths,intensities, label=(f"{pump_power}MW/$cm^{2}$"))
        if i==3:
            y=intensities
            x=wavelengths
            annot_max(x, y)
            print(y)


plt.title("Power Series: "+chip_name.translate({ord(i): ' ' for i in '_'})+" VCSEL "+filename[49:54].translate({ord(i): ' ' for i in '_'}))
plt.xlabel("Wavelength (nm)")
plt.ylabel("Integral Intensity (a.u)")
#plt.yscale("log")
#plt.ylim((0,5000))
plt.xlim(275,276.5) #region of interest

handles, labels=plt.gca().get_legend_handles_labels()
order = [3,2,1,0]
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])
#plt.legend()

plt.savefig(filename+".png")
plt.show()

#Detec the peak and give the FWHM