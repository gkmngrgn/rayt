cmake_minimum_required(VERSION 3.10)

project(rayt-cpp)

set(CMAKE_CXX_FLAGS "-std=c++17")

include_directories("./include/")

add_executable(rayt-cpp "src/main.cpp")
