# Ondisk_KMeans

Sparse matrix 데이터에 대하여, disk io 를 이용한 k-means clustering

Sparse matrix 파일은 document id (= row id) 순으로 묶여 있다고 가정합니다 (반드시 정렬이 되야 하는 것은 아닙니다)

	(예시)
	1 3 1
	1 72 5
	1 4 2
	...
	5 22 1
	5 91 2
	...
	3 12 1
	3 7 1

## Usage

학습은 sparse matrix 파일주소를 입력합니다. 

	from ondisk_kmeans import Ondisk_KMeans
	from ondisk_kmeans import MatrixMarket

	mm_fname = '' # sparse matrix file path
	kmeans = Ondisk_KMeans(n_clusters=10, max_iter=5)
	labels = kmeans.fit_predict(mm_fname)

Empty vector (zero vector)의 경우에는 cluster 할당이 되지 않기 때문에 label이 -1 입니다.

	from collections import Counter
	Counter(labels)

	Counter({-1: 6,
                  0: 148,
                  1: 78,
                  2: 85,
                  3: 307,
                  4: 197,
                  5: 184,
                  6: 301,
                  7: 35,
                  8: 50,
                  9: 109})

## Todo

1. 현재는 cosine distance만 만들었습니다. Euclidean 이 들어갈 예정입니다.
1. tolerance에 의한 convergence check를 하지 않습니다. max_iter 만큼 반복하는 부분에 대하여 early-stopping 이 들어갈 예정입니다. 
