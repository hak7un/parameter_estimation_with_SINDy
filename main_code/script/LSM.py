
# Online unknown object parameter estimation process with LSM

import numpy as np
from a_dataload import load_data

name = 'obj1_2' # obj1_1, obj1_2, obj1_3, obj1_4, obj2, obj3

start_point, end_point, _, g, v, a, sensor_cali = load_data(name)

dt = 0.001
data_len = 10000 # The parameter estimation uses 10 seconds of data.

sensor_to_ee_translation = 0.155 
z = -45 
x = 0

t = np.linspace(0, (end_point - start_point)*dt, (end_point - start_point))    

gcsv = np.genfromtxt(g, delimiter=',', skip_header=1)
vcsv = np.genfromtxt(v, delimiter=',', skip_header=1)
acsv = np.genfromtxt(a, delimiter=',', skip_header=1)
ftc = np.genfromtxt(sensor_cali, delimiter=',', skip_header=1)

g_x = gcsv[start_point:end_point,2]
g_y = gcsv[start_point:end_point,3]
g_z = gcsv[start_point:end_point,4]

v_x = vcsv[start_point:end_point,1]
v_y = vcsv[start_point:end_point,2]
v_z = vcsv[start_point:end_point,3]
v_wx = vcsv[start_point:end_point,4]
v_wy = vcsv[start_point:end_point,5]
v_wz = vcsv[start_point:end_point,6]

a_x = acsv[start_point:end_point,1]
a_y = acsv[start_point:end_point,2]
a_z = acsv[start_point:end_point,3]
a_wx = acsv[start_point:end_point,4]
a_wy = acsv[start_point:end_point,5]
a_wz = acsv[start_point:end_point,6]

fcx = ftc[start_point:end_point,1]
fcy = ftc[start_point:end_point,2]
fcz = ftc[start_point:end_point,3]
tcx = ftc[start_point:end_point,4]
tcy = ftc[start_point:end_point,5]    
tcz = ftc[start_point:end_point,6]

sensor_c_data = np.array([tcx, tcy, tcz, fcx, fcy, fcz])

a = np.cos(np.deg2rad(z))
b = np.sin(np.deg2rad(z))
c = np.cos(np.deg2rad(x))
d = np.sin(np.deg2rad(x))
R_z = np.array([[a, -b, 0], [b, a, 0], [0, 0, 1]])
R_x = np.array([[1, 0, 0], [0, c, -d], [0, d, c]])
translation = np.array([0,0,sensor_to_ee_translation])

R_ = R_z.dot(R_x)
translation_sensor_to_ee = R_.dot(translation)

p_cross = np.array([
    [0, -translation_sensor_to_ee[2], translation_sensor_to_ee[1]],
    [translation_sensor_to_ee[2], 0, -translation_sensor_to_ee[0]],
    [-translation_sensor_to_ee[1], translation_sensor_to_ee[0], 0]
])

Ad_T = np.zeros((6, 6))
Ad_T[0:3, 0:3] = R_
Ad_T[3:6, 0:3] = p_cross.dot(R_)
Ad_T[3:6, 3:6] = R_

transformed_sensor_c_data = ((Ad_T).T).dot(sensor_c_data)

fcx = transformed_sensor_c_data[3]
fcy = transformed_sensor_c_data[4]
fcz = transformed_sensor_c_data[5]
tcx = transformed_sensor_c_data[0]
tcy = transformed_sensor_c_data[1]
tcz = transformed_sensor_c_data[2]

data = np.array([ v_x, v_y, v_z, v_wx, v_wy, v_wz, g_x, g_y, g_z, a_x, a_y, a_z, a_wx, a_wy, a_wz, fcx, fcy, fcz, tcx, tcy, tcz])  

# Online unknown object parameter estimation with LSM
ft_len = 6

# DATA stack
combined_array = np.empty((ft_len * data_len,)) 
combined_array[0::ft_len] = fcx 
combined_array[1::ft_len] = fcy 
combined_array[2::ft_len] = fcz
combined_array[3::ft_len] = tcx 
combined_array[4::ft_len] = tcy
combined_array[5::ft_len] = tcz

# Convert to a column vector
combined_array = combined_array.reshape(-1, 1)

# nominal object dynaimics and the proposed integrated equation including unmodeled dynamics
A = np.zeros((ft_len*data_len, 10)) # nominal object dynamics 
AA = np.zeros((ft_len*data_len, 30)) # proposed integrated equation

