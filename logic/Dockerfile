# Logic container: lightweight ROS 2 base with Python node
# Uses Jazzy ros-base to communicate over host network with the simulation
FROM ros:jazzy-ros-base

# Ensure UTF-8 locale and basic tools
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	&& rm -rf /var/lib/apt/lists/*

# Create app directory and copy code
WORKDIR /app
COPY drive_node.py /app/drive_node.py

# Optional: install Python dependencies if needed
# RUN pip3 install -r requirements.txt

# Default command is provided by docker-compose.yml or fallback here
# Use ROS-provided entrypoint to source environment, then run our node
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["python3", "/app/drive_node.py"]
