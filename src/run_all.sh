export OMP_NUM_THREADS=1

./mv-row-x > mv_row.out
./mv-col-x > mv_col.out
./mv-row-cc-x > mv_row_cc.out
./mv-blas-x > mv_blas.out
./mv-blas-cc-x > mv_blas_cc.out

#./mm-x > mm.out
#./mm-blas-x > mm_blas.out
