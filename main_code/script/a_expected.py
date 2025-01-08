
# Data related to nominal object dynamics.

import numpy as np
from a_dataload import load_data

def load_segmented_data(file_path, delimiter, skip_header, ranges):
    try:
        full_data = np.genfromtxt(file_path, delimiter=delimiter, skip_header=skip_header)
        segmented_data = np.concatenate([full_data[start:end] for start, end in ranges], axis=0)
        return segmented_data
    except Exception as e:
        print(f"Failed to load or process file {file_path}: {e}")
        return None
    
def expected(name, obj):  

    # Information on known object parameters needed to identify unmodeled dynamics.
    if obj == 'obj1_1':

        m = 1.2 #kg 
        rx, ry, rz = -0.081, 0.0446, 0.1278 #m
        Ix, Iy, Iz = 0.05237, 0.06816, 0.03835 #kg*m^2
        Ixy, Ixz, Iyz = 0.004813, 0.01377, -0.01604 #kg*m^2
    
    elif obj == 'obj2':
        m = 1.16
        rx, ry, rz = 0.00, 0.00, 0.04
        Ix, Iy, Iz = 0.01308, 0.01685, 0.0086
        Ixy, Ixz, Iyz = 0.0, 0.0, 0.0
    
    elif obj == 'obj1_1_revised':
        m = 1.2 #kg 
        rx, ry, rz = -0.081, 0.0446, 0.1278 #m
        Ix, Iy, Iz = 0.05240, 0.0759, 0.04595 #kg*m^2
        Ixy, Ixz, Iyz = 0.00981, 0.02827, -0.09876 #kg*m^2


    start_point, end_point, _, g_localPath, objectVelocityPath, objectAccelerationPath, _ = load_data(name)

    ranges = [(start_point, end_point)]

    dt = 0.001
    t = np.linspace(0, (end_point - start_point)*dt, (end_point - start_point))

    gcsv = load_segmented_data(g_localPath, ',', 1, ranges)
    vcsv = load_segmented_data(objectVelocityPath, ',', 1, ranges)
    acsv = load_segmented_data(objectAccelerationPath, ',', 1, ranges)

    g_x = gcsv[:,2]
    g_y = gcsv[:,3]
    g_z = gcsv[:,4]    

    v_x = vcsv[:,1]
    v_y = vcsv[:,2]
    v_z = vcsv[:,3]
    v_wx = vcsv[:,4]
    v_wy = vcsv[:,5]
    v_wz = vcsv[:,6]

    a_x = acsv[:,1]
    a_y = acsv[:,2]
    a_z = acsv[:,3]
    a_wx = acsv[:,4]
    a_wy = acsv[:,5]
    a_wz = acsv[:,6]

    data = np.array([ v_x, v_y, v_z, v_wx, v_wy, v_wz, g_x, g_y, g_z, a_x, a_y, a_z, a_wx, a_wy, a_wz])                

    u_x = m * (rx * (-v_wy**2 - v_wz**2) + ry * (v_wx*v_wy - a_wz) + rz * (v_wx*v_wz + a_wy) + (a_x + g_x))
    u_y = m * (rx * (v_wx*v_wy + a_wz) + ry * (-v_wx**2 - v_wz**2) + rz * (v_wy*v_wz - a_wx) + (a_y + g_y))
    u_z = m * (rx * (v_wx*v_wz - a_wy) + ry * (v_wy*v_wz + a_wx) + rz * (-v_wy**2 - v_wx**2) + (a_z + g_z))
    u_tx = m * (ry*(a_z + g_z) + rz*(-g_y - a_y)) + Ix*a_wx + (-Iy + Iz)*v_wy*v_wz + Ixy*(a_wy - v_wx*v_wz) + Ixz*(a_wz + v_wx*v_wy) + Iyz*(v_wy**2 - v_wz**2)
    u_ty = m * (rx*(-g_z - a_z) + rz*(a_x + g_x)) + Iy*a_wy + (Ix - Iz)*v_wx*v_wz + Ixy*(a_wx + v_wy*v_wz) + Ixz*(v_wz**2 - v_wx**2) + Iyz*(a_wz - v_wx*v_wy)
    u_tz = m * (rx*(a_y + g_y) + ry*(-g_x - a_x)) + Iz*a_wz + (-Ix + Iy)*v_wx*v_wy + Ixy*(v_wx**2 - v_wy**2) + Ixz*(a_wx - v_wy*v_wz) + Iyz*(a_wy + v_wx*v_wz)

    data = np.array([ v_x, v_y, v_z, v_wx, v_wy, v_wz, g_x, g_y, g_z, a_x, a_y, a_z, a_wx, a_wy, a_wz, u_x, u_y, u_z, u_tx, u_ty, u_tz])                

    return t, data