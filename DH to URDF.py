#!/usr/bin/python

import sys
import math

theta1 = 0
theta2 = 0
d3 = 0

if len(sys.argv) == 4 :
    theta1 = float(sys.argv[1])*math.pi/180
    theta2 = float(sys.argv[2])*math.pi/180
    d3 = float(sys.argv[3])


f = open("r2d2.urdf.xml", "w")
text_list = ['<robot name="r2d2">'
'  <link name="base_link">'
'    <visual>'
'      <geometry>'
'        <box size="0.5 0.5 6"/>'
'      </geometry>'
'       <origin rpy="0 0 0" xyz="0 0 3"/>'
'      <material name="grey">'
'    <color rgba="0.75 0.75 0.75 1"/>'
'  	</material>'
'    </visual>'
'  </link>'
'  <link name="second_link">'
'    <visual>'
'      <geometry>'
'        <box size="0.1 0.1 2"/>'
'      </geometry>'
'        <material name="red">'
'    	<color rgba="1 0 0 1"/>'
'  		</material>'
'      <origin rpy="0 1.57075 0" xyz="1 0 0"/>'
'    </visual>'
'  </link>'
'<link name="third">'
'    <visual>'
'      <geometry>'
'         <box size="0.1 0.1 4"/>'
'      </geometry>'
'      	<material name="white">'
'    	<color rgba="1 1 1 1"/>'
'  		</material>'
'      <origin rpy="0 0 0" xyz="3 0 -2" />'
'    </visual>'
'  </link>'
'  <link name="third_link">'
'    <visual>'
'      <geometry>'
'        <box size="0.1 0.1 3"/>'
'      </geometry>'
'        <material name="blue">'
'    	<color rgba="0 0 0.8 1"/>'
'  		</material>'
'      <origin rpy="0 1.57075 0" xyz="1.5 0 0" />'
'    </visual>'
'  </link>'
'  <link name="end_link">'
'    <visual>'
'      <geometry>'
'        <box size="0.1 0.1 0.1"/>'
'      </geometry>'
'        <material name="green">'
'    	<color rgba="0 1 0 1"/>'
'  		</material>'
'       <origin rpy="0 0 0" xyz="-0.1 0 3.9" />'
'    </visual>'
'  </link>'
'  <joint name="base_to_second" type="continuous">'
'    <parent link="base_link"/>'
'    <child link="second_link"/>'
'    <origin xyz="0 0 6"/>'
'    <axis xyz="0 0 1"/>'
'  </joint>'
'  <joint name="second_to_third" type="revolute">'
'    <limit effort="1000.0" lower="-0.85" upper="0.85" velocity="0.5"/>'
'    <parent link="second_link"/>'
'    <child link="third_link"/>'
'    <origin rpy="0 0 0" xyz="2 0 0" />'
'    <axis xyz="0 0 1"/>'
'  </joint>'
'	<joint name="second" type="fixed">'
'    <parent link="second_link"/>'
'    <child link="third"/>'
'    <origin rpy="0 0 0" xyz="2 0 0" />'
'    <axis xyz="0 0 1"/>'
'  </joint>'
'  <joint name="linear_joint" type="prismatic">'
'    <parent link="third_link"/>'
'    <child link="end_link"/>'
'    <origin rpy="0 3.14 0" xyz="3 0 -0.05" />'
'    <limit effort="1000.0" lower="0" upper="10" velocity="0.5"/>'
'    <axis xyz="0 0 1"/>'
'  </joint>'
'</robot>']
f.writelines(text_list)
f.close()
