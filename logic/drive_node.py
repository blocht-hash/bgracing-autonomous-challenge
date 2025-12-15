#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
import numpy as np

class SubscriberNode(Node):
    def __init__(self):
        super().__init__('auto_driver')

        # --- התאמה מושלמת ללוג ששלחת ---
        # Log showed: Reliability: RELIABLE, Durability: VOLATILE
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # 1. Subscriber
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile) 
            
        # 2. Publisher
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.get_logger().info('DRIVER STARTED: QoS Matches Simulation (Reliable/Volatile)')

    def scan_callback(self, msg):
        # עיבוד הנתונים
        ranges = np.array(msg.ranges)
        
        # בדיקת הסקטור הקדמי
        left_side = ranges[0:15]
        right_side = ranges[-15:]
        front_sector = np.concatenate((left_side, right_side))
        
        # סינון
        front_sector = front_sector[front_sector > 0.05]
        front_sector = front_sector[front_sector < 10.0]
        
        min_distance = 10.0
        if len(front_sector) > 0:
            min_distance = np.min(front_sector)

        # --- הדפסה ללוג: חיווי חיים ---
        # זה ידפיס לך את המרחק למסך בכל שבריר שנייה
        self.get_logger().info(f'Front Distance: {min_distance:.2f}m')

        # --- נהיגה ---
        cmd = Twist()
        
        if min_distance < 0.4:
            # מכשול קרוב!
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5
        else:
            # סע!
            cmd.linear.x = 0.35
            cmd.angular.z = 0.0
            
        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()