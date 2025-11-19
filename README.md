# README

Much numerical computing relies heavily on linear algebra.  

I believe that "only masochists implement linear algebra themselves", or OMILAT.

If we sound that out like the egg dish, it's easy to remember.

This repository contains resources to guide students as they tinker, test, reflect, rebuild, and retest their code to compute dot products, matrix-vector products, and matrix-matrix products.  Along the way, we'll rope in CMake, various BLAS and LAPACK libraries, OpenMP, and CUDA.

## Installing BLAS

A default implementation of BLAS can be installed via

```
sudo apt install libblas-dev
```

A possibly better variant is OpenBLAS:

```
sudo apt install libopenblas-dev
```

## Installing Intel® oneAPI HPC Toolkit 

```
sudo apt update
sudo apt install -y gpg-agent wget
wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list
sudo apt update
sudo apt install intel-oneapi-hpc-toolkit
```
