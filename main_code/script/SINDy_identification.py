
# SINDy unmodeled identification process
import numpy as np
import pysindy as ps
from a_measurement import measurement
from a_expected import expected

name = 'train'

t, data = measurement(name)
_, expdata = expected(name, 'obj1_1')  # 데이터 #물체종류
minusdata = data - expdata

X = np.stack((data[0], data[1], data[2], data[3], data[4], data[5]), axis=-1)
U = np.stack((data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14]), axis=-1)
DX = np.stack((minusdata[15], minusdata[16], minusdata[17], minusdata[18], minusdata[19], minusdata[20]), axis=-1)

inputs_temp = np.tile([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 2)
inputs_per_library = np.reshape(inputs_temp, (2, 15))

for i in range(9): #1차
    inputs_per_library[0, 6 + i] = 3
for i in range(3):
    inputs_per_library[0, i] = 3
for i in range(9): #1차
    inputs_per_library[1, i] = 14


poly_1st_library = ps.PolynomialLibrary(degree=1, include_bias=True)
# poly_2nd_library = ps.PolynomialLibrary(degree=2, include_bias=True)
fourier_library = ps.FourierLibrary(include_cos=False)

generalized_library = ps.GeneralizedLibrary([poly_1st_library, fourier_library], inputs_per_library = inputs_per_library)
optimizer = ps.STLSQ(threshold=0.06)

model = ps.SINDy(
    feature_library=generalized_library,
    optimizer=optimizer,
    feature_names=["v_x", "v_y", "v_z", "v_wx", "v_wy", "v_wz", "g_x", "g_y", "g_z", "a_x", "a_y", "a_z", "a_wx", "a_wy", "a_wz"]
)

model.fit(X, x_dot=DX, u=U, t=t)
model.print()

print(model.get_feature_names())
print(len(model.get_feature_names()))
