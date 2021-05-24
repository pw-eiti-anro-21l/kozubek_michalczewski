#! /usr/bin/env python
from math import sin, cos, atan2, sqrt
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
import yaml
from tf2_ros import TransformBroadcaster, TransformStamped

class Ikin(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('ikin_node')
        self.d1 = 1.5
        self.a2 = 1
        self.a3 = 0.5
        self.d3 = 0.3
        self.alfa3 = 3.14
        self.poz1 = 0.0
        self.poz2 = 0.0
        self.poz3 = 0.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        qos_profile = QoSProfile(depth=10)
        self.pose_sub = self.create_subscription(PoseStamped, 'pose_stamped_oint', self.listener_callback, qos_profile)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.odom_trans = TransformStamped()
        self.odom_trans.header.frame_id = 'odom'
        self.odom_trans.child_frame_id = 'baza'
        self.joint_state = JointState()

        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))

    def listener_callback(self, msg):
        self.x = msg.pose.position.x
        self.y = msg.pose.position.y
        self.z = msg.pose.position.z
        self.calculate_joint_state()
        self.publish_joint()


    def publish_joint(self):
        now = self.get_clock().now()
        self.joint_state.header.stamp = now.to_msg()
        self.joint_state.name = ["baza_do_ramie1", "ramie1_do_ramie2", "ramie2_do_ramie3"]
        self.joint_state.position = [self.poz1, self.poz2, self.poz3]
        self.odom_trans.header.stamp = now.to_msg()
        self.joint_pub.publish(self.joint_state)
        self.broadcaster.sendTransform(self.odom_trans)

    def calculate_joint_state(self):
        cosVal2 = (self.x ** 2 + self.y ** 2 - self.a2 ** 2 - self.a3 ** 2) / (2 * self.a2 * self.a3)
        if cosVal2 > 1 or cosVal2 < -1:
            self.get_logger().error("IMPOSSIBLE POSITION")
        else:
            sinVal2 = sqrt(1 - cosVal2 ** 2)
            sinVal2 *= -1
            self.poz2 = atan2(sinVal2, cosVal2)
            k1 = self.a2 + self.a3 * cosVal2
            k2 = self.a3 * sinVal2
            r = sqrt(k1 ** 2 + k2 ** 2)
            phi = atan2(k2, k1)
            k1 = r * cos(phi)
            k2 = r * sin(phi)
            self.poz1 = atan2(self.y, self.x) - atan2(k2, k1)
            self.poz3 = self.d1 - self.d3 - self.z



def main():
    node = Ikin()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
