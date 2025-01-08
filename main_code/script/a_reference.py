
# Mathematical equation for perturbation input motion satisfying the persistent excitation condition and nominal object dynamics.

import numpy as np
from a_dataload import load_data

def mag_freq_func(t, mag_values, freq_values):
    if t < 10:  
        mag = mag_values[0]
        freq = freq_values[0]
    
    elif t >= 10 and t < 20: 
        mag = mag_values[1]
        freq = freq_values[1]
    
    elif t >= 20 and t < 30:  
        mag = mag_values[2]
        freq = freq_values[2]
    
    elif t >= 30 and t < 40: 
        mag = mag_values[3]
        freq = freq_values[3]
    
    elif t >= 40 and t < 50:  
        mag = mag_values[4]
        freq = freq_values[4]

    else: 
        mag = 0
        freq = 0

    return mag, freq

def reference(name, obj): 

    if obj == 'obj1_1':
        m = 1.2
        rx, ry, rz = -0.081, 0.0446, 0.1278
        Ix, Iy, Iz = 0.05237, 0.06816, 0.03835
        Ixy, Ixz, Iyz = 0.004813, 0.01377, -0.01604
    
    elif obj == 'obj2':
        m = 1.16
        rx, ry, rz = 0.00, 0.00, 0.04
        Ix, Iy, Iz = 0.01308, 0.01685, 0.0086
        Ixy, Ixz, Iyz = 0.0, 0.0, 0.0
  
    else:
        print("Command error")
        return

    start_point, end_point, _, g_localPath, _, _, _ = load_data(name)
    dt = 0.001
    t = np.linspace(0, (end_point - start_point)*dt, (end_point - start_point))

    gcsv = np.genfromtxt(g_localPath, delimiter=',', skip_header=1)
    g_x = gcsv[start_point:end_point, 2]
    g_y = gcsv[start_point:end_point, 3]
    g_z = gcsv[start_point:end_point, 4]

    # Parameters for each time segment : frequency and magnitude
    freq_values_x = [0.1, 0.3, 0.2, 0.3, 0.2]
    freq_values_y = [0.2, 0.1, 0.3, 0.2, 0.1]
    freq_values_z = [0.3, 0.2, 0.2, 0.3, 0.2]

    mag_values_x = [-10, -10, -6, -7, -9]
    mag_values_y = [8,8,8,5,9]
    mag_values_z = [-10, -10, -6, -5, -5]

    v_x = 0.0 * t
    v_y = 0.0 * t
    v_z = 0.0 * t 
    a_x = 0.0 * t
    a_y = 0.0 * t
    a_z = 0.0 * t 

    # Velocity and acceleration
    v_wx = np.zeros(len(t))
    v_wy = np.zeros(len(t))
    v_wz = np.zeros(len(t))
    a_wx = np.zeros(len(t))
    a_wy = np.zeros(len(t))
    a_wz = np.zeros(len(t))
    
    for i in range(len(t)):
        mag_x, freq_x = mag_freq_func(t[i], mag_values_x, freq_values_x)
        mag_y, freq_y = mag_freq_func(t[i], mag_values_y, freq_values_y)
        mag_z, freq_z = mag_freq_func(t[i], mag_values_z, freq_values_z)
        
        v_wx[i] = mag_x * np.pi / 180 * 2 * np.pi * freq_x * np.cos(2 * np.pi * freq_x * t[i])
        v_wy[i] = mag_y * np.pi / 180 * 2 * np.pi * freq_y * np.cos(2 * np.pi * freq_y * t[i])
        v_wz[i] = mag_z * np.pi / 180 * 2 * np.pi * freq_z * np.cos(2 * np.pi * freq_z * t[i])
        a_wx[i] = mag_x * np.pi / 180 * 2 * np.pi * freq_x * (2 * np.pi * freq_x) * np.sin(2 * np.pi * freq_x * t[i])
        a_wy[i] = mag_y * np.pi / 180 * 2 * np.pi * freq_y * (2 * np.pi * freq_y) * np.sin(2 * np.pi * freq_y * t[i])
        a_wz[i] = mag_z * np.pi / 180 * 2 * np.pi * freq_z * (2 * np.pi * freq_z) * np.sin(2 * np.pi * freq_z * t[i])

    fx = m * rx * (-v_wy * v_wy - v_wz * v_wz) + m * ry * (v_wx * v_wy - a_wz) + m * rz * (v_wx * v_wz + a_wy) + m * (a_x + g_x)
    fy = m * rx * (v_wx * v_wy + a_wz) + m * ry * (-v_wx * v_wx - v_wz * v_wz) + m * rz * (v_wy * v_wz - a_wx) + m * (a_y + g_y)
    fz = m * rx * (v_wx * v_wz - a_wy) + m * ry * (v_wy * v_wz + a_wx) + m * rz * (-v_wy * v_wy - v_wx * v_wx) + m * (a_z + g_z)
    tx = m * ry * (a_z + g_z) + m * rz * (-g_y - a_y) + Ix * a_wx + (-Iy + Iz) * v_wy * v_wz + Ixy * (a_wy - v_wx * v_wz) + Ixz * (a_wz + v_wx * v_wy) + Iyz * (v_wy * v_wy - v_wz * v_wz)
    ty = m * rx * (-g_z - a_z) + m * rz * (a_x + g_x) + Iy * a_wy + (Ix - Iz) * v_wx * v_wz + Ixy * (a_wx + v_wy * v_wz) + Ixz * (v_wz * v_wz - v_wx * v_wx) + Iyz * (a_wz - v_wx * v_wy)
    tz = m * rx * (a_y + g_y) + m * ry * (-g_x - a_x) + Iz * a_wz + (-Ix + Iy) * v_wx * v_wy + Ixy * (v_wx * v_wx - v_wy * v_wy) + Ixz * (a_wx - v_wy * v_wz) + Iyz * (a_wy + v_wx * v_wz)

    data = np.array([v_x, v_y, v_z, v_wx, v_wy, v_wz, g_x, g_y, g_z, a_x, a_y, a_z, a_wx, a_wy, a_wz, fx,fy,fz,tx,ty,tz])                
        
    return t, data
