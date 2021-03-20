from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        Node(
            package='LAB1',
            prefix='gnome-terminal --',
            executable='node',
            output='screen',
            parameters=[
                {'forward_key': 't'},
                {'backward_key': 'g'},
                {'left_key': 'f'},
                {'right_key': 'h'}
            ]

        )

    ])