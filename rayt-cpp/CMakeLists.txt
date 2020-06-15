cmake_minimum_required(VERSION 3.10)

project(rayt-cpp)

set(CMAKE_CXX_STANDARD 17)

include_directories("./include/")

add_executable(rayt-cpp "src/main.cpp")
install(TARGETS rayt-cpp DESTINATION "${PROJECT_SOURCE_DIR}/build/bin/")
