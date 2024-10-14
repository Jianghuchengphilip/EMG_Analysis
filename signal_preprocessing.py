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
#去除直流电 (直流偏移)
def remove_dc_offset(data):
    return data - np.mean(data, axis=1, keepdims=True)
#全波整流
def full_wave_rectification(data):
    return np.abs(data)
#计算线性包络 (RMS envelope)
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
