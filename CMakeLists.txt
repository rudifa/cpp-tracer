# Set the minimum required version of CMake
cmake_minimum_required(VERSION 3.10)

# Set the project name and version
project(cpp-tracer VERSION 1.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the executable
add_executable(cpp-tracer main.cpp)

# Include directories
target_include_directories(cpp-tracer PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# If you have any libraries to link, you can add them here
# target_link_libraries(cpp-tracer PRIVATE some_library)
