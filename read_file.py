import numpy as np
import scipy.io
import ezc3d
# 安装ezc3d请用conda install ezc3d-1.5.11-py311_python3_ha0d415b_3.conda 下载对应自己python版本和操作系统的包 https://anaconda.org/conda-forge/ezc3d/files?page=1
def Read_Asc_File(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            # 跳过非数值行
            if line.startswith('#') or not line.strip():
                continue
            # 根据 .asc 文件的格式解析每行数据
            values = line.split()
            try:
                # 提取所需的信号值并添加到数据列表中
                data.append([float(value) for value in values])
            except ValueError:
                channels_name = values # 通道名称
                continue
    return np.array(data).T,channels_name
def Read_M_File(file_path):
    mat_data = scipy.io.loadmat(file_path)
    main_data = mat_data[list(mat_data.keys())[-1]]
    main_data_content = main_data[0, 0]
    data_all = []
    channel_names = []
    for data in main_data_content[1][0][0][5][0][0][1][0][0]:
        data_all.append(np.array(data[0]['data'][0]).flatten())
        channel_names.append(str(data[0][0][1][0]))
    return np.vstack(data_all),channel_names

def Read_C3d_File(file_path):
    c3d = ezc3d.c3d(file_path)
    points = c3d['data']['points']  # 标记点数据
    analogs = c3d['data']['analogs']  # 力平台数据（模拟信号）
    parameters = c3d['parameters']  # 参数信息
    return points,analogs,parameters
