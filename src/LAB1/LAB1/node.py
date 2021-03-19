import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from curtsies import Input

import tty
import sys
import termios

import subprocess




class MinimalPublisherSubscriber(Node):

    def __init__(self):
        super().__init__('pubsub')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.listener_callback,
            10)

        timer_period = 1 # seconds
        self.timer = self.create_timer(timer_period, self.read_input)
        self.subscription
        self.declare_parameter('foward_key', 'w')
        self.declare_parameter('backward_key', 's')
        self.declare_parameter('left_key', 'a')
        self.declare_parameter('right_key', 'd')
        self.x = 0
        print('Press \'' + self.get_parameter('foward_key').get_parameter_value().string_value + '\' to move fowrd, \'' + self.get_parameter('backward_key').get_parameter_value().string_value + '\' to move backward, and press \'' + self.get_parameter('left_key').get_parameter_value().string_value + '\' and \'' + self.get_parameter('right_key').get_parameter_value().string_value + '\' to move left and right')
        #bashCommand = "stty -echo"
        #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()

    def listener_callback(self, pose):
        #self.get_logger().info(f'I heard: x = {pose.x}, y = {pose.y} ')
        pass

    # def read_input(self):
    #     orig_settings = termios.tcgetattr(sys.stdin)
    #
    #     tty.setcbreak(sys.stdin)
    #     x = 0
    #     while x != chr(27):  # ESC
    #         x = sys.stdin.read(1)[0]
    #         print("You pressed", x)
    #
    #     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)


    def read_input(self):
        with Input(keynames='curses') as input_generator:
            for e in input_generator:
                self.x=e
                self.timer_callback()
                tty.setcbreak

    def timer_callback(self):
        vel_msg = Twist()
        foward_key = self.get_parameter('foward_key').get_parameter_value().string_value
        backward_key = self.get_parameter('backward_key').get_parameter_value().string_value
        left_key = self.get_parameter('left_key').get_parameter_value().string_value
        right_key = self.get_parameter('right_key').get_parameter_value().string_value

        #orig_settings = termios.tcgetattr(sys.stdin)
        #tty.setcbreak(sys.stdin)
        #self.x = sys.stdin.read(1)[0]
        #print("You pressed", self.x)

        #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)


        vel_msg.linear.x = 0.0
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0


        if self.x == foward_key:
            vel_msg.linear.x = 1.0
        if self.x == backward_key:
            vel_msg.linear.x = -1.0
        if self.x == left_key:
            vel_msg.angular.z = 1.0
        if self.x == right_key:
            vel_msg.angular.z = -1.0
        self.publisher_.publish(vel_msg)
        #self.get_logger().info(f'Publishing: velocity: {vel_msg.linear}')




def main(args=None):
    #settings = saveTerminalSettings()
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
