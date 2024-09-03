import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np

class DepthSubscriber(Node):
    def __init__(self):
        super().__init__('depth_subscriber') #노드명

        #qos_profile: QoS(서비스 품질) 설정을 통해 구독자의 메시지 전송 신뢰성 및 저장 정책을 설정합니다. 여기서는 'Best Effort' 정책을 사용하여 가능한 한 많은 메시지를 수신하도록 합니다.
        qos_profile = rclpy.qos.QoSProfile(depth=10, reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT)

        #구독자 설정
        self.depth_sub = self.create_subscription(
            Image,
            '/zed/zed_node/depth/depth_registered',
            self.depth_callback,
            qos_profile
        )
    #콜백 함수
    def depth_callback(self,msg):
        if msg.encoding != '32FC1':
            self.get_logger().error(f'Unsupported encoding: {msg.encoding}')
            return 
        
        try:
            depth_image = np.frombuffer(msg.data, dtype=np.float32).reshape((msg.height, msg.width))
        except ValueError as e:
            self.get_logger().error(f'Error reshaping data: {e}')
            return 
        
        center_x = msg.width //2
        center_y = msg.height //2
        center_distance = depth_image[center_y, center_x] 

        self.get_logger().info(f'Center distance: {center_distance:.2f} m')

def main(args=None):
    rclpy.init(args=args)
    node = DepthSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
