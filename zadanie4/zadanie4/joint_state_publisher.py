#! /usr/bin/env python
from math import sin, cos, pi
import threading
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

        # robot state parameters
        self.declare_parameter('poz1', 0.0)
        self.declare_parameter('poz2', 0.0)
        self.declare_parameter('poz3', 0.0)

        self.poz1 = self.get_parameter('poz1').get_parameter_value().double_value
        self.poz2 = self.get_parameter('poz2').get_parameter_value().double_value
        self.poz3 = self.get_parameter('poz3').get_parameter_value().double_value

        # message declarations
        self.odom_trans = TransformStamped()
        self.odom_trans.header.frame_id = 'odom'
        self.odom_trans.child_frame_id = 'baza'
        self.joint_state = JointState()

        self.timer = self.create_timer(0.02, self.update_state)

    def update_state(self):

        try:
            # update joint_state
            now = self.get_clock().now()
            self.joint_state.header.stamp = now.to_msg()
            self.joint_state.name = ["baza_do_ramie1", "ramie1_do_ramie2", "ramie2_do_ramie3"]
            self.joint_state.position = [self.poz1, self.poz2, self.poz3]

            self.odom_trans.header.stamp = now.to_msg()


            self.joint_pub.publish(self.joint_state)
            self.broadcaster.sendTransform(self.odom_trans)


            p1 = self.get_parameter('poz1').get_parameter_value().double_value - self.poz1
            p2 = self.get_parameter('poz2').get_parameter_value().double_value - self.poz2
            p3 = self.get_parameter('poz3').get_parameter_value().double_value - self.poz3

            if abs(p1)>=0.1:
                if abs(self.poz1+0.02*(p1/abs(p1)))>3.14:
                    self.get_logger().error(
                        "Niepoprawna wartosc 1 parametru")
                else:
                    self.poz1 += 0.02*(p1/abs(p1))
            if abs(p2)>=0.1:
                if abs(self.poz2+0.02*(p2/abs(p2)))>2.5:
                    self.get_logger().error(
                        "Niepoprawna wartosc 2 parametru")
                else:
                    self.poz2 += 0.02*(p2/abs(p2))
            if abs(p3)>=0.1:
                if self.poz3+0.02*(p3/abs(p3))>0.1 or self.poz3+0.02*(p3/abs(p3))<-0.5:
                    self.get_logger().error(
                        "Niepoprawna wartosc 3 parametru")
                else:
                    self.poz3 += 0.02*(p3/abs(p3))

        except KeyboardInterrupt:
            pass


def main():
    node = StatePublisher()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
