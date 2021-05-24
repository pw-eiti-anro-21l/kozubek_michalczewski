#! /usr/bin/env python
import time
from math import sin, cos, pi, sqrt
import threading
import rclpy
from time import sleep
from rclpy.node import Node
from rclpy.qos import QoSProfile
from nav_msgs.msg import Path
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import PoseStamped
from tf2_ros import TransformBroadcaster, TransformStamped
from zadanie5_ikin_srv.srv import IkinControlSrv
from copy import deepcopy


class Oint(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('oint')

        # message declarations
        self.odom_trans = TransformStamped()
        self.odom_trans.header.frame_id = 'odom'
        self.odom_trans.child_frame_id = 'baza'
        self.pose_stamped = PoseStamped()
        self.oint_path = Path()

        # robot state parameters
        self.x = 1.0
        self.y = 0.0
        self.z = 1.3

        # interpolation parameters
        self.target_time = 0.0
        self.time = 1.0
        self.figure = ""
        self.oldx = self.x
        self.oldy = self.y
        self.oldz = self.z
        self.newx = 1.0
        self.newy = 0.0
        self.newz = 1.3

        self.a = 0.4
        self.b = 0.2
        self.interpolation_method = ""
        self.time_period = 0.05
        self.time_passed = 0.0


        self.result = False

        qos_profile = QoSProfile(depth=10)
        self.oint_pub = self.create_publisher(PoseStamped, 'pose_stamped_oint', qos_profile)
        self.path_pub = self.create_publisher(Path, 'path_poses', qos_profile)
        self.ikin_control_srv = self.create_service(IkinControlSrv, "interpolation_params_oint",
                                                    self.interpolation_params_callback)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))

        publsh_thread = threading.Thread(target=self.publish_state)
        publsh_thread.start()

    def interpolation_params_callback(self, request, response):

        self.time = 2
        self.oldx = self.x
        self.oldy = self.y
        self.oldz = self.z
        
        self.newx = self.x
        self.newy = self.y
        self.newz = self.z
        
        self.interpolation_method = "linear"
        self.time_passed = 0.0
        self.result = False
        self.figure = request.figure

        thread = threading.Thread(target=self.update_state)  # create update_state loop on a different thread
        thread.start()  # start thread
        thread.join()  # wait for the thread to stop

        self.draw_shape()
        return response

    def publish_state(self):
        while True:
            try:
                now = self.get_clock().now()
                self.pose_stamped.pose.position.x = self.x
                self.pose_stamped.pose.position.y = self.y
                self.pose_stamped.pose.position.z = self.z
                self.oint_path.header.stamp = now.to_msg()
                self.oint_path.header.frame_id = 'odom'
                self.pose_stamped.header.stamp = now.to_msg()
                self.pose_stamped.header.frame_id = 'odom'
                self.oint_path.poses.append(deepcopy(self.pose_stamped))
                self.odom_trans.header.stamp = now.to_msg()
                self.oint_pub.publish(self.pose_stamped)
                self.path_pub.publish(self.oint_path)
                time.sleep(self.time_period)

            except KeyboardInterrupt:
                exit(0)



    def draw_rectangle(self, a, b, ab, time):
        self.newx = self.x + a
        self.newz = self.z + b

        if a + b <= 0:
            flaga = -1
        else:
            flaga = 1

        self.target_time = time * 0.5 * ((a + b) / ab) * flaga
        self.oldx = self.x
        self.oldy = self.y
        self.oldz = self.z
        self.interpolation_method = "linear"
        self.time_passed = 0.0
        self.result = False

        thread = threading.Thread(target=self.update_state)
        thread.start()
        thread.join()

    def draw_ellipse(self, a, b, start_x, start_z, i, number_of_steps, ):
        self.x = start_x + a * cos(2 * pi * i / number_of_steps) - a
        self.z = start_z + b * sin(2 * pi * i / number_of_steps)
        time.sleep(self.time_period)

    def draw_shape(self):

        if self.figure == "rectangle":
            self.draw_rectangle(0, 0.5 * self.b, self.a + self.b, self.time)
            self.draw_rectangle(-self.a, 0, self.a + self.b, self.time)
            self.draw_rectangle(0, -self.b, self.a + self.b, self.time)
            self.draw_rectangle(self.a, 0, self.a + self.b, self.time)
            self.draw_rectangle(0, 0.5 * self.b, self.a + self.b, self.time)

        if self.figure == "ellipse":
            thread = threading.Thread(target=self.update_state)
            thread.start()
            thread.join()
            
            number_of_steps_ = int(self.time / self.time_period)
            for i in range(1, number_of_steps_ + 1):
                self.draw_ellipse(0.5 * self.a, 0.5 * self.b, self.newx, self.newz, i,
                                  number_of_steps_)

        if self.figure == "point":
            self.newy = 1.0
            self.newx = 0.0
            self.newz = 1.3
            self.oldx = self.x
            self.oldy = self.y
            self.oldz = self.z
            self.interpolation_method = "linear"
            self.target_time = 3
            self.time_passed = 0.0
            self.result = False
            thread = threading.Thread(target=self.update_state)
            thread.start()
            thread.join()
                                  


    def update_state(self):

        while self.time_passed < self.target_time:

            if self.x != self.newx or self.y != self.newy:
                x = self.x
                y = self.y
                if self.x != self.newx:
                    x = interpolate(self.oldx, self.newx, 0, self.target_time, self.time_passed,
                                    self.interpolation_method)
                if self.y != self.newy:
                    y = interpolate(self.oldy, self.newy, 0, self.target_time, self.time_passed,
                                    self.interpolation_method)
                if sqrt(x ** 2 + y ** 2) <= 1.5:
                    self.x = x
                    self.y = y
                else:
                    self.get_logger().error("CALCULATED LIMIT OF POSITION XY")
                    break


            if self.z != self.newz:
                z = interpolate(self.oldz, self.newz, 0, self.target_time, self.time_passed,
                                self.interpolation_method)
                if 1 <= z <= 1.5:
                    self.z = z
                else:
                    self.get_logger().error("CALCULATED LIMIT OF POSITION Z")
                    break

            time.sleep(self.time_period)

            self.time_passed += self.time_period




# method to count linear interpolated position for given current time
def interpolate_linear(x0, x1, t0, t1, time_passed):
    return x0 + ((x1 - x0) / (t1 - t0)) * (time_passed - t0)


# method to interpolate with given method
def interpolate(x0, x1, t0, t1, time_passed, method):
    if method == "linear":
        return interpolate_linear(x0, x1, t0, t1, time_passed)



def main():
    node = Oint()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
