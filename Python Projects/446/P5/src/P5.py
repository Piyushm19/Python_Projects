from matplotlib import pyplot
from math import log

def NDCG(k, rele, rank):
    i = 0
    DCG = 0
    k = min(k, len(rank))
    for r in rank:
        if i < k:
            if r in rele:
                DCG += ((2 ** rele[r]) - 1) / log(1 + (i + 1), 2)
        else:
            break
        i += 1
    temp = rele.copy()
    i = 0
    iDCG = 0
    k = min(k, len(temp))
    while i < k:
        max_key = max(temp, key=temp.get)
        iDCG += ((2 ** temp[max_key]) - 1) / log(1 + (i + 1), 2)
        temp[max_key] = -1
        i += 1
    return DCG / iDCG

def MRR(rele, rank):
    acc = 1
    for r in rank:
        if r in rele:
            if rele[r] > 0:
                return 1 / acc
        acc += 1
    return 0

def precision(k, rele, rank):
    acc = 0
    numerator = 0
    k = min(k, len(rank))
    for r in rank:
        if acc < k and r in rele:
            if rele[r] > 0:
                numerator += 1
        acc += 1
    return numerator / k

def recall(k, rele, rank):
    acc = 0
    numerator = 0
    k = min(k, len(rank))
    for r in rank:
        if acc < k and r in rele:
            if rele[r] > 0:
                numerator += 1
        acc += 1
    denominator = 0
    for r in rele:
        if rele[r] > 0:
            denominator += 1
    return numerator / denominator

def F1(k, rele, rank):
    R = recall(k, rele, rank)
    P = precision(k, rele, rank)
    if R + P == 0:
        return 0
    return (2 * R * P) / (R + P)

def MAP(rele, rank):
    R = 0
    P = 0
    acc = 0
    for i in range(1, len(rank) + 1):
        R1 = recall(i, rele, rank)
        P1 = precision(i, rele, rank)
        if (R1 > R):
            P += P1
            acc += 1
        R = R1
    if acc == 0:
        return 0
    return P / acc

def main():
    relevance = {}
    bm25Data = {}
    qlData = {}
    sdmData = {}
    stressData = {}
    f1 = open("qrels", 'r')
    for line in f1.readlines():
        cols = line.split()
        relevance.setdefault(cols[0], {})
        relevance[cols[0]][cols[2]] = int(cols[3])
    f1.close()

    f2 = open("bm25.trecrun", 'r')
    for line in f2.readlines():
        cols = line.split()
        bm25Data.setdefault(cols[0], [])
        bm25Data[cols[0]].append(cols[2])
    f2.close()

    f3 = open("ql.trecrun", 'r')
    for line in f3.readlines():
        cols = line.split()
        qlData.setdefault(cols[0], [])
        qlData[cols[0]].append(cols[2])
    f3.close()

    f4 = open("sdm.trecrun", 'r')
    for line in f4.readlines():
        cols = line.split()
        sdmData.setdefault(cols[0], [])
        sdmData[cols[0]].append(cols[2])
    f4.close()

    tempData = {}
    temp = None
    f5 = open("stress.trecrun", 'r')
    for line in f5.readlines():
        cols = line.split()           
        if len(cols) == 6:
            if temp == None:
                temp = cols[0]
                tempData[cols[2]] = int(cols[3])
            elif temp != cols[0]:
                i = 0
                while i < len(tempData):
                    key = min(tempData, key=tempData.get)
                    stressData.setdefault(temp, [])
                    stressData[temp].append(key)
                    tempData.pop(key)
                    i += 1
                temp = cols[0]
            else:
                tempData[cols[2]] = int(cols[3])
    f5.close()

    models = ["bm25.trecrun", "ql.trecrun", "sdm.trecrun", "stress.trecrun"]

    f6 = open("output.metrics", 'w')
    measure = None
    for model in models:
        if model == "bm25.trecrun":
            measure = bm25Data
        elif model == "ql.trecrun":
            measure = qlData
        elif model == "sdm.trecrun":
            measure = sdmData
        else:
            measure = stressData

        accum1 = 0
        for query in measure:
            accum1 += NDCG(100, relevance[query], measure[query])
        f6.write(model + ' NDCG@100 ' + str(accum1 / len(measure)) + '\n')

        accum2 = 0
        for query in measure:
            accum2 += MRR(relevance[query], measure[query])
        f6.write(model + ' MRR ' + str(accum2 / len(measure)) + '\n')

        accum3 = 0
        for query in measure:
            accum3 += precision(10, relevance[query], measure[query])
        f6.write(model + ' P@10 ' + str(accum3 / len(measure)) + '\n')

        accum4 = 0
        for query in measure:
            accum4 += recall(15, relevance[query], measure[query])
        f6.write(model + ' Recall@15 ' + str(accum4 / len(measure)) + '\n')

        accum5 = 0
        for query in measure:
            accum5 += F1(20, relevance[query], measure[query])
        f6.write(model + ' F1@20 ' + str(accum5 / len(measure)) + '\n')

        accum6 = 0
        for query in measure:
            accum6 += MAP(relevance[query], measure[query])
        f6.write(model + ' MAP ' + str(accum6 / len(measure)) + '\n')

    f6.close()


if __name__ == '__main__':
    main()