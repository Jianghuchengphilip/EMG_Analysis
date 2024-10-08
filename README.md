# 表面肌电EMG分析包
## 一、数据读取
- .ASC格式文件 √
- .MAT格式文件 ×
- .CSV格式文件 ×
- .EDF格式文件 × （初步考虑使用MNE库打开与处理）
- .C3D格式文件 ×
- .HDF5格式文件 × （初步考虑使用h5py库处理）
- .TXT格式文件
## 二、数据预处理
- 巴特沃斯滤波器 √
- 去除直流偏移 √
- 全波整流 √
- RMS envelope √
- MVC标准化 √
- 基线漂移校正 ×
- 小波去噪 ×
- ......
## 三、特征提取
- 均方根值（RMS） √
- 平均绝对值（MAV） √
- 功率谱密度（PSD） √
- 肌肉贡献率 √
- CCI值 (共激活指数) √
- 积分肌电值（iEMG） √
- 零交叉率（ZC） √
- 波形长度（WL） ×
- 均值频率（MNF） √
- 奇异值分解(SVD) √
- 斜率符号变化（SSC） √
- 中值频率（MF）×
- 平均功率频率(MPF) ×
- ......
## 四、数据分析
- 步态周期分割√
- 疲劳分析（基于PSD） √
- 肌肉协同分析（NMF） √
- 左右肌群对比分析（基于RMS，MAV） √
- 肌肉贡献率分析 √
- CCI值分析 √
- 肌肉收缩速度分析 ×
- 非线性动力学分析 ×
- 运动控制策略分析 ×
- ......
## 五、绘图
- RMS_MAV图
![RMS_MAV图](https://github.com/Jianghuchengphilip/EMG_Analysis/blob/main/output_img/RMS_MAV_Graph.png "RMS_MAV图")
- PSD图
![PSD图](https://github.com/Jianghuchengphilip/EMG_Analysis/blob/main/output_img/PSD_Graph.png "PSD图")
- 步态周期PSD图
![步态周期PSD图](https://github.com/Jianghuchengphilip/EMG_Analysis/blob/main/output_img/PSD_Per_Cycle_Graph.png "步态周期PSD图")
- NMF图
![NMF图](https://github.com/Jianghuchengphilip/EMG_Analysis/blob/main/output_img/NMF_Bar.png "NMF图")
![NMF图](https://github.com/Jianghuchengphilip/EMG_Analysis/blob/main/output_img/NMF_Line.png "NMF图")
- 左右肌肉RMS对比图
![左右肌肉RMS对比图](https://github.com/Jianghuchengphilip/EMG_Analysis/blob/main/output_img/Left_Right_Muscle_RMS.png "左右肌肉RMS对比图")
- 左右肌肉MAV对比图
![左右肌肉MAV对比图](https://github.com/Jianghuchengphilip/EMG_Analysis/blob/main/output_img/Left_Right_Muscle_MAV.png "左右肌肉MAV对比图")
- 肌肉贡献率图
![肌肉贡献率图](https://github.com/Jianghuchengphilip/EMG_Analysis/blob/main/output_img/Muscle_Contribution_Rate.png "肌肉贡献率图")
- CCI值图
![CCI值图](https://github.com/Jianghuchengphilip/EMG_Analysis/blob/main/output_img/CCI_Values.png "CCI值图")
