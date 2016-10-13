cmake_minimum_required(VERSION 2.8.3)
project(pipefollowing)

find_package(catkin REQUIRED COMPONENTS
  std_srvs
  topic_tools 
  rospy
  std_msgs
)


catkin_package(
  CATKIN_DEPENDS
    std_srvs
    topic_tools
  DEPENDS
    roscpp
)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/CMakeModules;{CMAKE_MODULE_PATH}")

find_package(PkgConfig)


INCLUDE_DIRECTORIES(${catkin_INCLUDE_DIRS})

# this disables the warnings that come mostly from osg
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-ignored-qualifiers")

add_executable(groundTruth_basic src/groundTruth_basic.cpp)
add_executable(groundTruth_turns src/groundTruth_turns.cpp)
add_executable(groundTruth_heights src/groundTruth_heights.cpp)

TARGET_LINK_LIBRARIES(groundTruth_basic ${catkin_LIBRARIES})
TARGET_LINK_LIBRARIES(groundTruth_turns ${catkin_LIBRARIES})
TARGET_LINK_LIBRARIES(groundTruth_heights ${catkin_LIBRARIES})

install(
  TARGETS
    groundTruth_turns
    groundTruth_basic
    groundTruth_heights
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(PROGRAMS src/PF_teleop.py src/PF_waypoints.py src/PF_vision.py src/manageSpreadSheet.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
  PATTERN ".svn" EXCLUDE)
