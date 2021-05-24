import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'zadanie4'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.py')),
        (os.path.join('share', package_name), glob('urdf/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='przemyslaw',
    maintainer_email='przemyslaw@student.com',
    description='manipulator',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joint_state_publisher = zadanie4.joint_state_publisher:main',
            'nie_kdl = zadanie4.nie_kdl:main',
            'kdl = zadanie4.kdl:main',
            'jint = zadanie4.jint:main',
            'oint = zadanie4.oint:main',
            'ikin = zadanie4.ikin:main'
        ],
    },
)
