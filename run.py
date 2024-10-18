from read_file import Read_Asc_File
from signal_preprocessing import *
from time_frequency_analysis import Compute_RMS_MAV_Value,Compute_Psd_Value
from draw_data_graph import *
from muscle_analysis import *
asc_file_path = './data/1.asc'
emg_data = Read_Asc_File(asc_file_path)
dc_removed_data = remove_dc_offset(emg_data)
filtered_data = Butter_Bandpass_Preprocessing(dc_removed_data)
rectified_data = full_wave_rectification(filtered_data)
envelope_data = rms_envelope(rectified_data)
normalized_data = mvc_normalization(envelope_data)
rms_values,mav_values = Compute_RMS_MAV_Value(filtered_data)
psd_values = Compute_Psd_Value(filtered_data,1000)
Plot_RMS_MAV_Graph(rms_values,mav_values)
Plot_PSD_Graph(psd_values)
NMF_W,NMF_H = NMF_Muscle(normalized_data,3)
Plot_NMF_Graph(NMF_W,NMF_H,3)
left_indices,right_indices,left_rms_values,right_rms_values,left_mav_values,right_mav_values = Left_Right_Muscle_Comparison(filtered_data)
Plot_Left_Right_Muscle_Comparison(left_indices,right_indices,left_rms_values,right_rms_values,left_mav_values,right_mav_values)
contribution_rate = Muscle_Contribution_Rate(normalized_data)
Plot_Muscle_Contribution_Rate(contribution_rate)
CCI_values = Left_Right_Muscle_CCI(normalized_data)
Plot_CCI_Values(CCI_values)
