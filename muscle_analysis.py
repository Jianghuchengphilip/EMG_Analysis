from sklearn.decomposition import NMF
from time_frequency_analysis import *
#分割步态周期
def Gait_Cycle_Segmentation(filtered_emg_data,emg_fs,force_plate_fs,heel_strikes, toe_offs):
    gait_set ={'id': 0,'begin': 0,'end': 0,'data':None}
    gait_sets = []
    fs_rate = emg_fs / force_plate_fs
    for id , (begin, end) in enumerate(zip(heel_strikes, toe_offs)):
        gait_set = {'id': 0, 'begin': 0, 'end': 0, 'data': None}
        gait_set['id'] = id
        gait_set['begin'] = begin
        gait_set['end'] = end
        gait_set['data'] = filtered_emg_data[:,int(begin * fs_rate) : int(end * fs_rate)]
        gait_sets.append(gait_set)
    return gait_sets
#疲劳分析-计算每个步态周期内的PSD，并查看频率是否向低频段移动 疲劳的肌肉通常会表现出频率下移的特征
def Compute_Psd_Per_Cycle(cycles, sampling_rate):
    cycle_psds = []
    for cycle in cycles:
        freqs, psd = welch(cycle.flatten(), sampling_rate, nperseg=512)
        cycle_psds.append((freqs, psd))
    return cycle_psds
#肌肉协同分析
def NMF_Muscle(filtered_emg_data,n_components,random_state=0, max_iter=500):
    # 对数据进行NMF分解
    model = NMF(n_components=n_components, init='random', random_state=random_state, max_iter=max_iter)
    # 拟合NMF模型
    W = model.fit_transform(np.abs(filtered_emg_data.T))  # 将数据的每列代表时间序列的特征矩阵进行分解
    H = model.components_  # 获取特征权重矩阵
    # W是每个时间点的协同激活值
    # H是各个协同模式对每个肌肉通道的贡献权重
    return W,H
#左右肌群对比
def Left_Right_Muscle_Comparison(filtered_emg_data,left_indices = [5, 6, 2, 4], right_indices = [0, 1, 3, 7]):
    # left_indices = [5, 6, 2, 4]  # 左侧肌肉对应的通道索引
    # right_indices = [0, 1, 3, 7]  # 右侧肌肉对应的通道索引

    left_rms_values = [compute_rms(filtered_emg_data[i, :]) for i in left_indices]
    right_rms_values = [compute_rms(filtered_emg_data[i, :]) for i in right_indices]

    left_mav_values = [compute_mav(filtered_emg_data[i, :]) for i in left_indices]
    right_mav_values = [compute_mav(filtered_emg_data[i, :]) for i in right_indices]
    return left_indices,right_indices,left_rms_values,right_rms_values,left_mav_values,right_mav_values
#计算肌肉贡献率
def Muscle_Contribution_Rate(filtered_emg_data):
    iemg_values = [compute_iemg(filtered_emg_data[i, :]) for i in range(filtered_emg_data.shape[0])]
    contribution_rate = compute_contribution_rate(np.array(iemg_values))
    return contribution_rate
#计算CCI值 以左侧和右侧的对应肌肉为例
def Left_Right_Muscle_CCI(filtered_emg_data,left_indices = [5, 6, 2, 4],right_indices = [0, 1, 3, 7]):
    # left_indices = [5, 6, 2, 4]
    # right_indices = [0, 1, 3, 7]
    cci_values = []
    for left_index, right_index in zip(left_indices, right_indices):
        cci = compute_cci(filtered_emg_data[left_index, :], filtered_emg_data[right_index, :])
        cci_values.append(cci)
    return cci_values
