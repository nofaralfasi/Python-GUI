def half(matrix, k=1):
    return [(matrix[i])[-len(matrix[i]) + i * (1 - k):len(matrix[i]) - k*len(matrix[i]) + i + k] for i in range(len(matrix))]

def decrypt(string, key=1):
    str1 = ""
    for i in range(len(string)):
        new_char = ord(string[i]) - key
        if new_char < ord('a'):
            new_char += 26
        str1 += chr(new_char)
    return str1

def div_by(n, limit):
    k = 0
    while k < limit:
        yield k
        k += n

def merge(l, r):
    iter1, iter2 = iter(l), iter(r)
    n1, n2 = next(iter1), next(iter2)
    while n1 is not None and n2 is not None:
        if n1 < n2:
            yield n1
            n1 = next(iter1, None)
        else:
            yield n2
            n2 = next(iter2, None)
    if n1 is None:
        n1, iter1 = n2, iter2
    while n1 is not None:
        yield n1
        n1 = next(iter1, None)

def rank(file_name, how_to_rank='total'):
    f = open(file_name, "r")
    words, counts = [], []
    data = f.readlines()
    for line in data:
        words += line.split()
    f.close()
    for i in range(0, len(words), 4):
        g, s, p = int(words[i + 1]), int(words[i+2]), int(words[i+3])
        if how_to_rank == 'total':
            counts.append((words[i], g+s+p, 0))
        elif how_to_rank == 'weighted':
            counts.append((words[i], g*3+s*2+p, 0))
        elif how_to_rank == 'gold':
            counts.append((words[i], g + s + p, g))
    counts.sort(key=lambda tup: (tup[2], tup[1]), reverse=True)
    for i in range(len(counts)):
        yield counts[i][0] + " : " + str(counts[i][1])
