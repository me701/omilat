// driver-mv.cpp

#include <iostream>
#include <vector>
#include <algorithm>
#include <omp.h>

extern "C" {
    void dgemv_(const char* TRANS, const int* M, const int* N,
                const double* ALPHA, const double* A, const int* LDA,
                const double* X, const int* INCX,
                const double* BETA, double* Y, const int* INCY);
}

int main()
{
    double alpha = 1.0;
    double beta  = 0.0;
    int incx = 1;
    int incy = 1;

    for (int j = 1; j <= 100; ++j) {
        // Matrix size
        int m   = 10 * 2 * j;
        int n   = m;
        int lda = m;   // not really used here, but mirrored from Fortran
        char trans = 'N';
        int incx = 1, incy = 1;

        // Allocate and initialize A, x, y
        std::vector<double> A(m * n, 1.0);  // A = 1.0
        std::vector<double> x(n, 1.0);      // x = 1.0
        std::vector<double> y(m, 0.0);      // y = 0.0

        // Loop count for timing (matches Fortran maxi)
        int maxi = 200;

        double t0 = omp_get_wtime();
        for (int it = 0; it < maxi; ++it) {
            std::fill(y.begin(), y.end(), 0.0);
            dgemv_(&trans, &m, &n, &alpha, A.data(), &lda,
                   x.data(), &incx, &beta, y.data(), &incy);
        }
        double t = omp_get_wtime() - t0;

        // 2*m*m flops per matvec, *maxi applications
        double flops  = 2.0 * static_cast<double>(m) * static_cast<double>(m) * maxi;
        double gflops = flops / 1.0e9 / t;

        // Match Fortran output style: "m  Gflops"
        std::cout << m << " " << gflops << std::endl;
    }

    return 0;
}
