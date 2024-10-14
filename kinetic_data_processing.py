'''动力学数据提取'''
from signal_preprocessing import *
import matplotlib.pyplot as plt
#获取FZ的数据，目前肌电处理包我只针对于做步态分割所需参数。
def Get_Force_Plate_Data(data,parameters,channel_id,is_filter=0,cutoff=50):
    '''
    data一般是c3d中的analogs
    Channel_id为一个list必须按照(Fx,Fy,Fz,Mx,My,Mz)
    is_filter=1 为打开滤波器
    '''

    if 'ANALOG' in parameters:
        analog_params = parameters['ANALOG']
        scale_factors = analog_params['SCALE']['value']
        offsets = analog_params['OFFSET']['value']
        sampling_rate = int(analog_params['RATE']['value'][0])
    if 'FORCE_PLATFORM' in parameters:
        force_params = parameters['FORCE_PLATFORM']
        cal_matrix = force_params['CAL_MATRIX']['value']
    offsets = offsets[channel_id]
    scale_factors = scale_factors[channel_id]
    force_data = data[0, channel_id]
    real_force_data = (force_data.T - offsets) * scale_factors
    calibrated_force_data = np.dot(cal_matrix[:, :, 0], real_force_data.T)
    Fz_data = calibrated_force_data[2]  # Fx=0 Fy=1 Fz=2
    if is_filter:
        Fz_data = low_pass_filter(Fz_data,cutoff,sampling_rate)
    return Fz_data,sampling_rate

#
def Get_Gait_Events(Fz_data,sampling_rate, threshold=20,is_smoothed=1):
    heel_strikes = []  # 用于保存初始接触事件
    toe_offs = []  # 用于保存脚趾离地事件
    #平滑数据
    if is_smoothed:
        Fz_data = smooth_signal(Fz_data)
    # 状态标志，检测步态阶段的标志
    is_contact = False
    for i in range(1, len(Fz_data)):
        if not is_contact and Fz_data[i] > threshold:
            # 检测到初始接触（Fz 由低于阈值变为高于阈值）
            heel_strikes.append(i)
            is_contact = True
        elif is_contact and Fz_data[i] < threshold:
            # 检测到脚趾离地（Fz 由高于阈值变为低于阈值）
            toe_offs.append(i)
            is_contact = False
    return heel_strikes, toe_offs

