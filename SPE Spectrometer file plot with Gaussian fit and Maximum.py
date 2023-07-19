from needed_imports import *
import matplotlib.pyplot as plt
from numpy import exp, linspace, random, sqrt, pi
from scipy.optimize import curve_fit
from lmfit import Model
from lmfit.models import GaussianModel,SkewedGaussianModel,DoniachModel,VoigtModel

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
	intensities[k]=np.sum(data[:,k])+820

# Recast xdata and ydata into numpy arrays so we can use their handy features
x=wavelengths
y = intensities

model = SkewedGaussianModel()
params = model.guess(y, x=x)
result = model.fit(y, params, x=x)
print(result.fit_report())

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
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.34,0.96), **kw)


plt.plot(x, y, label="Raw Data")
plt.plot(x, result.best_fit, '--', label='Gaussian Fit')
annot_max(x,result.best_fit)


def fwhm(intensities,wavelength):
    maximum=intensities.max()
    max_pos=int(np.array(np.where(intensities==find_nearest( intensities,intensities.max() ))))
    max_peak=wavelengths[max_pos]
    right_half=int(np.array(np.where(intensities==find_nearest( intensities[0:max_pos:1],(maximum/2) ))))
    right_half_pos=wavelengths[right_half]
    
    left_half=int(np.array(np.where(intensities==find_nearest( intensities[max_pos:intensities.size:1],(maximum/2) ))))
    left_half_pos=wavelengths[left_half]
    output=[max_peak,right_half_pos,left_half_pos,np.round(left_half_pos-right_half_pos,3)]
    
    plt.annotate("", xy=(left_half_pos+0.5, intensities[left_half]), xytext=(left_half_pos, intensities[left_half]),arrowprops=dict(arrowstyle="<-"))
    plt.annotate("", xy=(right_half_pos-0.5, intensities[right_half]), xytext=(right_half_pos, intensities[right_half]),arrowprops=dict(arrowstyle="<-"))
    
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(xycoords='data',textcoords="axes points", bbox=bbox_props, ha="right", va="top")
    plt.annotate(f"FWMH:{np.round(left_half_pos-right_half_pos,3)}nm", xy=(left_half_pos, intensities[left_half]), xytext=(left_half_pos+5, 120), **kw)
    
    
    return output

fwhm=fwhm(intensities,wavelengths)
print(fwhm)

plt.legend()
plt.xlim(274,276)

#power=float(chip_name.translate({ord(i): '' for i in '_uWR'}))
power=10
pump_power=pump_power_density(10,power,2.38,2162162)

title=f"CC1 VCSEL Z2-18 at {pump_power} MW\cm$^2$"
plt.title(title)
plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity (a.u)")
#plt.ylim(800,300000)
#plt.yscale("log")

Model=str(model).translate({ord(i): '' for i in '><lmfit.Model(): '})
#plt.savefig(folder+title[0:(len(title)-10)]+"_uWcm2_"+Model+".png")