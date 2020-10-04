cmake_minimum_required(VERSION 3.10)

project(rayt-cpp)

set(CMAKE_CXX_STANDARD 17)

if(NOT DEFINED ENV{VCPKG_DIR})
  message(FATAL_ERROR "VCPKG_DIR is not defined in the environment.")
endif()

set(VCPKG_DIR "$ENV{VCPKG_DIR}")
message("VCPKG_DIR: ${VCPKG_DIR}")
set(CMAKE_TOOLCHAIN_FILE "${VCPKG_DIR}/scripts/buildsystems/vcpkg.cmake" CACHE STRING "")

find_package(Stb REQUIRED)

add_executable(rayt_one_weekend "one_weekend.cpp")
install(TARGETS rayt_one_weekend DESTINATION "${PROJECT_SOURCE_DIR}/build/bin")

add_executable(rayt_next_week "next_week.cpp")
install(TARGETS rayt_next_week DESTINATION "${PROJECT_SOURCE_DIR}/build/bin")