for i in range(data_len):

    # mass
    A[ft_len*i, 0] = a_x[i] + g_x[i]
    A[ft_len*i+1, 0] = a_y[i] + g_y[i]
    A[ft_len*i+2, 0] = a_z[i] + g_z[i]

    # center of mass x
    A[ft_len*i, 1] = -v_wy[i]**2 - v_wz[i]**2
    A[ft_len*i+1, 1] = v_wx[i]*v_wy[i] + a_wz[i]
    A[ft_len*i+2, 1] = v_wx[i]*v_wz[i] - a_wy[i]
    A[ft_len*i+4, 1] = -g_z[i] - a_z[i]
    A[ft_len*i+5, 1] = a_y[i]+g_y[i]
    
    # center of mass y
    A[ft_len*i, 2] = v_wx[i]*v_wy[i]-a_wz[i]
    A[ft_len*i+1, 2] = -v_wx[i]**2 - v_wz[i]**2
    A[ft_len*i+2, 2] = v_wy[i]*v_wz[i] + a_wx[i]
    A[ft_len*i+3, 2] = a_z[i] + g_z[i]
    A[ft_len*i+5, 2] = -g_x[i]-a_x[i]
    
    # center of mass z
    A[ft_len*i, 3] = v_wx[i]*v_wz[i] + a_wy[i]
    A[ft_len*i+1, 3] = v_wy[i]*v_wz[i] - a_wx[i]
    A[ft_len*i+2, 3] = -v_wy[i]**2 -v_wx[i]**2
    A[ft_len*i+3, 3] = -g_y[i] -a_y[i]
    A[ft_len*i+4, 3] = a_x[i] + g_x[i]

    # moment of inertia Ixx
    A[ft_len*i+3, 4] = a_wx[i]
    A[ft_len*i+4, 4] = v_wx[i]*v_wz[i]
    A[ft_len*i+5, 4] = -v_wx[i]*v_wy[i]
    
    # moment of inertia Ixy
    A[ft_len*i+3, 5] = a_wy[i]-v_wx[i]*v_wz[i]
    A[ft_len*i+4, 5] = a_wx[i]+v_wy[i]*v_wz[i]
    A[ft_len*i+5, 5] = v_wx[i]**2-v_wy[i]**2

    # moment of inertia Ixz
    A[ft_len*i+3, 6] = a_wz[i]+v_wx[i]*v_wy[i]
    A[ft_len*i+4, 6] = v_wz[i]**2 - v_wx[i]**2
    A[ft_len*i+5, 6] = a_wx[i] - v_wy[i]*v_wz[i]

    # moment of inertia Iyy
    A[ft_len*i+3, 7] = -v_wy[i]*v_wz[i]
    A[ft_len*i+4, 7] = a_wy[i]
    A[ft_len*i+5, 7] = v_wx[i]*v_wy[i]

    # moment of inertia Iyz
    A[ft_len*i+3, 8] = v_wy[i]**2 - v_wz[i]**2
    A[ft_len*i+4, 8] = a_wz[i] - v_wx[i]*v_wy[i]
    A[ft_len*i+5, 8] = a_wy[i] + v_wx[i]*v_wz[i]

    # moment of inertia Izz
    A[ft_len*i+3, 9] = v_wy[i]*v_wz[i]
    A[ft_len*i+4, 9] = -v_wx[i]*v_wz[i]
    A[ft_len*i+5, 9] = a_wz[i]


