## This is a README dedicated to Assignment1 of CS6890- Fraud Analytics

Aim: To detect circular trade using Node2Vec Algorithm

Note: This uses the Node2Vec implementation developed by Aditya Grover and Jure Leskovec and can be found on the following page: https://github.com/aditya-grover/node2vec

Steps to run the code:

1. Create a new Conda environment using the following command:
```
conda create -n graph2vec
```

2. Activate the environment:
```
conda activate graph2vec
```

3. Install pip:
```
conda install pip
```

4. Using pip, install the following packages:
```
pip install numpy scipy pandas matplotlib scikit-learn
```

5. Install the packages mentioned in `requirements.txt`:
```
pip install -r requirements.txt
```

6. The following changes have to be made to some of the library files, because of version changes and/or depreciations. For this, first obtain the path at which the environment has been created using the following command:
```
echo $CONDA_PREFIX
```

7. Open the path in your file explorer or finder, and make the following changes:

    a. Look for the file `networkx/algorithms/dag.py`. Change the lines in import as:
    ```
    # from fractions import gcd
    from math import gcd
    ```

    b. Look for the file `gensim/models/ldamodel.py`. Under the except block after the imports, make the following change:
    ```
    # from scipy.misc import logsumexp
    from scipy.special import logsumexp
    ```

    c. Look for the file `gensim/corpora/dictionary.py`. Change the import line as:
    ```
    # from collections import Mapping, defaultdict
    from collections import defaultdict
    from collections.abc import Mapping
    ```

    d. Look for the file `gensim/models/word2vec.py`. Under the method ` _raw_word_count()`, change the return line as:
    ```     
    # return sum(len(sentence) for sentence in job)
    return sum(len(list(sentence)) for sentence in job)
    ```

8. In the file `node2vec.py` in the main directory, under the function `alias_setup()`, change the initialization of J to the following:
```
J = np.zeros(K, dtype=np.int64)
```

9. Now we are ready to run the code. Note that the node2vec implementation is within the Jupter notebook itself. In case you wish to run it on the command line terminal seperately, the command for it is as follows:
```
python main.py --input graph.txt --output embedding.emd --weighted
```