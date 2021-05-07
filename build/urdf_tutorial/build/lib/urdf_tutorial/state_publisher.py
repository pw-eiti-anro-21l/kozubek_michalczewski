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

        q1=0.0
        q2_passive=0.0
        q2_x=0.0
        q3_passive=0.0
        q3_x=0.0


        # message declarations
        odom_trans = TransformStamped()
        odom_trans.header.frame_id = 'odom'
        odom_trans.child_frame_id = 'link0_passive'
        joint_state = JointState()

        try:
            while rclpy.ok():
                rclpy.spin_once(self)


                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = ['q1', 'q2_passive', 'q2_x', 'q3_passive', 'q3_x']
                joint_state.position = [q1, q2_passive, q2_x, q3_passive, q3_x]

                odom_trans.header.stamp = now.to_msg()
                self.joint_pub.publish(joint_state)
                self.broadcaster.sendTransform(odom_trans)



                q1+=rot_speed
                q2_x-=2*rot_speed




                loop_rate.sleep()

        except KeyboardInterrupt:
            pass

def main():
    node = StatePublisher()

if __name__ == '__main__':
    main()
