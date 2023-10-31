## Re2Com

### Requirements
- Python 3.7
- TensorFlow 1.15
- CUDA 10.1
- NLTK 3.4.5
- Java 1.8.0

### Train and Test

Our code is based on 

- download PCSD dataset
    - we choose [tree-sitter](https://github.com/tree-sitter) tool to extract, so you have to clone tree-sitter-python-master repository under 'tree/vendor/' 
    - the originalcode files are used to produce AST, and can be found at [SG-Trans](https://github.com/shuzhenggao/SG-Trans/tree/master/python/data)
    - the code and nl files also come from SG-Trans and can be downloaded from [here](https://drive.google.com/file/d/1c0Im6M71VHn4hv7gmnQnfqa1QtbzFjPn/view)
- before we start, you file structure should like this
    - tree
        - build
        - vendor
            - tree-sitter-python-master(clone from the former link)
    - data/PCSD
        - originalcode
            - dev_originalcode
            - test_originalcode
            - train_originalcode
        - test
            - code.original_subtoken
            - javadoc.original
        - train
            - code.original_subtoken
            - javadoc.original
        - val
            - code.original_subtoken
            - javadoc.original
- Generate the AST
```
    python extract_ast.py data/PCSD/originalcode data/PCSD/
```
- Process the dataset and generate the vocabulary
```
    python data-process.py
```
- Build the Retrieval corpus
```
    cd retrieve
    ./compile.sh
    ./buildIndex.sh
```
- Generate exemplars for training and testing
```
    cd retrieve
    ./buildExemplars.sh
```
- Train Re2Com model for standard dataset
```
    cd standard
    python __main__.py re2com.yaml --train -v
```
- Train Re2Com model for challenge dataset
```
    cd challenge
    python __main__.py challenge.yaml --train -v
```
- Retrieve code with standard dataset as corpus
  - Note that the output file will only contain numbers, which are the line numbers of the retrieved code.
```
    cd retrieve
    ./search.sh standard-corpus ${input-file} ${output-file}
```

### Evaluation
The evaluation results are located at `standard/models/eval/` or `challenge/models/eval/`.
Evaluation code is based on https://github.com/tylin/coco-caption
```
    cd evaluation
    python2 evaluate.py
```
