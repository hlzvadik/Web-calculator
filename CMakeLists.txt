cmake_minimum_required(VERSION 3.15)
project(Web-calculator VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/cpp-core/include)

add_library(calc_core STATIC src/calculator.cpp src/mathoperations.cpp)

set_target_properties(calc_core PROPERTIES POSITION_INDEPENDENT_CODE ON)

pybind11_add_module(calculator_module src/module.cpp)

target_link_libraries(calculator_module PRIVATE calc_core)
