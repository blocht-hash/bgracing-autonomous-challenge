# BGRacing Autonomous Challenge: TurtleBot3 Obstacle Avoidance

## 1. Introduction
This project implements a robotic data processing pipeline using **ROS 2 Jazzy** and **Docker**. It is designed to demonstrate autonomous navigation capabilities by simulating a TurtleBot3 robot that acquires environmental data and processes it in real-time to avoid obstacles.

The system is fully containerized, splitting the simulation (Data Acquisition) and the control logic (Data Processing) into two distinct containers, complying with the BGRacing assignment architecture requirements.

## 2. System Architecture
The pipeline consists of two Docker containers running **Ubuntu 24.04** on the host network:

### Container A: `bgr_sim` (Data Source)
* **Base Image:** `osrf/ros:jazzy-desktop-full`
* **Role:** Acts as the data generator. It runs the **Gazebo** simulator with the `turtlebot3_world` map.
* **Data Published:**
    * `/scan`: LiDAR point cloud data (LaserScan) describing the environment.
    * `/odom`: Odometry data.

### Container B: `bgr_logic` (Data Processing)
* **Language:** Python 3.12 (via ROS 2 Jazzy)
* **Role:** Acts as the autonomous driver. It subscribes to the sensor data, calculates distances, and commands the robot.
* **Key Logic (`drive_node.py`):**
    * Subscribes to `/scan` with a **RELIABLE/VOLATILE** QoS profile to match the simulation output.
    * Filters LiDAR ranges to isolate the front sector (approx. ±15 degrees).
    * **Decision Making:**
        * **Clear Path (> 0.4m):** Move forward at 0.35 m/s.
        * **Obstacle Detected (< 0.4m):** Stop linear motion and rotate at 0.5 rad/s until the path is clear.
    * Publishes velocity commands to `/cmd_vel`.

## 3. Dataset & Data Properties
Instead of a static CSV, this project utilizes **Live Simulation Data**:
* **Source:** Simulated LiDAR (Light Detection and Ranging) sensor on a TurtleBot3 Waffle model.
* **Data Format:** `sensor_msgs/msg/LaserScan`
* **Rate:** Real-time stream.
* **Environment:** Standard TurtleBot3 World (includes hexagonal and box obstacles).

## 4. Prerequisites
* **OS:** Linux (Ubuntu recommended for native display support).
* **Docker Engine** & **Docker Compose**.
* **X11 Server:** Required for viewing the Gazebo GUI (simulation visualization).

## 5. How to Run

1.  **Clone the Repository:**
    ```bash
    git clone <YOUR_REPO_URL>
    cd <YOUR_REPO_NAME>
    ```

2.  **Allow GUI Access (for Gazebo):**
    Run the following command to allow Docker to render the simulation window on your screen:
    ```bash
    xhost +local:root
    ```

3.  **Build and Launch:**
    Use Docker Compose to build both containers and start the pipeline:
    ```bash
    docker compose up --build
    ```
4. **then open new terminal and run the following three commands:**

    ```bash
    docker exec -it bgr_sim bash 
    ```
     ```bash
     source /opt/ros/jazzy/setup.bash
    ```
    ```bash
     ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/TwistStamped "{header: {frame_id: 'world'}, twist: {linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}}"
    ```             

6.  **Expected Output:**
    * A Gazebo window will open showing the TurtleBot3 in a world with pillars.
    * **In the terminal:** You will see logs from the logic container:
        ```text
        [auto_driver]: Front Distance: 1.25m
        [auto_driver]: Front Distance: 0.38m
        ...
        ```
    * **In the Simulation:** The robot will drive forward. When it gets close to a pillar (approx. 40cm), it will stop, rotate left, and continue moving once the path is clear.

---
**Author:** Tal Bloch 
