extern "C"
void dgemv_(const char* TRANS, const int* M, const int* N,
            const double* ALPHA, const double* A, const int* LDA,
            const double* X, const int* INCX,
            const double* BETA, double* Y, const int* INCY)
{

    // A stored row-major: A[i*n + j]
    for (int i = 0; i < *M; ++i) {
        double sum = 0.0;
        for (int j = 0; j < *N; ++j) {
            sum += A[i * *N + j] * X[j];
        }
        Y[i] = sum;
    }
}