import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    urdf_file_name = 'robot.urdf.xml'
    urdf = os.path.join(get_package_share_directory('zadanie4'), urdf_file_name)

 
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        Node(
            package='zadanie4',
            executable='nie_kdl',
            name='non_kdl_pose_stamped',
            parameters=[{
                'use_sim_time': use_sim_time,
            }],
            output='screen'),

        Node(
            package='zadanie4',
            executable='kdl',
            name='kdl_pose_stamped',
            parameters=[{
                'use_sim_time': use_sim_time,
            }],
            output='screen'),

    ])
