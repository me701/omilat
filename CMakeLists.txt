cmake_minimum_required(VERSION 3.15)

project(me701_matvec LANGUAGES Fortran CXX)

if(CMAKE_SOURCE_DIR STREQUAL CMAKE_BINARY_DIR)
  message(FATAL_ERROR "Please use a separate build directory!")
endif()

# Default to Release if nothing set
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# Put all executables in build/bin
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# Sources directory
set(SRC ${CMAKE_SOURCE_DIR}/src)

# --------------------------------------------------------------------
# OpenMP: required because the drivers use omp_get_wtime()
# --------------------------------------------------------------------
find_package(OpenMP REQUIRED)

# --------------------------------------------------------------------
# BLAS (only needed for the *-blas-* targets)
# tip: you can steer detection with -DBLA_VENDOR=OpenBLAS (etc.)
# --------------------------------------------------------------------
find_package(BLAS)

# -------------------------
# Fortran targets
# -------------------------
add_executable(mv-row-x
  ${SRC}/matvec-row.f90
  ${SRC}/driver-mv.f90
)
target_link_libraries(mv-row-x PRIVATE OpenMP::OpenMP_Fortran)

add_executable(mv-col-x
  ${SRC}/matvec-col.f90
  ${SRC}/driver-mv.f90
)
target_link_libraries(mv-col-x PRIVATE OpenMP::OpenMP_Fortran)

if(BLAS_FOUND)
  add_executable(mv-blas-x ${SRC}/driver-mv.f90)
  target_link_libraries(mv-blas-x PRIVATE OpenMP::OpenMP_Fortran ${BLAS_LIBRARIES})
else()
  message(STATUS
    "BLAS not found — skipping mv-blas-x. "
    "Install a BLAS (e.g., libblas / OpenBLAS) or pass -DBLA_VENDOR=OpenBLAS.")
endif()

# -------------------------
# C++ targets
# -------------------------

add_executable(mv-row-cc-x
  ${SRC}/driver-mv.cc
  ${SRC}/matvec-row.cc
)
target_link_libraries(mv-row-cc-x PRIVATE OpenMP::OpenMP_CXX)

if(BLAS_FOUND)
  add_executable(mv-blas-cc-x ${SRC}/driver-mv.cc)
  target_link_libraries(mv-blas-cc-x PRIVATE OpenMP::OpenMP_CXX ${BLAS_LIBRARIES})
endif()

# -------------------------
# Phony targets 
# -------------------------
add_custom_target(simple)
add_dependencies(simple mv-row-x mv-row-cc-x mv-col-x)

if(TARGET mv-blas-x)
  add_custom_target(blas)
  add_dependencies(blas mv-blas-x mv-blas-cc-x)
endif()
