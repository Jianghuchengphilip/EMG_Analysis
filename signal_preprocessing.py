import numpy as np
from scipy.signal import butter, filtfilt
#信号预处理：巴特沃斯滤波
def Butter_Bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
#低通滤波器
def low_pass_filter(data, cutoff, sampling_rate, order=4):
    nyquist = 0.5 * sampling_rate  # 奈奎斯特频率
    normal_cutoff = cutoff / nyquist  # 归一化截止频率
    b, a = butter(order, normal_cutoff, btype='low', analog=False)  # 设计低通滤波器
    filtered_data = filtfilt(b, a, data)  # 应用滤波器
    return filtered_data
#高通滤波器
def high_pass_filter(data, cutoff, sampling_rate, order=4):
    nyquist = 0.5 * sampling_rate  # 奈奎斯特频率
    normal_cutoff = cutoff / nyquist  # 归一化截止频率
    b, a = butter(order, normal_cutoff, btype='high', analog=False)  # 设计高通滤波器
    filtered_data = filtfilt(b, a, data)  # 应用滤波器
    return filtered_data
#移动平均滤波器 - 移动平滑平滑
def smooth_signal(signal, window_size=5):
    return np.convolve(signal, np.ones(window_size)/window_size, mode='same')
def Butter_Bandpass_Preprocessing(emg_data,sampling_rate,lowcut = 20.0,highcut = 450.0):
    # sampling_rate = 1000 #采样率
    # 滤波参数
    # lowcut = 20.0
    # highcut = 450.0
    b, a = Butter_Bandpass(lowcut, highcut, sampling_rate)
    #行数 = 通道数 ， 列数 = 样本数
    n_channels = emg_data.shape[0]
    n_samples = emg_data.shape[1]
    filtered_data = np.zeros_like(emg_data)
    # 对每个通道进行滤波
    for i in range(n_channels):
        filtered_data[i, :] = filtfilt(b, a, emg_data[i, :])
    return filtered_data
#去除直流电 (直流偏移)  待修改  高通0.5hz-20hz
def remove_dc_offset(data):
    return data - np.mean(data, axis=1, keepdims=True)
#全波整流
def full_wave_rectification(data):
    return np.abs(data)
#修改 添加线性包络
#计算 RMS envelope
def rms_envelope(data, window_size=100):
    envelope = np.zeros_like(data)
    for i in range(data.shape[0]):
        for j in range(window_size, data.shape[1]):
            envelope[i, j] = np.sqrt(np.mean(data[i, j-window_size:j] ** 2))
    return envelope
#MVC标准化
def mvc_normalization(data):
    max_values = np.max(data, axis=1, keepdims=True)
    return (data / max_values) * 100
#将一个Group组sEMG信号对齐
def semg_signal_alignment(group_data,n_channels,n_timepoints=100): #SPM分析的数据预处理  group数据包含一组list，每个步态周期的数据都放在一个list中//n_channels为通道数//目标时间点数（0-100% 步态周期）
    aligned_data = np.zeros((len(group_data), n_timepoints, n_channels))
    for i, cycle in enumerate(group_data):
        n_samples = cycle.shape[1]
        original_time = np.linspace(0, 1, n_samples)
        target_time = np.linspace(0, 1, n_timepoints)
        # 对每个通道插值
        for j in range(n_channels):
            aligned_data[i, :, j] = np.interp(target_time, original_time, cycle[j, :])
    return aligned_data