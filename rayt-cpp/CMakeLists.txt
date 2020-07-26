cmake_minimum_required(VERSION 3.10)

project(rayt-cpp)

set(CMAKE_CXX_STANDARD 17)

add_executable(rayt_one_weekend "one_weekend.cpp")
install(TARGETS rayt_one_weekend DESTINATION "${PROJECT_SOURCE_DIR}/bin")

add_executable(rayt_next_week "next_week.cpp")
install(TARGETS rayt_next_week DESTINATION "${PROJECT_SOURCE_DIR}/bin")
