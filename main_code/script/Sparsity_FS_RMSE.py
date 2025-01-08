
# Sparsity, 
# Fitting Score, 
# and RMSE data for quantitatively evaluating the appropriate Threshold value when learning SINDy.

import matplotlib.pyplot as plt
import numpy as np

threshold = np.arange(0, 0.11, 0.01)
candidate_data = np.array([60, 47, 41, 39, 31, 22, 20, 18, 17, 15, 14])
candidate_data = np.array([0/60*100, 13/60*100, 19/60*100, 21/60*100, 29/60*100, 38/60*100, 40/60*100, 42/60*100, 43/60*100, 45/60*100, 46/60*100])
bfr_data = np.array([85.9717698809175, 85.95981275591696, 85.64237248654165, 85.63729096202643, 84.5092427811475, 82.9899682601001, 82.98692473230024, 81.86838590007049, 81.78274395525638, 81.1230869414479, 80.70390751454144])
rmse_data = np.array([0.12106869806229535, 0.12109132108501526, 0.12166421747176916, 0.1216845703347685, 0.12487085505445633, 0.1285252379870708, 0.12860810013587176, 0.1300912805306841, 0.1302735250061977, 0.1334684450861484, 0.13431860147019714])

# Sparsity graph
fig1, ax1 = plt.subplots(figsize=(12.5, 10))
ax1.plot(threshold, candidate_data, linestyle='-', lw=7, color='blue', label='Candidate')
ax1.set_xlabel('Threshold Value', fontsize=40, fontweight='bold')
ax1.set_ylabel('Value (%)', fontsize=40, fontweight='bold')
ax1.set_title('Sparsity', fontsize=45, fontweight='bold')
ax1.tick_params(axis='x', labelsize=40)
ax1.tick_params(axis='y', labelsize=40)
fig1.tight_layout()  

# FS, RMSE graph
fig2, ax1 = plt.subplots(figsize=(15, 10))
line1, = ax1.plot(threshold, bfr_data, linestyle='-', color='green', lw=7, label='FS')
ax1.set_xlabel('Threshold Value', fontsize=40, fontweight='bold')
ax1.set_ylabel('FS Value (%)', fontsize=40, fontweight='bold', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.tick_params(axis='x', labelsize=40)
ax1.tick_params(axis='y', labelsize=40)
ax2 = ax1.twinx()
line2, = ax2.plot(threshold, rmse_data, linestyle='-', color='red', lw=7, label='RMSE')
ax2.set_ylabel('RMSE Value', fontsize=40, fontweight='bold', color='black')
ax2.tick_params(axis='y', labelcolor='black')
ax2.tick_params(axis='y', labelsize=40)
ax1.set_title('FS and RMSE', fontsize=45, fontweight='bold')
lines = [line1, line2]
ax1.legend(lines, [l.get_label() for l in lines], loc='center left', fontsize=40)
fig2.tight_layout()  
plt.show()


