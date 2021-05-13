#! /usr/bin/env python
import time
from math import sin, cos, pi
import threading
import rclpy
from time import sleep
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped
from zadanie4_srv.srv import JintControlSrv


class Jint(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('jint')

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.jint_control_srv = self.create_service(JintControlSrv, "interpolation_params",
                                                    self.interpolation_params_callback)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))

        # robot state parameters
        self.declare_parameter('poz1', 0.0)
        self.declare_parameter('poz2', 0.0)
        self.declare_parameter('poz3', 0.0)
        self.poz1 = self.get_parameter('poz1').get_parameter_value().double_value
        self.poz2 = self.get_parameter('poz2').get_parameter_value().double_value
        self.poz3 = self.get_parameter('poz3').get_parameter_value().double_value

        # interpolation parameters
        self.target_time = 0.0
        self.oldpoz1 = self.poz1
        self.oldpoz2 = self.poz2
        self.oldpoz3 = self.poz3
        self.newpoz1 = 0.0
        self.newpoz2 = 0.0
        self.newpoz3 = 0.0
        self.interpolation_method = ""
        self.time_period = 0.05
        self.time_passed = 0.0
        self.max_error = 0.05
        self.err_poz = [0.0, 0.0, 0.0]

        # threading
        self.result = False

        # message declarations
        self.odom_trans = TransformStamped()
        self.odom_trans.header.frame_id = 'odom'
        self.odom_trans.child_frame_id = 'baza'
        self.joint_state = JointState()

        publsh_thread = threading.Thread(target=self.publish_state)
        publsh_thread.start()

    def interpolation_params_callback(self, request, response):

        self.newpoz1 = request.newpoz1
        self.newpoz2 = request.newpoz2
        self.newpoz3 = request.newpoz3


        if abs(self.newpoz1) > 3.14 or abs(self.newpoz2) > 2.5 or self.newpoz3 > 0.1 or self.poz3 < -0.5:
            response.operation = "Podana pozycja jest bledna"
            return response

        if request.time <= 0.0:
            response.operation = "Czas musi byc wiekszy od 0"
            return response

        if request.interpolation == "linear" or request.interpolation == "spline":
            self.target_time = request.time
            self.oldpoz1 = self.poz1
            self.oldpoz2 = self.poz2
            self.oldpoz3 = self.poz3
            self.interpolation_method = request.interpolation
            self.time_passed = 0.0
            self.result = False

            thread = threading.Thread(target=self.update_state)  # create update_state loop on a different thread
            thread.start()  # start thread
            thread.join()  # wait for the thread to stop

            if self.result:
                response.operation = "Iterpolacja zakonczona sukcesem"
            else:
                response.operation = "Interpolacja nieudana"

        else:
            response.operation = "Nieznana metoda interpolacji"

        return response

    # method to publish new state even if not changing (to keep connection with rviz)
    def publish_state(self):
        while True:
            try:
                # update joint_state
                now = self.get_clock().now()
                self.joint_state.header.stamp = now.to_msg()
                self.joint_state.name = ["baza_do_ramie1", "ramie1_do_ramie2", "ramie2_do_ramie3"]
                self.joint_state.position = [self.poz1, self.poz2, self.poz3]
                self.odom_trans.header.stamp = now.to_msg()

                # send the joint state and transform
                self.joint_pub.publish(self.joint_state)
                self.broadcaster.sendTransform(self.odom_trans)
                time.sleep(self.time_period)

            except KeyboardInterrupt:
                exit(0)

    # method to interpolate all new positions of joints
    def update_state(self):
        while self.time_passed < self.target_time:
            # change params
            self.poz1 = interpolate(self.oldpoz1, self.newpoz1, 0, self.target_time, self.time_passed,
                                        self.interpolation_method)

            self.poz2 = interpolate(self.oldpoz2, self.newpoz2, 0, self.target_time, self.time_passed,
                                        self.interpolation_method)

            self.poz3 = interpolate(self.oldpoz3, self.newpoz3, 0, self.target_time, self.time_passed,
                                        self.interpolation_method)

            # count time for interpolation
            time.sleep(self.time_period)

            self.time_passed += self.time_period
            
        self.result = True

# method to count linear interpolated position for given current time
def interpolate_linear(x0, x1, t0, t1, time_passed):
    return x0 + ((x1 - x0) / (t1 - t0)) * (time_passed - t0)


# method to count spline cubic interpolated position for given current time
def interpolate_spline_cubic(x0, x1, t0, t1, time_passed):
    tx = (time_passed - t0) / (t1 - t0)  # wzor z wiki
    k1 = 0  # pochodna rowna zero v(t0) = 0
    k2 = 0  # pochodna rowna zero v(t1) = 0
    a = k1 * (t1 - t0) - (x1 - x0)
    b = - k2 * (t1 - t0) + (x1 - x0)
    qx = (1 - tx) * x0 + tx * x1 + tx * (1 - tx) * ((1 - tx) * a + tx * b)
    return qx


# method to interpolate with given method
def interpolate(x0, x1, t0, t1, time_passed, method):
    if method == "linear":
        return interpolate_linear(x0, x1, t0, t1, time_passed)
    elif method == "spline":
        return interpolate_spline_cubic(x0, x1, t0, t1, time_passed)


def main():
    node = Jint()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
