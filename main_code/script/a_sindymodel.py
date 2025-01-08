
# Unmodeled dynamics identified using SINDy in the offline learning process.

import numpy as np
from a_dataload import load_data

def sindy(name):    

    start_point, end_point, _, g_localPath, objectVelocityPath, objectAccelerationPath, _ = load_data(name)

    dt = 0.001
    t = np.linspace(0, (end_point - start_point)*dt, (end_point - start_point))

    gcsv = np.genfromtxt(g_localPath, delimiter=',',skip_header=1)         
    vcsv = np.genfromtxt(objectVelocityPath, delimiter=',',skip_header=1)    
    acsv = np.genfromtxt(objectAccelerationPath, delimiter=',',skip_header=1) 

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

    data = np.array([ v_x, v_y, v_z, v_wx, v_wy, v_wz, g_x, g_y, g_z, a_x, a_y, a_z, a_wx, a_wy, a_wz])       
        
    # Unmodeled dynamics
    # Threshold 0.06
    fx = -0.254*1 + 0.193*v_wy + -1.873*np.sin(1*a_x) + -0.235*np.sin(1*a_wy)
    fy = 0.617*1 + -0.577*v_wx + -1.474*np.sin(1*a_y) + 0.362*np.sin(1*a_wx) + 0.089*np.sin(1*a_wz)
    fz = -0.084*1 + 0.065*v_wy + -2.223*np.sin(1*a_z) + 0.160*np.sin(1*a_wx) + -0.082*np.sin(1*a_wy)
    tx = 0.250*np.sin(1*a_y)
    ty = -0.149*np.sin(1*a_x) + -0.124*np.sin(1*a_z) + -0.090*np.sin(1*a_wy)
    tz = 0.116*np.sin(1*a_y) + -0.068*np.sin(1*a_wz)

    data = np.array([v_x, v_y, v_z, v_wx, v_wy, v_wz, g_x, g_y, g_z, a_x, a_y, a_z, a_wx, a_wy, a_wz, fx, fy, fz, tx, ty, tz ])                

    return t, data