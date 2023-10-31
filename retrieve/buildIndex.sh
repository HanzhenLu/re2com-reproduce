#!/bin/bash
CLASSPATH='lucene-analyzers-common.jar:lucene-demo.jar:lucene.jar:lucene-queryparser.jar:.'
mkdir PCSD-corpus
java -cp $CLASSPATH IndexBuilder ../data/PCSD/train/train.token.code PCSD-corpus
