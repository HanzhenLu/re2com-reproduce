## Re2Com

### Requirements
- Python 3.7
    - TensorFlow 1.15
    - CUDA 10.1
    - NLTK 3.4.5
    - Java 1.8.0
- Python 2.7

### Train and Test

Our code is based on 

- download PCSD dataset
    - the originalcode files are used to produce AST, and can be found at [SG-Trans](https://github.com/shuzhenggao/SG-Trans/tree/master/python/data)
    - the code and nl files also come from SG-Trans and can be downloaded from [here](https://drive.google.com/file/d/1c0Im6M71VHn4hv7gmnQnfqa1QtbzFjPn/view)
- before we start, you file structure should like this
    - data/PCSD
        - originalcode
            - dev_originalcode
            - test_originalcode
            - train_originalcode
        - test
            - javadoc.original
        - train
            - javadoc.original
        - val
            - javadoc.original
- Generate the AST
```
    # Since the python codes in dataset is written by Python2
    # you should switch your python to 2.7 so that ast module can parse it successfully
    python extract_ast.py data/PCSD/originalcode data/PCSD/
```
```
    # Switch back to Python3
    python split_token.py data/PCSD/originalcode data/PCSD
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
- Train Re2Com model for PCSD dataset
```
    cd PCSD
    python __main__.py re2com.yaml --train
```

### Evaluation
The evaluation results are located at `PCSD/models/eval/`.
Evaluation code is based on https://github.com/tylin/coco-caption
```
    cd evaluation
    python2 evaluate.py
```
