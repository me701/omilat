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
# BLAS / Intel oneAPI MKL
#
# If USE_MKL=ON, we try to find Intel oneAPI MKL via its CMake package
# (MKLConfig.cmake). Otherwise we fall back to generic BLAS.
#
# Usage examples (after sourcing oneAPI's setvars.sh):
#   cmake -DUSE_MKL=ON -DCMAKE_BUILD_TYPE=Release ..
#   cmake -DUSE_MKL=OFF ..   # or just omit to use system BLAS
# --------------------------------------------------------------------
option(USE_MKL "Use Intel oneAPI MKL instead of generic BLAS" OFF)

if(USE_MKL)
  # oneAPI typically sets MKLROOT and installs MKLConfig.cmake under:
  #   $MKLROOT/lib/cmake/mkl
  # Sourcing setvars.sh should put that on CMAKE_PREFIX_PATH automatically,
  # but you can also pass -DCMAKE_PREFIX_PATH="$MKLROOT/lib/cmake" if needed.
  find_package(MKL CONFIG QUIET)

  if(MKL_FOUND)
    message(STATUS "Using Intel oneAPI MKL (MKL::MKL) for BLAS")
    # Emulate CMake's BLAS variables so the rest of the file can stay the same
    set(BLAS_FOUND TRUE)
    set(BLAS_LIBRARIES MKL::MKL)
  else()
    message(FATAL_ERROR
      "USE_MKL=ON but Intel oneAPI MKL not found.\n"
      "Make sure you've sourced oneAPI's setvars.sh and that MKLConfig.cmake "
      "is on CMAKE_PREFIX_PATH (e.g. -DCMAKE_PREFIX_PATH=\"$ENV{MKLROOT}/lib/cmake\").")
  endif()

else()
  # Fallback: whatever BLAS CMake can find (OpenBLAS, Netlib, etc.)
  find_package(BLAS)
endif()

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
