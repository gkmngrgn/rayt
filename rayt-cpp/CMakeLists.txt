cmake_minimum_required(VERSION 3.10)

project(rayt-cpp)

set(CMAKE_CXX_STANDARD 17)

add_executable(one_weekend "one_weekend.cpp")
install(TARGETS one_weekend DESTINATION "${PROJECT_SOURCE_DIR}/build/bin")

add_executable(next_week "next_week.cpp")
install(TARGETS next_week DESTINATION "${PROJECT_SOURCE_DIR}/build/bin")
