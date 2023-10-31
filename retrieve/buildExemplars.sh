#!/bin/bash
mkdir PCSD-exemplars
./search.sh PCSD-corpus ../data/PCSD/train/train.token.code PCSD-exemplars/train.exemplar ../data/PCSD/val/test.token.code PCSD-exemplars/val.exemplar ../data/PCSD/test/test.token.code PCSD-exemplars/test.exemplar
python3 generate_exemplar.py --exemplars PCSD-exemplars --output ../data/PCSD
