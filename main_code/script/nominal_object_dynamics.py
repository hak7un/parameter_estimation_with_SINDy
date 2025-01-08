import sympy as sp

v_wx, v_wy, v_wz, a_wx, a_wy, a_wz, a_x, a_y, a_z, g_x, g_y, g_z = sp.symbols('v_wx v_wy v_wz a_wx a_wy a_wz a_x a_y a_z g_x g_y g_z')

m = 1.2
rx, ry, rz = -0.081, 0.0446, 0.1278
Ix, Iy, Iz = 0.05259, 0.06831, 0.03872
Ixy, Ixz, Iyz = 0.005702, 0.01608, -0.01628
        
u_x = (m*rx*(-v_wy**2 - v_wz**2) + m*ry*(v_wx*v_wy - a_wz) + m*rz*(v_wx*v_wz + a_wy) + m*(a_x + g_x))
u_y = (m*rx*(v_wx*v_wy + a_wz) + m*ry*(-v_wx**2 - v_wz**2) + m*rz*(v_wy*v_wz - a_wx) + m*(a_y + g_y))
u_z = (m*rx*(v_wx*v_wz - a_wy) + m*ry*(v_wy*v_wz + a_wx) + m*rz*(-v_wy**2 - v_wx**2) + m*(a_z + g_z))
u_tx = (m*ry*(a_z + g_z) + m*rz*(-g_y - a_y) + Ix*a_wx + (-Iy + Iz)*v_wy*v_wz + Ixy*(a_wy - v_wx*v_wz) + Ixz*(a_wz + v_wx*v_wy) + Iyz*(v_wy**2 - v_wz**2))
u_ty = (m*rx*(-g_z - a_z) + m*rz*(a_x + g_x) + Iy*a_wy + (Ix - Iz)*v_wx*v_wz + Ixy*(a_wx + v_wy*v_wz) + Ixz*(v_wz**2 - v_wx**2) + Iyz*(a_wz - v_wx*v_wy))
u_tz = (m*rx*(a_y + g_y) + m*ry*(-g_x - a_x) + Iz*a_wz + (-Ix + Iy)*v_wx*v_wy + Ixy*(v_wx**2 - v_wy**2) + Ixz*(a_wx - v_wy*v_wz) + Iyz*(a_wy + v_wx*v_wz))

print("")
print("fx =", u_x)
print("fy =", u_y)
print("fz =", u_z)
print("tx =", u_tx)
print("ty =", u_ty)
print("tz =", u_tz)
print("")

