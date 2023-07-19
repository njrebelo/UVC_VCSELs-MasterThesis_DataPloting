from needed_imports import *
import matplotlib.pyplot as plt
import numpy as np

folder_path="Z:\\UVC VCSELs\\Carrier Chips\\CC1_X0187-2\\PL\\Z2-18"
count,file_paths=get_files(folder_path)
experiment_data=np.zeros((count,2))
chip_name=folder_path[29:39]
intensities=np.zeros(2048)

first_y=274.8
second_y=275.2

for i in range(count):
    filename=file_paths[i]
    if ".spe" in filename: 
    
        laser_tag=filename[55:59]
        power=float(laser_tag.translate({ord(i): None for i in 'uWm_'}).translate({ord(i): "." for i in 'p'}))
    
        data=readSpe(filename)
        wavelengths=data.wavelengths
        data=np.array(data.data)
        data=data[0,0,:,:]
        data=data[274:276:1,:]
        wavelengths=np.array(wavelengths) #Extratcs the wavelegnths
        
        pump_power=pump_power_density(10,power,2.38,2162162)
        experiment_data[i,0]=pump_power
        print(f"{laser_tag} {power} {pump_power}")
        
        
        for k in range(2048):
            intensities[k]=np.average(data[:,k])
            
            first_lambda=int(np.array(np.where(wavelengths==find_nearest( wavelengths,first_y ))))
            second_lambda=int(np.array(np.where(wavelengths==find_nearest( wavelengths,second_y ))))
            experiment_data[i,1]=np.trapz(intensities[first_lambda:second_lambda:1])
                 
experiment_data=np.sort(experiment_data,axis=0)
plt.scatter(experiment_data[:,0],experiment_data[:,1],marker="o")
print(experiment_data)

#Linear Fits
lim0=2
lim1=5
m_1, b_1=np.polyfit(experiment_data[lim0:lim1:1,0],experiment_data[lim0:lim1:1,1],1)
plt.plot(experiment_data[lim0:(lim1+1):1,0],m_1*experiment_data[lim0:(lim1+1):1,0]+b_1,ls=":")

#Linear Fits
lim2=experiment_data.shape[0]-1
m_2, b_2=np.polyfit(experiment_data[lim1-1:(lim2+1):1,0],experiment_data[lim1-1:(lim2+1):1,1],1)
plt.plot(experiment_data[(lim1-2):(lim2+1):1,0],m_2*experiment_data[(lim1-2):(lim2+1):1,0]+b_2,ls=":")


plt.title(chip_name.translate({ord(i): ' ' for i in '_'})+" "+laser_tag[0:5].translate({ord(i): ' ' for i in '_'}))
plt.title("Z3-5 at 275.9nm")
plt.xlabel("Pump Power Density (MW/$cm^{2}$)")
plt.ylabel("Integral Intensity (a.u)")
#plt.yscale("log")
plt.xlim((3,12)) #region of interest
#plt.ylim((-100,800000))
#plt.legend()
#plt.yticks([])
plt.show()

#Detec the peak and give the FWHM