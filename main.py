def printMedoid(files):
    arr = [(i[0], i[1]) for i in files]
    results = []
    for n in arr:
        for m in arr:
            results.append((n[0], sum([abs(l - k) for l, k in zip(n[1], m[1])])))
    returns = []
    for n in arr:
        returns.append((n[0], ([m[1] for m in results if m[0] == n[0]])))
    return returns

def buildKMedoids(distances, medoid):

    medoids = [i for i, n in enumerate(distances) if n[0] == medoid]
    unselected = [i for i, n in enumerate(distances) if n[0] != medoid]
    for k in range(K-1):
        Cij, ganhos = 0, []
        for i in unselected:
            Cij = 0
            for j in unselected:
                Dj, lista = 0, []
                if j != i:
                    for l in medoids:
                        lista.append(distances[j][1][l])
                    Dj = min(lista)
                    dij = distances[i][1][j]
                    Cij += Dj - dij if Dj > dij else 0
            ganhos.append((Cij, i))
        novo_medoid = sorted(ganhos, key=lambda x: x[0], reverse=True)[0]
        medoids.append(novo_medoid[1])
        unselected.remove(novo_medoid[1])
    return medoids, unselected

def buildClusters(medoids, samples):
    samples = [(n[0], i) for i, n in enumerate(input_files) if i in samples]
    distances = [n for i, n in enumerate(
        MatrixD) if n[0] in [n[0] for n in samples]]
    distances = [(k, sorted(vs,  key=lambda x: x[0])[0])
                 for k, vs in [(n, [(values[m], m) for m in medoids]) for n, values in distances]]

    distances = [(input_files[values[1]][0], x)for x, values in distances]
    return distances

with open("vectors.txt") as f:
    lines = [line.rstrip().split(" ", 1) for line in f]
files = {value[0]: (list(map(float, value[1].split()))) for value in lines}

input_files = []
T, N, K = map(int, input().split())
for n in range(N):
    filename = input()
    input_files.append((filename, files.get(filename)))
input_files.sort()
if T == 1:
    MatrixD = printMedoid(input_files)
    print(sorted([(m[0], sum(m[1]))
          for m in MatrixD], key=lambda x: x[1])[0][0])
if T == 2:
    MatrixD = printMedoid(input_files)
    medoids, _ = buildKMedoids(MatrixD, sorted(
        [(m[0], sum(m[1])) for m in MatrixD], key=lambda x: x[1])[0][0])
    medoids = [n[0] for i, n in enumerate(input_files) if i in medoids]
    [print(n) for n in sorted(medoids)]
if T == 3:
    MatrixD = printMedoid(input_files)
    clusters, samples = buildKMedoids(MatrixD, sorted(
        [(m[0], sum(m[1])) for m in MatrixD], key=lambda x: x[1])[0][0])
    points = {input_files[n][0]: [] for n in clusters}
    clusters = buildClusters(clusters, samples)
    filenames = [n[0] for n in input_files]
    for each, file in clusters:
        points[each].append(file)
    for each, el in sorted(points.items()):
        print(each)
        [print(" ", value) for value in el if value != each]