import matplotlib
#matplotlib.use('svg')
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import MySQLdb

matplotlib.rc('text',usetex=True) # Magic fix for the font warnings

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

#SOMETHING WRONG WITH THE X-SCALE!!!!

#Mass of methanol: 32.0262147
#Mass of oxygen: 31.9898292
def TimeToMass(time):
    #time = 2.9870925856 * mass^0.497621653202
    #corr_time = time - 0.183  #Approximate delay - not optimized for this spectrum
    mass = (time / 2.9870925856)**(1.0/0.497621653202)
    #mass = mass - 0.413085820678 # Approximate value, not optimized for this spectrum
    return mass

print TimeToMass(20)
data = {}
#Methanol + oxygen
cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 170")
data['ch'] = np.array(cursor.fetchall())

axis_array = []
fig = plt.figure()
fig.subplots_adjust(bottom=0.15) # Make room for x-label
fig.subplots_adjust(top=0.8) # Make room for extra x-label

LINEWIDTH = 0.5
arrow = dict(facecolor='black',arrowstyle='->')
font = 8

ratio = 0.4                     # This figure should be very wide to span two columns
fig_width = 17
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

gs = gridspec.GridSpec(2, 3)
gs.update(wspace=0.2,hspace=0.2)

axis = plt.subplot(gs[0, :])

axis.plot(data['ch'][:,0], data['ch'][:,1], 'r-',linewidth=LINEWIDTH)
#xticks = range(0,20,4)
#axis.set_xticks((xticks))
axis.set_ylim(0,20)
axis.set_xlim(0,20)



axis3 = axis.twiny()
axis3.plot(TimeToMass(data['ch'][:,0]),data['ch'][:,0]*0,'w-',linewidth=0) #Hack to create an invisible set on the extra x-axis
axis3.set_xlim(TimeToMass(0),TimeToMass(20))
#axis3.set_xticks((12.41,12.42,12.43,12.44))    
axis3.set_xlabel('Mass / AMU', fontsize=8)
axis3.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=3)
#xticks = range(0,50,5)
#axis3.set_xticks((xticks))
axis3.ticklabel_format(useOffset=False)

axis.set_ylim(0,20)
axis3.set_ylim(0,20)


p = axis.axvspan(0, 1, facecolor='#26aaf7', alpha=0.25)
p = axis.axvspan(12, 13, facecolor='#b6fa77', alpha=0.25)
p = axis.axvspan(16.9, 17, facecolor='#4599a7', alpha=0.25)

axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis.set_ylabel('Response / mV', fontsize=8)
#axis.set_xlabel('Flight Time / $\mu$s', fontsize=8)
axis.set_xlabel('')



axis = plt.subplot(gs[1,0])
axis.set_ylabel('Response / mV', fontsize=8)
axis.set_yticks((0,10,20,30,40))
axis.plot(data['ch'][:,0], data['ch'][:,1], 'r-',linewidth=LINEWIDTH)
p = axis.axvspan(0, 1, facecolor='#26aaf7', alpha=0.25)
axis.set_xlim(0,1)
axis.set_ylim(0,40)
axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)


axis = plt.subplot(gs[1,1])
axis.set_ylabel('')
axis.set_yticks((0,1,2,3,4))
#axis.set_xticks((12,12.5))
axis.plot(data['ch'][:,0], data['ch'][:,1], 'r-',linewidth=LINEWIDTH)
axis.set_xlim(12,13)
axis.set_ylim(0,4)
axis.set_xlabel('Flight Time / $\mu$s', fontsize=8)
p = axis.axvspan(11.45, 13, facecolor='#b6fa77', alpha=0.25)
axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)


axis = plt.subplot(gs[1,2])
axis.set_ylabel('')
axis.set_yticks((0,1,2,3,4))
axis.set_xticks((16.95,16.97,16.99))
axis.plot(data['ch'][:,0], data['ch'][:,1], 'r-',linewidth=LINEWIDTH)
p = axis.axvspan(16.94, 17, facecolor='#4599a7', alpha=0.25)
axis.set_xlim(16.94,17)
axis.set_ylim(0,4)
axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis.ticklabel_format(useOffset=False)

axis.annotate('O$_2$', xy=(16.963, 2),  xycoords='data', xytext=(16.95, 3), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('CH$_3$OH', xy=(16.977, 1.2),  xycoords='data', xytext=(16.995, 2.4), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)



#plt.tight_layout()
plt.show()
plt.savefig('../untreated_data.png',dpi=300)