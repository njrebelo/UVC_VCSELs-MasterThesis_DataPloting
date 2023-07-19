import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_directory="X:\\UVC VCSEL (Nelson and Estrella)\\Processing\\11-TopDBR\\Reflectance spectrum\\Tool113\\X0187-2_CC2\\"+"Z3-5.csv"
#label_data=np.loadtxt(file_directory)
label_data=np.genfromtxt(file_directory,delimiter=";",dtype="float")

#label_x=label_data[0,0]
#label_y=label_data[0,1]

#Specific to making mA into uA
label_y="Reflectivity [%]"

#kernel_size = 11
#kernel = np.ones(kernel_size) / kernel_size
#data = np.delete(data,0,0)
#data_convolve = np.convolve(data[:,1], kernel, mode='same')
#data_convolve=data[:,1]
#Specific to making mA into uA
#data_convolve=data_convolve*1000

def find_in_array(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def annot(array,x, ax=None):
    array_x=array[:,0]
    array_y=array[:,1]
    x_ind = find_in_array(array_x, x)
    xmax = array_x[x_ind]
    ymax = array_y[x_ind]
    text= f"R={np.round(ymax,decimals=2)}% @$\lambda$:{np.round(xmax,decimals=2)}nm".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=145,angleB=-15")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.70,0.80), **kw)
    
def annot_max(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = y.max()
    text= f"R={np.round(ymax,decimals=2)}% @$\lambda$:{np.round(xmax,decimals=2)}nm".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=145,angleB=130")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.70,0.80), **kw)



plt.plot(label_data[:,0],label_data[:,1])
plt.title("Top DBR X0187 Z3-5")
plt.xlim((220,400))
plt.ylim((0,100))
plt.ylabel("Reflectivity(%)")
plt.xlabel("Wavelength[nm]")



#annot_max(label_data[:,0],label_data[:,1])
annot(label_data,275)

plt.savefig("X0187_BottomDBR_Center_Reflectivity.png")