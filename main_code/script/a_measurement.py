
# Three-axis force and three-axis torque data obtained from an ATI force-torque sensor.
# The data measured from the sensor includes uncertainty data such as noise, bias, and friction.

import numpy as np
from a_dataload import load_data

def measurement(name):

    start_point, end_point, _, g, v, a, sensor_cali = load_data(name)
    dt = 0.001

    # Adjoint matrix
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

    # Three-axis force and three-axis torque data expressed in the end-effector coordinate system {r}.
    fcx = transformed_sensor_c_data[3]
    fcy = transformed_sensor_c_data[4]
    fcz = transformed_sensor_c_data[5]
    tcx = transformed_sensor_c_data[0]
    tcy = transformed_sensor_c_data[1]
    tcz = transformed_sensor_c_data[2]

    data = np.array([ v_x, v_y, v_z, v_wx, v_wy, v_wz, g_x, g_y, g_z, a_x, a_y, a_z, a_wx, a_wy, a_wz, fcx, fcy, fcz, tcx, tcy, tcz])  
    
    return t, data







