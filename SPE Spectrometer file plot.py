from needed_imports import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import chirp, find_peaks, peak_widths
import mpld3


filename="Z:\\UVC VCSELs\\Carrier Chips\\CC1_X0187-2\\PL\\Z2-18\\"
filename=filename+"Z2-18_10uW 2023 March 22 16_20_38.spe"
chip_name=filename[38:45]

data=readSpe(filename)
label=filename[0:7]
wavelengths=data.wavelengths
data=np.array(data.data)
data=data[0,0,:,:]
wavelengths=np.array(wavelengths) #Extratcs the wavelegnths
intensities=np.zeros(2048)


for k in range(2048):
	intensities[k]=np.average(data[:,k])
    

def fwhm(intensities,wavelength):
    maximum=intensities.max()
    max_pos=int(np.array(np.where(intensities==find_nearest( intensities,intensities.max() ))))
    max_peak=wavelengths[max_pos]
    right_half=int(np.array(np.where(intensities==find_nearest( intensities[0:max_pos:1],(maximum/2) ))))
    right_half_pos=wavelengths[right_half]
    
    left_half=int(np.array(np.where(intensities==find_nearest( intensities[max_pos:intensities.size:1],(maximum/2) ))))
    left_half_pos=wavelengths[left_half]
    output=[max_peak,right_half_pos,left_half_pos,np.round(left_half_pos-right_half_pos,3)]
    
    plt.annotate("", xy=(left_half_pos+5, intensities[left_half]), xytext=(left_half_pos, intensities[left_half]),arrowprops=dict(arrowstyle="<-"))
    plt.annotate("", xy=(right_half_pos-5, intensities[right_half]), xytext=(right_half_pos, intensities[right_half]),arrowprops=dict(arrowstyle="<-"))
    
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(xycoords='data',textcoords="axes points", bbox=bbox_props, ha="right", va="top")
    plt.annotate(f"FWMH:{np.round(left_half_pos-right_half_pos,3)}nm", xy=(left_half_pos, intensities[left_half]), xytext=(left_half_pos+5, 120), **kw)
    
    
    return output

  
plt.plot(wavelengths,intensities)

#fwhm=fwhm(intensities,wavelengths)
#print(fwhm)

plt.xlim(274.75,275.30)
plt.title("X0187 Bare Epi at "+chip_name.translate({ord(i): '' for i in '_uWR'})+"uW\cm$^2$")
plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity (a.u)")
#plt.yscale("log")