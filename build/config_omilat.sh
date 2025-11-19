# comment if you do not have Intel's one API
source /opt/intel/oneapi/setvars.sh

rm CMakeCache.txt 
cmake                                  \
  -DUSE_MKL=OFF                        \
  -DCMAKE_BUILD_TYPE=Release           \
  -DBLA_VENDOR=OpenBLAS                \
..

make

