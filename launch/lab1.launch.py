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
            name='control',
            parameters=[
                {'forward_key': 'i'},
                {'backward_key': 'k'},
                {'left_key': 'j'},
                {'right_key': 'l'}
            ]


        )
 
    ])
