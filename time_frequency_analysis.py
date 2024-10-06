import numpy as np
from scipy.signal import welch

def compute_rms(emg_signal):
    """计算均方根值（RMS）"""
    return np.sqrt(np.mean(emg_signal**2))

def compute_mav(emg_signal):
    """计算平均绝对值（MAV）"""
    return np.mean(np.abs(emg_signal))

def compute_psd(emg_signal, fs, nperseg=1024):
    """计算功率谱密度（PSD）"""
    freqs, psd = welch(emg_signal, fs, nperseg=nperseg)
    return freqs, psd
def compute_iemg(emg_signal):
    """计算iEMG"""
    return np.sum(np.abs(emg_signal))
def compute_contribution_rate(iemg_values):
    """计算肌肉贡献率"""
    total_iemg = np.sum(iemg_values)
    return iemg_values / total_iemg
def compute_cci(rms_a, rms_b):
    """计算CCI值 (共激活指数)"""
    min_rms = np.minimum(rms_a, rms_b)
    cci = 2 * np.sum(min_rms) / (np.sum(rms_a) + np.sum(rms_b))
    return cci
def Compute_RMS_MAV_Value(filtered_emg_data):
    n_channels = filtered_emg_data.shape[0]
    rms_values = []
    mav_values = []
    for i in range(n_channels):
        rms_value = compute_rms(filtered_emg_data[i, :])
        mav_value = compute_mav(filtered_emg_data[i, :])
        rms_values.append(rms_value)
        mav_values.append(mav_value)
    return rms_values,mav_values
def Compute_Psd_Value(filtered_emg_data,sampling_rate):
    n_channels = filtered_emg_data.shape[0]
    psd_values = []
    for i in range(n_channels):
        freqs, psd = compute_psd(filtered_emg_data[i, :], sampling_rate)
        psd_values.append((freqs, psd))
    return psd_values
