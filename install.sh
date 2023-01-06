#!/bin/bash

set -e

git submodule init
git submodule update

./install_deps.sh
(cd ext && ./install_kaldi.sh && make depend && make && rm -rf kaldi *.o)
./install_models.sh
