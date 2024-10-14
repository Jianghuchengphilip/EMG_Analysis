import matplotlib.pyplot as plt
import numpy as np
channel_names = ['右股直肌','右股二头肌','左胫前肌','右胫前肌','左腓肠肌','左股直肌','左股二头肌','右腓肠肌']  # 通道名称
#解决中文乱码问题
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False
def Plot_RMS_MAV_Graph(rms_values,mav_values):
    plt.figure(figsize=(12, 8))
    plt.bar(channel_names, rms_values, color='b', alpha=0.6, label='RMS')
    plt.bar(channel_names, mav_values, color='r', alpha=0.6, label='MAV')
    plt.title("RMS 和 MAV 的对比", fontsize=20)
    plt.xlabel("肌肉通道", fontsize=15)
    plt.ylabel("信号幅值", fontsize=15)
    plt.xticks(rotation=45, fontsize=12)
    plt.legend()
    plt.grid()
    plt.savefig("./output_img/RMS_MAV_Graph.png")
    plt.show()

def Plot_PSD_Graph(psd_values):
    for i, (x, y) in enumerate(psd_values):
        plt.plot(x, y, label=channel_names[i])
    plt.title('功率谱密度 (PSD)', fontsize=20)
    plt.xlabel('频率 (Hz)', fontsize=15)
    plt.ylabel('功率谱密度 (μV^2/Hz)', fontsize=15)
    plt.xlim(0, 200)  # 只展示0到200Hz范围内的频率
    plt.legend(fontsize=12)
    plt.grid()
    plt.savefig("./output_img/PSD_Graph.png")
    plt.show()

def Plot_PSD_Per_Cycle_Graph(cycle_psds):
    plt.figure(figsize=(12, 8))
    for i, (freqs, psd) in enumerate(cycle_psds):
        plt.plot(freqs, psd, label=f'步态周期 {i + 1}')
    plt.title('不同步态周期的功率谱密度（PSD）', fontsize=20)
    plt.xlabel('频率 (Hz)', fontsize=15)
    plt.ylabel('功率谱密度 (μV^2/Hz)', fontsize=15)
    plt.xlim(0, 200)  # 只显示0到200Hz范围内的频率
    plt.legend(fontsize=12)
    plt.grid()
    plt.savefig("./output_img/PSD_Per_Cycle_Graph.png")
    plt.show()
def Plot_NMF_Graph(W,H,n_components,channel_names,file_name):
    # 统一字体和样式设置
    plt.rcParams.update({
        'font.size': 30,  # 全局字体大小
        'axes.titlesize': 35,  # 标题字体大小
        'axes.labelsize': 25,  # x, y 轴标签字体大小
        'xtick.labelsize': 25,  # x 轴刻度标签字体大小
        'ytick.labelsize': 25,  # y 轴刻度标签字体大小
        'legend.fontsize': 25  # 图例字体大小
    })

    # 定义条形图宽度
    bar_width = 0.15  # 每个条形图的宽度
    index = np.arange(len(channel_names))  # 横轴刻度位置

    # 可视化协同模式 H，条形图并排排列
    plt.figure(figsize=(18, 12))
    for i in range(n_components):
        # 偏移每个协同模式的条形图，使其并排排列
        plt.bar(index + i * bar_width, H[i, :], bar_width, alpha=0.6, label=f'协同模式 {i + 1}')

    plt.title(f'文件{file_name} 各协同模式的肌肉贡献')
    plt.xlabel('肌肉通道')
    plt.ylabel('权重')
    plt.xticks(index + bar_width * (n_components - 1) / 2, channel_names, rotation=45)  # 调整x轴刻度位置
    plt.legend()
    plt.grid()

    plt.tight_layout()  # 调整布局防止标签重叠
    plt.savefig(f"./output_img/NMF_Bar_{file_name}.png")
    plt.show()

    # 可视化协同激活时间曲线 W
    plt.figure(figsize=(12, 8))
    for i in range(n_components):
        plt.plot(W[0:1000, i], label=f'协同模式 {i + 1}')

    plt.title(f'文件{file_name} 协同模式的激活时间曲线')
    plt.xlabel('时间 (样本点)')
    plt.ylabel('激活值')
    plt.legend()
    plt.grid()

    plt.tight_layout()  # 调整布局
    plt.savefig(f"./output_img/NMF_Line_{file_name}.png")
    plt.show()
