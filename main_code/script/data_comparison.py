
# Comparison of data measured from the ATI force-torque sensor (measurement f/t sensor data), 
# data obtained through nominal object dynamics (object dynamics w/o SINDy), 
# and data obtained through the equation integrating nominal object dynamics and unmodeled dynamics (object dynamics w/ SINDy).

import matplotlib.pyplot as plt
import numpy as np
from a_measurement import measurement
from a_expected import expected
from a_sindymodel import sindy
from matplotlib.font_manager import FontProperties

namef = ['force x', 'force y', 'force z', 'torque x', 'torque y', 'torque z']
namev = ['velocity_x', 'velocity_y', 'velocity_z', 'angular_vel_x', 'angular_vel_y', 'angular_velz']
namea = ['acc_x', 'acc_y', 'acc_z', 'angular_acc_x', 'angular_acc_y', 'angular_acc_z']
nameg = ['gravity_x', 'gravity_y', 'gravity_z']

def calculate_rmse(object1, object2):
    return np.sqrt(np.mean((object1 - object2) ** 2))

def calculate_BFR(sensor, sindy):
    a = np.sum((np.array(sensor) - np.array(sindy)) ** 2)
    b = np.sum((np.array(sensor) - np.mean(sindy)) ** 2)
    bfr = (1- a/b)*100
    return bfr

name = 'train' #train, test

t, sensor = measurement(name) # measurement f/t sensor data
_, expdata = expected(name, 'obj1_1') # object dynamics w/o SINDy
_, sindydata = sindy(name) # unmodeled dynamics 
datacompen = expdata + sindydata # object dynamics w/ SINDy

#------------------------RMSE-----------------------
a = calculate_rmse(sensor[15], expdata[15])
aa = calculate_rmse(sensor[16], expdata[16])
aaa = calculate_rmse(sensor[17], expdata[17])
aaaa = calculate_rmse(sensor[18], expdata[18])
aaaaa = calculate_rmse(sensor[19], expdata[19])
aaaaaa = calculate_rmse(sensor[20], expdata[20])

b = calculate_rmse(sensor[15], datacompen[15])
bb = calculate_rmse(sensor[16], datacompen[16])
bbb = calculate_rmse(sensor[17], datacompen[17])
bbbb = calculate_rmse(sensor[18], datacompen[18])
bbbbb = calculate_rmse(sensor[19], datacompen[19])
bbbbbb = calculate_rmse(sensor[20], datacompen[20])

#------------------------BFR-----------------------
c = calculate_BFR(sensor[15], expdata[15])
cc = calculate_BFR(sensor[16], expdata[16])
ccc = calculate_BFR(sensor[17], expdata[17])
cccc = calculate_BFR(sensor[18], expdata[18])
ccccc = calculate_BFR(sensor[19], expdata[19])
cccccc = calculate_BFR(sensor[20], expdata[20])

d = calculate_BFR(sensor[15], datacompen[15])
dd = calculate_BFR(sensor[16], datacompen[16])
ddd = calculate_BFR(sensor[17], datacompen[17])
dddd = calculate_BFR(sensor[18], datacompen[18])
ddddd = calculate_BFR(sensor[19], datacompen[19])
dddddd = calculate_BFR(sensor[20], datacompen[20])

#------------------------RESULT-----------------------
print(" ")
print("----------------------------------")
print("-----Object dynamics w/o SINDy-----")
print("[1] RMSE")
print((a + aa + aaa + aaaa + aaaaa + aaaaaa)/6)
print("[1] FS")
print((c + cc + ccc + cccc + ccccc + cccccc)/6)
print("----------------------------------")
print("-----Object dynamics w/ SINDy-----")
print("[1] RMSE")
print((b + bb + bbb + bbbb + bbbbb + bbbbbb)/6)
print("[1] FS")
print((d + dd + ddd + dddd + ddddd + dddddd)/6)
print("----------------------------------")
print(" ")

# Figure force-torque data
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(19, 10))
lines = []
labels = []

y_labels = ['Force X (N)', 'Force Y (N)', 'Force Z (N)', 'Torque X (Nm)', 'Torque Y (Nm)', 'Torque Z (Nm)']

for i, ax in enumerate(axes.flat):
    line1, = ax.plot(t, sensor[i+15], label='Measurement f/t sensor data', lw=1, alpha=0.8, color='black') 
    line2, = ax.plot(t, expdata[i+15], label='Object dynamics w/o uncertainty', lw=1, alpha=0.6, color='blue')
    line3, = ax.plot(t, datacompen[i+15], label='Object dynamics w/ uncertainty', lw=1.5, alpha=0.6, color='red')   
    
    if i == 0:
        lines.extend([line1, line2, line3])
        labels.extend([line1.get_label(), line2.get_label(), line3.get_label()])

    ax.set_xlabel('Time (s)', fontsize=27, fontweight='bold')
    ax.set_ylabel(y_labels[i], fontsize=27, fontweight='bold')
    ax.grid(True)
    ax.tick_params(axis='both', which='major', labelsize=24) 

font_properties = FontProperties(weight='bold', size=27)
fig.legend(lines, labels, loc='upper center', fontsize=500, ncol=3, prop=font_properties)
plt.tight_layout(rect=[0, 0, 1, 0.93]) 
plt.show()


# Figure Velocity, gravity, acc

# fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
# for i, ax in enumerate(axes.flat):
#     ax.plot(t, sensor[i], label='measured velocity', alpha=1, lw = '1', color='black')
#     ax.set_xlabel('sec')
#     if i in [0,1,2]:
#         ax.set_ylabel('m/sec')
#     else:
#         ax.set_ylabel('rad/sec')
#     ax.set_title(namev[i])
#     ax.legend(loc='upper right')
#     ax.grid(True)
# plt.tight_layout() 

# fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 4))
# for i, ax in enumerate(axes.flat):
#     ax.plot(t, sensor[i+6], label='measured gravity', lw = '1', alpha=1, color='black')
#     ax.set_xlabel('sec')
#     ax.set_ylabel('N')
#     ax.set_title(nameg[i])
#     ax.legend(loc='upper right')
#     ax.grid(True)
# plt.tight_layout()  

# fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
# for i, ax in enumerate(axes.flat):
#     ax.plot(t, sensor[i+9], label='measured acceleration', alpha=1, lw = '1',color='black')
#     ax.set_xlabel('sec')
#     if i in [0,1,2]:
#         ax.set_ylabel('m/sec^2')
#     else:
#         ax.set_ylabel('rad/sec^2')
#     ax.set_title(namea[i])
#     ax.legend(loc='upper right')
#     ax.grid(True)
# plt.tight_layout()  
# plt.show()