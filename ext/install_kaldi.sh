#!/bin/bash

# Prepare Kaldi
#!/bin/bash

# Prepare Kaldi
cd kaldi/tools
./extras/install_openblas.sh
cd ../src
# make clean (sometimes helpful after upgrading upstream?)
./configure --static --static-math=yes --static-fst=yes --use-cuda=no --openblas-root=../tools/OpenBLAS/install
make clean
make depend
make
cd ../../
