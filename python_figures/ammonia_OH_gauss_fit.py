import matplotlib
from scipy import optimize
import math
#matplotlib.use('svg')
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb
import sys

def TimeToMass(time):
    corr_time = time - 0.181  #Approximate delay
    mass = (corr_time / 2.98660484819)**(1.0/0.4977024241071)
    return mass

matplotlib.rc('text',usetex=True) # Magic fix for the font warnings

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

fig = plt.figure()
fig.subplots_adjust(bottom=0.2) # Make room for x-label
fig.subplots_adjust(top=0.8) # Make room for extra x-label
ratio = 0.4                     # This figure should be very wide to span two columns
fig_width = 10
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)


#Relevant time, OH: 12.418, NH3: 12.427
data = {}
#cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 245")
cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 427")
Data = np.array(cursor.fetchall())

masses = []
masses.append(['OH',12.413,6])
masses.append(['NH3',12.424,6])

fit = []

#X_range = Data[24600:25000,0]
X_range = np.arange(12.405,12.44,0.0001)

i = 0
axis = fig.add_subplot(1,1,1)
for mass in masses:
    i = i + 1
    
    center = (int)(mass[1] * 2000) ## Notice... 
    center_mass = mass[1]
    Start = center -50 #Display range
    End = center + 50
    start = center - mass[2] #Fitting range
    end = center + mass[2]

    offset = min(Data[Start:End,1])
    x_values = Data[start:end,0]
    y_values = Data[start:end,1]-offset
    X_values = Data[Start:End,0]
    Y_values = Data[Start:End,1]-offset
    
    # Fit the first set
    fitfunc = lambda p, x: p[0]*math.e**(-1*((x-center_mass-p[2])**2)/p[1])       # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    p0 = [50,0.00001,0] # Initial guess for the parameters
    p1, success = optimize.leastsq(errfunc, p0[:], args=(x_values, y_values),maxfev=1000)        

    if (success > 4) or p1[1]>0.01:
        p0 = [5,0.00001,0]
        p1, success = optimize.leastsq(errfunc, p0[:], args=(x_values[2:5], y_values[2:5]))
   
    if success > 4 or p1[1]>0.01 or p1[1]<0:
        print "p1:" + str(p1[0]) + " p1:" + str(p1[1]) + " p2:" + str(p1[2]) + " j: " + str(j)
        p1[1] = 0

    
    axis.plot(X_range,fitfunc(p1, X_range),'r--',linewidth=1.1)
    fit.append(fitfunc(p1, X_range))


axis.plot(X_range,fit[0]+fit[1],'g-',linewidth=0.5)
axis.plot(X_values,Y_values,'b.',markersize=1.5)
axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis.set_yticks((20,40,60))    
axis.set_xticks((12.41,12.42,12.43,12.44))    
axis.ticklabel_format(useOffset=False)
axis.set_xlim(12.405,12.435)
axis.set_ylabel('Response / mV', fontsize=8)
axis.set_xlabel('Flight Time / $\mu$s', fontsize=8)


arrow = dict(facecolor='black',arrowstyle='->')
font = 8
axis.annotate('OH', xy=(12.413, 60),  xycoords='data', xytext=(12.408, 50), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('NH$_3$', xy=(12.426, 40),  xycoords='data', xytext=(12.431, 50), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)



axis3 = axis.twiny()
axis3.plot(TimeToMass(X_range),X_range*0,'w-',linewidth=0) #Hack to create an invisible set on the extra x-axis
axis3.set_xlim(TimeToMass(12.405),TimeToMass(12.44))
#axis3.set_xticks((12.41,12.42,12.43,12.44))    
axis3.set_xlabel('Mass / amu', fontsize=8)
axis3.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis3.ticklabel_format(useOffset=False)


#plt.tight_layout()
#plt.show()
plt.savefig('../ammonia_OH_gauss_fit.png',dpi=300)
