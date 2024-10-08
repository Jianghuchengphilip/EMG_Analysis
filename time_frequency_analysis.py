import numpy as np
from scipy.signal import welch
import scipy.signal as signal
from scipy.linalg import svd
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
def zero_crossing(filtered_emg_data):
    """零交叉率（Zero Crossing, ZC）"""
    zc_count = np.sum(np.diff(np.sign(filtered_emg_data)) != 0)
    return zc_count
def slope_sign_changes(filtered_emg_data, threshold=0.01):
    """斜率符号变化（Slope Sign Change, SSC）"""
    ssc_count = np.sum(((filtered_emg_data[1:-1] - filtered_emg_data[:-2]) * (filtered_emg_data[2:] - filtered_emg_data[1:-1])) > threshold)
    return ssc_count
def mean_frequency(filtered_emg_data, fs):
    """均值频率（Mean Frequency, MNF）  fs为采样频率"""
    f, Pxx = signal.welch(filtered_emg_data, fs, nperseg=1024)
    mnf = np.sum(f * Pxx) / np.sum(Pxx)
    return mnf
def singular_value_decomposition(filtered_emg_data):
    """奇异值分解（Singular Value Decomposition, SVD）"""
    u, s, vh = svd(filtered_emg_data.reshape(-1, 1), full_matrices=False)
    return s[0]
