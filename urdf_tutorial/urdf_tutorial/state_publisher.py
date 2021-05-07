from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped

class StatePublisher(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('state_publisher')

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))

        degree = pi / 180.0
        loop_rate = self.create_rate(30)

        tinc = degree
        rot_speed = 0.01

        self.declare_parameter('poz1', 0.0)
        self.declare_parameter('poz2', 0.0)
        self.declare_parameter('poz3', 0.0)

        self.poz1 = self.get_parameter('poz1').get_parameter_value().double_value
        self.poz2 = self.get_parameter('poz2').get_parameter_value().double_value
        self.poz3 = self.get_parameter('poz3').get_parameter_value().double_value


        base_to_second=0.0
        second_to_third=0.0
        linear_joint=0.0
        self.timer = self.create_timer(0.2, self.update_state)

    def update_state(self):
        # message declarations
        odom_trans = TransformStamped()
        odom_trans.header.frame_id = 'odom'
        odom_trans.child_frame_id = 'base_link'
        joint_state = JointState()

        try:
            while rclpy.ok():
                rclpy.spin_once(self)


                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = ['base_to_second', 'second_to_third', 'linear_joint']
                joint_state.position = [self.poz1, self.poz2, self.poz3]

                if self.poz1 < self.get_parameter('poz1').get_parameter_value().double_value:
                    self.poz1 += 0.05
                if self.poz1 > self.get_parameter('poz1').get_parameter_value().double_value:
                    self.poz1 -= 0.05

                self.poz1 = min(max(-3.14,self.poz1),3.14)

                odom_trans.header.stamp = now.to_msg()
                self.joint_pub.publish(joint_state)
                self.broadcaster.sendTransform(odom_trans)



        except KeyboardInterrupt:
            pass

def main():
    node = StatePublisher()
    rclpy.spin(node)

main()
