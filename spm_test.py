import os
import matplotlib.pyplot as plt
import numpy as np
from read_file import *
from signal_preprocessing import *
from draw_data_graph import *
from muscle_analysis import *
from kinetic_data_processing import *
import spm1d
import numpy as np
import matplotlib.pyplot as plt
c3d_paths = ["./data/c3d/0619-caoli-LR-3.33.c3d","./data/c3d/0619-caoli-DR-3.33.c3d"]
m_paths = ["./data/m/2024-06-19-20-15_0619 caoli LR 3.33.m","./data/m/2024-06-19-20-20_0619 caoli DR 3.33.m"]
group = [[],[]]
for id,(c3d_path,m_path) in enumerate(zip(c3d_paths,m_paths)):
    # kinetic
    points, analogs, parameters = Read_C3d_File(c3d_path)
    Fz_data, Fz_sampling_rate = Get_Force_Plate_Data(data=analogs, parameters=parameters, channel_id=[0, 1, 2, 3, 4, 5],
                                                     is_filter=1)
    heel_strikes, toe_offs = Get_Gait_Events(Fz_data, Fz_sampling_rate)
    # emg
    emg_data, channel_names = Read_M_File(m_path)
    print(emg_data.shape)
    del channel_names[-1]
    emg_data = np.delete(emg_data, -1, axis=0)
    dc_removed_data = remove_dc_offset(emg_data)
    emg_sampling_rate = 2000  # 采样率
    filtered_data = Butter_Bandpass_Preprocessing(dc_removed_data, sampling_rate=emg_sampling_rate)
    rectified_data = full_wave_rectification(filtered_data)
    envelope_data = rms_envelope(rectified_data)
    normalized_data = mvc_normalization(envelope_data)
    gait_sets = Gait_Cycle_Segmentation(normalized_data, emg_sampling_rate, Fz_sampling_rate, heel_strikes, toe_offs)
    for gait in gait_sets:
        group[id].append(gait['data'])
n_timepoints = 100  # 目标时间点数（0-100% 步态周期）
n_channels = 8  # 每个周期有 8 个通道
aligned_data_1 = semg_signal_alignment(group_data=group[0],n_channels=n_channels,n_timepoints=n_timepoints)
aligned_data_2 = semg_signal_alignment(group_data=group[1],n_channels=n_channels,n_timepoints=n_timepoints)
# aligned_data_1 = np.zeros((len(group[0]), n_timepoints, n_channels))

# for i, cycle in enumerate(group[0]):
#     cycle = cycle.T
#     n_samples = cycle.shape[0]  # 当前周期的采样点数
#     original_time = np.linspace(0, 1, n_samples)  # 原始时间轴 (0-100%)
#     print(original_time.shape)
#     target_time = np.linspace(0, 1, n_timepoints)  # 目标时间轴 (0-100%)
#
#     # 对每个通道插值
#     for j in range(n_channels):
#         aligned_data_1[i, :, j] = np.interp(target_time, original_time, cycle[:, j])
# print("对齐后的数据形状:", aligned_data_1.shape)
#
# aligned_data_2 = np.zeros((len(group[1]), n_timepoints, n_channels))
# for i, cycle in enumerate(group[1]):
#     cycle = cycle.T
#     n_samples = cycle.shape[0]  # 当前周期的采样点数
#     original_time = np.linspace(0, 1, n_samples)  # 原始时间轴 (0-100%)
#     target_time = np.linspace(0, 1, n_timepoints)  # 目标时间轴 (0-100%)
#     # 对每个通道插值
#     for j in range(n_channels):
#         aligned_data_2[i, :, j] = np.interp(target_time, original_time, cycle[:, j])
# print("对齐后的数据形状:", aligned_data_2.shape)

plt.figure(figsize=(10, 6))
plt.plot(np.linspace(0, 100, n_timepoints), aligned_data_1[7, :, 3])
plt.xlabel('步态周期 (%)')
plt.ylabel('EMG 信号幅值')
plt.title('对齐后的 EMG 信号 (通道 1)')
plt.legend()
plt.show()

aligned_data_1 = aligned_data_1[:43, :,:]
aligned_data_2 = aligned_data_2[:43, :,:]
for i in range(0,8):
    print(aligned_data_1.shape, aligned_data_2.shape)
    t = spm1d.stats.ttest_paired(aligned_data_1[:,:,i], aligned_data_2[:,:,i])
    t_inference = t.inference(two_tailed=True)
    # print(SPM(aligned_data_1[:,:,i], aligned_data_2[:,:,i]))
    # 绘制 SPM 结果
    plt.figure()
    t_inference.plot()
    plt.title(f'LR & DR SPM sEMG{channel_names[i]}')
    plt.savefig(f'./output_img/LR & DR SPM sEMG{channel_names[i]}.png')
    plt.show()
