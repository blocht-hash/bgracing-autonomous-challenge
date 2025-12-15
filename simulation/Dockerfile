# Base image with ROS 2 Jazzy and Gazebo pre-installed
FROM osrf/ros:jazzy-desktop-full

# Install the TurtleBot3 simulation packages
# This includes the robot model and the world files
RUN apt-get update && apt-get install -y \
    ros-jazzy-turtlebot3-gazebo \
    ros-jazzy-turtlebot3-msgs \
    && rm -rf /var/lib/apt/lists/*

# Set the robot model to 'waffle' (includes LiDAR and Camera)
ENV TURTLEBOT3_MODEL=waffle

# Command to run when the container starts:
# This launches Gazebo with the standard TurtleBot3 world.
# It automatically starts publishing to topics like /scan and /odom.
CMD ["ros2", "launch", "turtlebot3_gazebo", "turtlebot3_world.launch.py"]