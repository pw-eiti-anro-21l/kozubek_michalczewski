import os
from glob import glob
from setuptools import setup

package_name = 'LAB1'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='01149402@pw.edu.pl',
    description='ANRO_LAB1',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'node = LAB1.node:main'
            #'talker = py_pubsub.publisher_member_function:main',
            #'listener = py_pubsub.subscriber_member_function:main',
        ],
    },
)