for i in range(data_len):

    # mass
    AA[ft_len*i, 0] = a_x[i] + g_x[i]
    AA[ft_len*i+1, 0] = a_y[i] + g_y[i]
    AA[ft_len*i+2, 0] = a_z[i] + g_z[i]

    # center of mass x
    AA[ft_len*i, 1] = -v_wy[i]**2 - v_wz[i]**2
    AA[ft_len*i+1, 1] = v_wx[i]*v_wy[i] + a_wz[i]
    AA[ft_len*i+2, 1] = v_wx[i]*v_wz[i] - a_wy[i]
    AA[ft_len*i+4, 1] = -g_z[i] - a_z[i]
    AA[ft_len*i+5, 1] = a_y[i]+g_y[i]
    
    # center of mass y
    AA[ft_len*i, 2] = v_wx[i]*v_wy[i]-a_wz[i]
    AA[ft_len*i+1, 2] = -v_wx[i]**2 - v_wz[i]**2
    AA[ft_len*i+2, 2] = v_wy[i]*v_wz[i] + a_wx[i]
    AA[ft_len*i+3, 2] = a_z[i] + g_z[i]
    AA[ft_len*i+5, 2] = -g_x[i]-a_x[i]
    
    # center of mass z
    AA[ft_len*i, 3] = v_wx[i]*v_wz[i] + a_wy[i]
    AA[ft_len*i+1, 3] = v_wy[i]*v_wz[i] - a_wx[i]
    AA[ft_len*i+2, 3] = -v_wy[i]**2 -v_wx[i]**2
    AA[ft_len*i+3, 3] = -g_y[i] -a_y[i]
    AA[ft_len*i+4, 3] = a_x[i] + g_x[i]

    # moment of inertia Ixx
    AA[ft_len*i+3, 4] = a_wx[i]
    AA[ft_len*i+4, 4] = v_wx[i]*v_wz[i]
    AA[ft_len*i+5, 4] = -v_wx[i]*v_wy[i]
    
    # moment of inertia Ixy
    AA[ft_len*i+3, 5] = a_wy[i]-v_wx[i]*v_wz[i]
    AA[ft_len*i+4, 5] = a_wx[i]+v_wy[i]*v_wz[i]
    AA[ft_len*i+5, 5] = v_wx[i]**2-v_wy[i]**2

    # moment of inertia Ixz
    AA[ft_len*i+3, 6] = a_wz[i]+v_wx[i]*v_wy[i]
    AA[ft_len*i+4, 6] = v_wz[i]**2 - v_wx[i]**2
    AA[ft_len*i+5, 6] = a_wx[i] - v_wy[i]*v_wz[i]

    # moment of inertia Iyy
    AA[ft_len*i+3, 7] = -v_wy[i]*v_wz[i]
    AA[ft_len*i+4, 7] = a_wy[i]
    AA[ft_len*i+5, 7] = v_wx[i]*v_wy[i]

    # moment of inertia Iyz
    AA[ft_len*i+3, 8] = v_wy[i]**2 - v_wz[i]**2
    AA[ft_len*i+4, 8] = a_wz[i] - v_wx[i]*v_wy[i]
    AA[ft_len*i+5, 8] = a_wy[i] + v_wx[i]*v_wz[i]

    # moment of inertia Izz
    AA[ft_len*i+3, 9] = v_wy[i]*v_wz[i]
    AA[ft_len*i+4, 9] = -v_wx[i]*v_wz[i]
    AA[ft_len*i+5, 9] = a_wz[i]

    # unmodeled dynamics term with SINDy
    # fx
    AA[ft_len*i+0, 10] = 1
    AA[ft_len*i+0, 11] = v_wy[i]
    AA[ft_len*i+0, 12] = np.sin(a_x[i])
    AA[ft_len*i+0, 13] = np.sin(a_wy[i]) 

    # fy
    AA[ft_len*i+1, 14] = 1 
    AA[ft_len*i+1, 15] = v_wx[i]
    AA[ft_len*i+1, 16] = np.sin(a_y[i])
    AA[ft_len*i+1, 17] = np.sin(a_wx[i]) 
    AA[ft_len*i+1, 18] = np.sin(a_wz[i])

    # fz 
    AA[ft_len*i+2, 19] = 1
    AA[ft_len*i+2, 20] = v_wy[i]
    AA[ft_len*i+2, 21] = np.sin(a_z[i])
    AA[ft_len*i+2, 22] = np.sin(a_wx[i])
    AA[ft_len*i+2, 23] = np.sin(a_wy[i])

    # tx  
    AA[ft_len*i+3, 24] = np.sin(a_y[i])

    # ty 
    AA[ft_len*i+4, 25] = np.sin(a_x[i])
    AA[ft_len*i+4, 26] = np.sin(a_z[i])
    AA[ft_len*i+4, 27] = np.sin(a_wy[i])

    # tz 
    AA[ft_len*i+5, 28] = np.sin(a_y[i])
    AA[ft_len*i+5, 29] = np.sin(a_wz[i])

pinA = np.linalg.pinv(A)
pinAA = np.linalg.pinv(AA)

resultA = np.dot(pinA, combined_array)
resultAA = np.dot(pinAA, combined_array)

for i in range(3):
    resultA[i+1] = resultA[i+1]/resultA[0]

for i in range(3):
    resultAA[i+1] = resultAA[i+1]/resultAA[0]

print(" ")
print("LSM w/o SINDy")
print(resultA[0]*1000, resultA[1]*1000, resultA[2]*1000, resultA[3]*1000)
print(resultA[4], resultA[7], resultA[9], resultA[5], resultA[6], resultA[8])
print(" ")
print("LSM w/ SINDy")
print(resultAA[0]*1000, resultAA[1]*1000, resultAA[2]*1000, resultAA[3]*1000)
print(resultAA[4], resultAA[7], resultAA[9], resultAA[5], resultAA[6], resultAA[8])
print(" ")
