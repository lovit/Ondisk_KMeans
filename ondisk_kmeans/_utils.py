from math import sqrt

class MatrixMarket:
    def __init__(self, mm_fname, iter_line=True, do_normalize=True):
        self.fname = mm_fname
        self.iter_line = iter_line
        self.do_normalize = do_normalize
        with open(mm_fname, encoding='utf-8') as f:
            for _ in range(2):
                next(f)
            self.n_rows, self.n_cols, self.n_elements = [int(v) for v in next(f).split()]

    def __iter__(self):
        with open(self.fname, encoding='utf-8') as f:
            for _ in range(3):
                next(f)
            self._n_iter = 0
            if self.iter_line:
                for row in f:
                    self._n_iter += 1
                    i,j,v = row.split()
                    yield int(i)-1, int(j)-1, float(v)
            else:
                i_prev = -1
                d = {}
                for row in f:
                    self._n_iter += 1
                    i,j,v = row.split()
                    i, j, v = int(i)-1, int(j)-1, float(v)
                    if i != i_prev:
                        if d:
                            if self.do_normalize:
                                yield i_prev, self._normalize(d)
                            else:
                                yield i_prev, d
                        d = {}
                    i_prev = i
                    d[j] = v
                if d:
                    if self.do_normalize:
                        yield i_prev, self._normalize(d)
                    else:
                        yield i_prev, d

    def _normalize(self, d):
        sum_ = sum([v**2 for v in d.values()])
        return {k:sqrt(v**2/sum_) for k,v in d.items()}
        
    def __str__(self):
        return 'MatrixMarket file (n_rows={}, n_cols={}, n_elements={})'.format(self.n_rows, self.n_cols, self.n_elements)