import numpy as np
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
                # 处理无法转换为浮点数的行  跳过中文
                continue
    return np.array(data)