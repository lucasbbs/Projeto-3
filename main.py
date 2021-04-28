import itertools

def printMedoid(files):
  arr = [(i[0],i[1]) for i in files]
  results = []
  for n in arr:
    for m in arr:
      result = sum([abs(l - k) for l, k in zip(n[1],m[1])])
      results.append((n[0], result))
  returns = []
  for n in arr:
    returns.append((n[0], ([m[1] for m in results if m[0]==n[0]])))
  return returns
         

def buildKMedoids(distances,medoid):
  arrayFiles = []
  initialMedoid = [n for n in distances if n[0] == medoid]
  distances = [n for n in distances if n[0] != medoid]
  
  arr = list(itertools.combinations(distances, K-1))
  secArray = []
  for n in arr: 
    n = list(n)
    n.extend(initialMedoid)
    secArray.append(n)

  for subset in secArray:
    array = []
    for k in range(N):
      minimum = min([(n[1][k]) for n in subset])
      array.append([(n[0], minimum) for n in subset if n[1][k] == minimum])
    array = [item for sublist in array for item in sublist]
    arrayFiles.append(array)
    newArray = [sum([n[1] for n in subArr]) for subArr in arrayFiles]

    newArray = [(m,n)  for m, n in zip([[n[0] for n in subarray] for subarray in secArray],newArray)]
  return newArray, arrayFiles


with open("vectors.txt") as f:
    lines = [line.rstrip().split(" ",1) for line in f]
files = {value[0]:(list(map(float, value[1].split()))) for value in lines}

input_files = []
T, N, K = map(int, input().split())
for n in range(N):
  filename = input()
  input_files.append((filename,files.get(filename)))
if T ==1:
  MatrixD = printMedoid(sorted(input_files))
  print(sorted([(m[0],sum(m[1])) for m in MatrixD], key=lambda x: x[1])[0][0])
if T ==2:
  MatrixD = printMedoid(sorted(input_files))
  values, clusters = buildKMedoids(MatrixD, sorted([(m[0],sum(m[1])) for m in MatrixD], key=lambda x: x[1])[0][0])
  [[print(n) for n in sorted(subarray)] for subarray in sorted(values, key=lambda x: x[1])[0][0:1]]