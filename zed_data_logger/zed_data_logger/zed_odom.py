import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import csv
import datetime

class ZedDataLogger(Node):
    def __init__(self):
        super().__init__('zed_odom') # 노드명 

        # Subscriber 설정
        self.subscriber = self.create_subscription(
            Odometry,
            '/zed/zed_node/odom', #구독할 토픽 
            self.subscriber_callback,
            10 
        )

        # Timer 설정 (1초 간격)
        self.timer = self.create_timer(0.1, self.timer_callback)

        # 데이터를 저장할 변수들 초기화
        self.position = None
        self.orientation = None
        self.twist_linear = None
        self.twist_angular = None

        # 로그 파일 생성 및 CSV 헤더 작성
        self.data_file = open("src/zed_data_logger/zed_data.csv", "w", newline='')
        self.data_writer = csv.writer(self.data_file)

        # 헤더 작성
        self.data_writer.writerow([
            'Position_X', 'Position_Y', 'Position_Z',
            'Orientation_X', 'Orientation_Y', 'Orientation_Z', 'Orientation_W',
            'Twist_Linear_X', 'Twist_Linear_Y', 'Twist_Linear_Z',
            'Twist_Angular_X', 'Twist_Angular_Y', 'Twist_Angular_Z'
        ])

    def subscriber_callback(self, msg):
        # Odometry 메시지로부터 위치, 방향, 속도 데이터를 저장
        self.position = msg.pose.pose.position
        self.orientation = msg.pose.pose.orientation
        self.twist_linear = msg.twist.twist.linear
        self.twist_angular = msg.twist.twist.angular

    def timer_callback(self):
        # 저장된 데이터를 1초마다 파일에 기록
        if self.position and self.orientation and self.twist_linear and self.twist_angular:

            # 모든 데이터를 한 행에 기록
            self.data_writer.writerow([
                self.position.x, self.position.y, self.position.z,
                self.orientation.x, self.orientation.y, self.orientation.z, self.orientation.w,
                self.twist_linear.x, self.twist_linear.y, self.twist_linear.z,
                self.twist_angular.x, self.twist_angular.y, self.twist_angular.z
            ])
            self.get_logger().info('Data written to file') #터미널에 로그가 되고 있음을 출력 
            # 기록을 즉시 파일에 반영
            self.data_file.flush()
        else:
            self.get_logger().info('로그되지 않음')

    def destroy(self):
        # 노드 종료 시 파일 닫기
        self.data_file.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    # 노드 실행
    node = ZedDataLogger()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy()

    rclpy.shutdown()

if __name__ == '__main__':
    main()