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

data = {}
#Methanol + oxygen
cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 170")
data['ch'] = np.array(cursor.fetchall())

axis_array = []
fig = plt.figure()
fig.subplots_adjust(bottom=0.15) # Make room for x-label

LINEWIDTH = 0.5

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
axis.set_xlim(16.91,17.03)
axis.set_ylim(0,4)
axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)



#plt.tight_layout()
plt.show()
plt.savefig('../untreated_data.png',dpi=300)