import pandas as pd #데이터 분석을 위한 라이브러리 
import matplotlib.pyplot as plt #그래프를 그리는데 사용 

csv_file = "/home/kon/ros2_ws/src/zed_data_logger/zed_data.csv" #csv가 저장된 경로
data = pd.read_csv(csv_file) #pd 라이브러리르 사용하여 csv 파일을 읽어 저장할 변수 


#dataframe의 인덱스를 넘파이 배열로 변환하여, 그래프의 x축으로 사용할 시간 스텝 데이터를 준비 
time_steps = data.index.to_numpy() 

fig, axs = plt.subplots(2,1, figsize = (10,10))
#2행 1열의 플롯을 생성, 그림 크기는 10,10

axs[0].plot(time_steps, data['Position_X'].to_numpy(), label='Position X')
axs[0].plot(time_steps, data['Position_Y'].to_numpy(), label='Position Y')
axs[0].plot(time_steps, data['Position_Z'].to_numpy(), label='Position Z')
axs[0].plot(time_steps, data['Orientation_X'].to_numpy(), label='Orientation X')
axs[0].plot(time_steps, data['Orientation_Y'].to_numpy(), label='Orientation Y')
axs[0].plot(time_steps, data['Orientation_Z'].to_numpy(), label='Orientation Z')
axs[0].plot(time_steps, data['Orientation_W'].to_numpy(), label='Orientation W')
axs[0].set_title('Position and Orientation') #제목
axs[0].legend() #범례
axs[0].set_xlabel('Time Step') #x이름
axs[0].set_ylabel('Values')#y이름 

axs[1].plot(time_steps, data['Twist_Linear_X'].to_numpy(), label='Linear Velocity X')
axs[1].plot(time_steps, data['Twist_Linear_Y'].to_numpy(), label='Linear Velocity Y')
axs[1].plot(time_steps, data['Twist_Linear_Z'].to_numpy(), label='Linear Velocity Z')
axs[1].plot(time_steps, data['Twist_Angular_X'].to_numpy(), label='Angular Velocity X')
axs[1].plot(time_steps, data['Twist_Angular_Y'].to_numpy(), label='Angular Velocity Y')
axs[1].plot(time_steps, data['Twist_Angular_Z'].to_numpy(), label='Angular Velocity Z')
axs[1].set_title('Linear and Angular Velocity')
axs[1].legend()
axs[1].set_xlabel('Time Step')
axs[1].set_ylabel('Values')

plt.tight_layout() #plt.tight_layout()는 플롯의 레이아웃을 최적화하여 요소들이 겹치지 않도록 합니다.
plt.show() #plt.show()는 그래프를 화면에 표시합니다.

