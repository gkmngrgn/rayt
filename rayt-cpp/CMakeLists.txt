cmake_minimum_required(VERSION 3.10)

project(rayt-cpp)

set(CMAKE_CXX_STANDARD 17)

add_executable(rayt-cpp "main.cpp")
install(TARGETS rayt-cpp DESTINATION "${PROJECT_SOURCE_DIR}/build/bin/")
