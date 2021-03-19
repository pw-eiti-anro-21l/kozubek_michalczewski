import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class MinimalPublisherSubscriber(Node):

    def __init__(self):
        super().__init__('pubsub')
        #self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.listener_callback,
            10)

        #timer_period = 1 # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        #self.subscription

        self.i = 0

    def listener_callback(self, pose):
        self.get_logger().info('I heard: x')

    def timer_callback(self):
        vel_msg = Twist()
        vel_msg.linear.x = -1.0
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0
        self.publisher_.publish(vel_msg)
        self.get_logger().info(f'Publishing: velocity: {vel_msg.linear}')
        #self.i += 1




def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisherSubscriber()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()