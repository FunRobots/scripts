#!/bin/bash

#script for running candybot_vr docker container with candybot_v2 ROS package
#	commands:
#
#	run_package [-d] - run candybot_v2 ROS package, -d - as daemon
#
#	run_roscore [-d] - run roscore in container, -d - as daemon
#
#	attach - attach to running candybot_vr container
#
#	commit - commit last runned candybot_vr container
#
#	run_node [-d] <node_name> - run candybot_v2 ROS package node, -d - as daemon
#
#	update_package - update candybot_v2 package from github repository

ROS_PACKAGE_NAME="candybot_v2"
DOCKER_IMAGE_NAME="candybot_gui"

function run_package(){
	key="-ti"
	
	if [ "$1" == "-d" ]
	then
		key="-d"
	fi
	
	sudo docker run "$key" -p 11311:11311 -p 9090:9090 -w="/root/catkin_ws" --privileged --device /dev:/dev "$DOCKER_IMAGE_NAME" /bin/bash -c "source /opt/ros/kinetic/setup.bash; roslaunch $ROS_PACKAGE_NAME run.launch"
}

function run_roscore(){
	key="-ti"
	
	if [ "$1" == "-d" ]
	then
		key="-d"
	fi
	
	sudo docker run "$key" -p 11311:11311 -p 9090:9090 -w="/root/catkin_ws" --privileged --device /dev:/dev "$DOCKER_IMAGE_NAME" /bin/bash -c "source /opt/ros/kinetic/setup.bash; roscore"
}


case $1 in
"enter_package" )
	sudo docker run -ti -p 11311:11311 -p 9090:9090 -w="/root/catkin_ws" --privileged --device /dev:/dev "$DOCKER_IMAGE_NAME"
	;;
	
"run_package" )
	run_package $2
	;;
	
"run_roscore" )
	run_roscore $2
	;;
	
"attach" )
	sudo docker exec -ti $(sudo docker ps -lq --filter "ancestor=$DOCKER_IMAGE_NAME") /bin/bash
	;;
	
"commit" )
	sudo docker commit $(sudo docker ps -lq --filter "ancestor=$DOCKER_IMAGE_NAME") "$DOCKER_IMAGE_NAME"
	;;
	
"run_node" )
	sudo docker run -w="/root/catkin_ws" -ti -p 11311:11311 -p 9090:9090 --privileged --device /dev:/dev "$DOCKER_IMAGE_NAME" /bin/bash -c "source /opt/ros/kinetic/setup.bash; roslaunch $ROS_PACKAGE_NAME $2.launch"
	;;

*)
	sudo docker run -w="/root/catkin_ws" -ti -p 11311:11311 -p 9090:9090 --privileged --device /dev:/dev "$DOCKER_IMAGE_NAME" /bin/bash -c "$1"
	;;

esac
