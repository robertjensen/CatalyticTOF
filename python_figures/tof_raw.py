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
def MassToTime(mass):
    time = 2.9870925856 * (mass**0.497621653202)
    corr_time = time + 0.207
    return corr_time


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
axis.set_ylim(0,20)
axis.set_xlim(0,20)
axis.set_xticks([2.5,5,7.5,10,12.5,15,17.5,20])

mass_ticks = np.array([1,5,10,15,20,25,30,35,40])

axis3 = axis.twiny()
#axis3.plot(data['ch'][:,0],data['ch'][:,0]*0,'w-',linewidth=0) #Hack to create an invisible set on the extra x-axis
axis3.set_xlim(0,20)
print MassToTime(32.0262147)
axis3.set_xticks(MassToTime(mass_ticks))
axis3.set_xticklabels(mass_ticks)
axis3.set_xlabel('Mass / amu', fontsize=8)
axis3.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=3)
#axis3.ticklabel_format(useOffset=False)

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
axis.set_xticks([0.2,0.4,0.6,0.8])
axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)


axis = plt.subplot(gs[1,1])
axis.set_ylabel('')
axis.set_yticks((0,1,2,3,4))
#axis.set_xticks((12,12.5))
axis.plot(data['ch'][:,0], data['ch'][:,1], 'r-',linewidth=LINEWIDTH)
axis.set_xlim(12,13)
axis.set_ylim(0,4)
axis.set_xticks([12.2,12.4,12.6,12.8])
axis.set_xlabel('Flight Time / $\mu$s', fontsize=8)
p = axis.axvspan(11.45, 13, facecolor='#b6fa77', alpha=0.25)
axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis.annotate('H$_2$O', xy=(12.75, 2.3),  xycoords='data', xytext=(12.65, 3.3), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('OH', xy=(12.4, 1),  xycoords='data', xytext=(12.7, 1.8), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('O', xy=(12.05, 0.9),  xycoords='data', xytext=(12.26, 1.4), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)


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