def Plot_Left_Right_Muscle_Comparison(left_indices,right_indices,left_rms_values,right_rms_values,left_mav_values,right_mav_values):
    channels = ['股直肌', '股二头肌', '胫前肌', '腓肠肌']
    # 可视化左右肌肉RMS对比
    plt.figure(figsize=(12, 6))
    bar_width = 0.35
    index = np.arange(len(channels))

    # 绘制RMS对比图
    plt.bar(index, left_rms_values, bar_width, label='左侧肌肉', alpha=0.7, color='blue')
    plt.bar(index + bar_width, right_rms_values, bar_width, label='右侧肌肉', alpha=0.7, color='red')

    plt.xlabel('肌肉通道', fontsize=15)
    plt.ylabel('RMS值', fontsize=15)
    plt.title('左右肌肉RMS对比', fontsize=20)
    plt.xticks(index + bar_width / 2, channels, fontsize=20)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("./output_img/Left_Right_Muscle_RMS.png")
    plt.show()

    # 可视化左右肌肉MAV对比
    plt.figure(figsize=(12, 6))

    # 绘制MAV对比图
    plt.bar(index, left_mav_values, bar_width, label='左侧肌肉', alpha=0.7, color='blue')
    plt.bar(index + bar_width, right_mav_values, bar_width, label='右侧肌肉', alpha=0.7, color='red')

    plt.xlabel('肌肉通道', fontsize=15)
    plt.ylabel('MAV值', fontsize=15)
    plt.title('左右肌肉MAV对比', fontsize=20)
    plt.xticks(index + bar_width / 2, channels, fontsize=20)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("./output_img/Left_Right_Muscle_MAV.png")
    plt.show()
def Plot_Muscle_Contribution_Rate(contribution_rate):
    channels = ['右股直肌', '右股二头肌', '左胫前肌', '右胫前肌', '左腓肠肌', '左股直肌', '左股二头肌', '右腓肠肌']
    plt.figure(figsize=(10, 6))
    plt.bar(channels, contribution_rate, color='lightgreen', alpha=0.7)
    plt.title('各通道的贡献率 (Contribution Rate)', fontsize=16)
    plt.xlabel('肌肉通道', fontsize=14)
    plt.ylabel('贡献率', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("./output_img/Muscle_Contribution_Rate.png")
    plt.show()
def Plot_CCI_Values(cci_values):
    plt.figure(figsize=(10, 6))
    comparison_channels = ['股直肌', '股二头肌', '胫前肌', '腓肠肌']
    plt.bar(comparison_channels, cci_values, color='lightcoral')
    plt.title('左右肌肉的CCI值', fontsize=25)
    plt.xlabel('肌肉对比', fontsize=14)
    plt.ylabel('CCI值', fontsize=14)
    # plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("./output_img/CCI_Values.png")
    plt.show()
def Plot_Gait_Per_Cycle(single_gait_data,channel_names):
    fig, axes = plt.subplots(len(channel_names), 1, figsize=(12, 15), sharex=True)
    fig.suptitle(f"步态周期:id:{single_gait_data['id']} \n emg帧:{int(single_gait_data['begin'])} - {int(single_gait_data['end'])}", fontsize=25)
    for i in range(len(channel_names)):
        axes[i].plot(single_gait_data["data"][i], label=channel_names[i], color='b', linewidth=1.5)
        axes[i].grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)  # 添加网格
        axes[i].legend(loc='upper right')  # 添加图例
        axes[-1].set_xticklabels([f'{int(x)}' for x in np.linspace(int(single_gait_data['begin']), int(single_gait_data['end']), len(axes[-1].get_xticks()))])
    plt.subplots_adjust(hspace=0.4)
    plt.savefig(f"./output_img/Gait_Per_Cycle_id_{single_gait_data['id']}.png")
    plt.show()