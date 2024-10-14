import os

import matplotlib.pyplot as plt

from read_file import *
from signal_preprocessing import *
from draw_data_graph import *
from muscle_analysis import *
from kinetic_data_processing import *
# directory_path = './data/m'
# file_paths = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path)]
# for file_path in file_paths:
#     channel_names , data = Read_M_File(file_path)
#     del channel_names[-1]
#     emg_data = np.delete(data,-1,axis=0)
#     dc_removed_data = remove_dc_offset(emg_data)
#     sampling_rate = 2000  # 采样率
#     filtered_data = Butter_Bandpass_Preprocessing(dc_removed_data,sampling_rate=sampling_rate)
#     rectified_data = full_wave_rectification(filtered_data)
#     envelope_data = rms_envelope(rectified_data)
#     normalized_data = mvc_normalization(envelope_data)
#     print(file_path,normalized_data.shape)
    # W,H = NMF_Muscle(normalized_data,n_components=3)
    # Plot_NMF_Graph(W,H,n_components=3,channel_names=channel_names,file_name=file_path[-18:-2])
c3d_path = "./data/c3d/0619-caoli-LR-3.33.c3d"
m_path = "./data/m/2024-06-19-20-15_0619 caoli LR 3.33.m"
# kinetic
points,analogs,parameters = Read_C3d_File(c3d_path)
Fz_data,Fz_sampling_rate = Get_Force_Plate_Data(data=analogs,parameters=parameters,channel_id=[0,1,2,3,4,5],is_filter=1)
heel_strikes, toe_offs = Get_Gait_Events(Fz_data,Fz_sampling_rate)
#emg
emg_data,channel_names = Read_M_File(m_path)
del channel_names[-1]
emg_data = np.delete(emg_data,-1,axis=0)
dc_removed_data = remove_dc_offset(emg_data)
emg_sampling_rate = 2000  # 采样率
filtered_data = Butter_Bandpass_Preprocessing(dc_removed_data,sampling_rate=emg_sampling_rate)
rectified_data = full_wave_rectification(filtered_data)
envelope_data = rms_envelope(rectified_data)
normalized_data = mvc_normalization(envelope_data)
# seg
gait_sets = Gait_Cycle_Segmentation(normalized_data,emg_sampling_rate,Fz_sampling_rate,heel_strikes, toe_offs)
# print(gait_sets)
# print(gait_sets[9])
# print(gait_sets[9]["data"].shape)
# plt.plot(gait_sets[9]["data"][2].T)
# plt.show()
# print(channel_names)
for i in range(1,20):
    Plot_Gait_Per_Cycle(gait_sets[i],channel_names)