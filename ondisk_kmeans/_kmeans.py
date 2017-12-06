import random
import numpy as np
from sklearn.preprocessing import normalize as sknormalize
from ._utils import MatrixMarket

class Ondisk_KMeans:
    def __init__(self, n_clusters, max_iter=20, tol=0.001, metric='cosine', verbose=True):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol if 0 <= tol < 1 else 0.001
        self.verbose = verbose
        self.metric = metric
        self._distance = self._euclidean if metric == 'euclidean' else self._cosine
        
        self.labels = None

    def _euclidean(self, query, centroid):
        """query: {term:count}
        centroid: list of list - like
        """
        return 0
    
    def _cosine(self, query, centroid):
        """query: {term:count}
        centroid: list of list - like
        """
        sim = sum({v*centroid[j] for j,v in query.items()})
        return 1 - sim
    
    def _most_similar(self, j_dict):
        cdist = [self._distance(j_dict, centroid) for centroid in self.c0]
        return sorted(enumerate(cdist), key=lambda x:x[1])[0][0]
    
    def fit_predict(self, mm_fname):
        mm = MatrixMarket(mm_fname)
        self._initialize(mm)

        mm.iter_line = False
        for n_iter in range(1, self.max_iter+1):
            c1 = np.zeros((self.n_clusters, self.n_words))
            self.labels = [-1] * self.n_docs
            for n_nonempty_doc, (i, j_dict) in enumerate(mm):
                best_c = self._most_similar(j_dict)
                self.labels[i] = best_c
                for j, v in j_dict.items():
                    c1[best_c,j] += v
                if self.verbose and n_nonempty_doc % 100 == 99:
                    print('\r  - iter = {} / {}, {} %'.format(n_iter, self.max_iter, '%.2f'%(100*n_nonempty_doc/self._n_nonempty_docs)), flush=True, end='')
            self.c0 = sknormalize(c1)
            if self.verbose:
                print('\rIteration = {} was done{}'.format(n_iter, ' '*40), flush=True)
        return self.labels

    def _initialize(self, mm):
        self.n_docs, self.n_words, self.n_elements = mm.n_rows, mm.n_cols, mm.n_elements
        # Scanning document idx
        docs_set = set()
        for n_row, (i, _, _) in enumerate(mm):
            if self.verbose and n_row % 5000 == 4999:
                print('\r  - scanning document idx {} %'.format('%.2f'%(100*n_row/self.n_elements)), flush=True, end='')
            if not i in docs_set:
                docs_set.add(i)
        self._n_nonempty_docs = len(docs_set)
        self.c0 = np.zeros((self.n_clusters, self.n_words))
                
        # Select seeds
        if self.verbose:
            print('\r  - initialize centroids', flush=True, end='')
        seeds = random.sample(docs_set, self.n_clusters)
        mm.iter_line = False
        _c0_index = 0
        for i, j_dict in mm:
            if i in seeds:
                for j, v in j_dict.items():
                    self.c0[_c0_index,j] = v
                _c0_index += 1
            if _c0_index == (self.n_clusters):
                break
        if self.verbose:
            print('\rInitialization was done{}'.format(' '*40), flush=True)