import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

from curtsies import Input

import tty
import sys
import termios


class MinimalPublisherSubscriber(Node):

    def __init__(self):
        super().__init__('pubsub')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        timer_period = 1 # seconds
        self.timer = self.create_timer(timer_period, self.read_input)

        self.declare_parameter('forward_key', 'w')
        self.declare_parameter('backward_key', 's')
        self.declare_parameter('left_key', 'a')
        self.declare_parameter('right_key', 'd')
        self.x = 0
        print('Press \'' + self.get_parameter('forward_key').get_parameter_value().string_value + '\' to move forward, \'' + self.get_parameter('backward_key').get_parameter_value().string_value + '\' to move backward, and press \'' + self.get_parameter('left_key').get_parameter_value().string_value + '\' and \'' + self.get_parameter('right_key').get_parameter_value().string_value + '\' to move left and right')

    def read_input(self):
        with Input(keynames='curses') as input_generator:
            for e in input_generator:
                self.x = e
                self.timer_callback()
                tty.setcbreak

    def timer_callback(self):
        vel_msg = Twist()
        forward_key = self.get_parameter('forward_key').get_parameter_value().string_value
        backward_key = self.get_parameter('backward_key').get_parameter_value().string_value
        left_key = self.get_parameter('left_key').get_parameter_value().string_value
        right_key = self.get_parameter('right_key').get_parameter_value().string_value

        vel_msg.linear.x = 0.0
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0

        if self.x == forward_key:
            vel_msg.linear.x = 1.0
        if self.x == backward_key:
            vel_msg.linear.x = -1.0
        if self.x == left_key:
            vel_msg.angular.z = 1.0
        if self.x == right_key:
            vel_msg.angular.z = -1.0
        self.publisher_.publish(vel_msg)


def main(args=None):
    global Settings
    Settings = termios.tcgetattr(sys.stdin)
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