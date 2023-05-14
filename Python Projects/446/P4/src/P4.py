import gzip
import json
import math
import queue


def BM25(tf, dtf, qtf, numDocs, dl, avg, k1, k2, b):
    K = k1 * ((1-b) + b * (float(dl)/float(avg)))
    return (math.log( 1 / ((dtf + 0.5) / (numDocs - dtf + 0.5)))) * (((k1 + 1) * tf) / ((k1 * ((1-b) + b * (float(dl)/float(avg)))) + tf)) * (((k2+1) * qtf) / (k2 + qtf))


def QL(tf, ctf, totalTerms, dl, mu):
    preLog = (tf + (mu * (ctf / totalTerms))) / (dl + mu)
    return math.log(abs(preLog))


def retrieval(model, query, invIndex, scenes, avg, docLens, numDocs, totalTerms, constants):
    L = []
    R = queue.PriorityQueue()
    docs = set({})
    for q in query:
        if invIndex[q] not in L:
            L.append(invIndex[q])
            for p in invIndex[q]:
                docs.add(list(p.keys())[0])
    docs = list(docs)
    docs = sorted(docs)
    for index in range(len(docs)):
        dl = docLens[docs[index] - 1]
        curScore = 0.0
        curTerm = 0
        for pL in L:
            tf = 0
            dtf = 0
            ctf = 0
            for p in pL:
                dtf += 1
                ctf += len(p[list(p.keys())[0]])
                if list(p.keys())[0] == docs[index]:
                    tf = len(p[list(p.keys())[0]])
            qtf = query.count(query[curTerm])
            curTerm += 1
            if model == 0:
                curScore += BM25(tf, dtf, qtf, numDocs, dl, avg, constants[0], constants[1], constants[2])
            else:
                curScore += qtf * QL(tf, ctf, totalTerms, dl, constants[3])
        R.put((-1 * curScore, scenes[docs[index] - 1]))
    return R

# Indexing code
def indexing(C, invLists, docLens):
    index = 0
    docId = 0
    totalWords = 0
    scenes = []
    while (index < len(C)):
        docId = docId + 1
        d = C[index]
        scenes.append(d["sceneId"])
        tokens = d["text"].split()
        docLens.append(len(tokens))
        totalWords += len(tokens)
        position = 0
        while (position < len(tokens) - 1):
            position = position + 1
            token = tokens[position]
            invLists.setdefault(token, []) 
            postList = invLists[token] 
            if len(postList) == 0:
                postList.append({docId : [position]})
            elif list(postList[-1].keys())[0] != docId:
                postList.append({docId : [position]})
            else:
                postList[-1][docId].append(position)
        index = index + 1
    return [invLists, scenes, docLens, totalWords, len(C)]


def main():
    constants = [1.8, 5, 0.75, 250]
    invIndex = {}
    data = []
    docLens = []
    with gzip.open('shakespeare-scenes.json.gz','r') as f:
        C = json.load(f)
        collection = C['corpus']
        data = indexing(collection, invIndex, docLens)
    f.close()
    invIndex = data[0]
    scenes = data[1]
    docLens = data[2]
    totalTerms = data[3]
    numDocs = data[4]
    avg = sum(docLens) / len(docLens)
    Q1 = retrieval(0, ['the', 'king', 'queen', 'royalty'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    Q2 = retrieval(0, ['servant', 'guard', 'soldier'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    Q3 = retrieval(0, ['hope', 'dream', 'sleep'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    Q4 = retrieval(0, ['ghost', 'spirit'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    Q5 = retrieval(0, ['fool', 'jester', 'player'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    Q6 = retrieval(0, ['to', 'be', 'or', 'not', 'to', 'be'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    write(Q1, Q2, Q3, Q4, Q5, Q6, 'bm25.trecrun', 'bm25')
    Q1 = retrieval(1, ['the', 'king', 'queen', 'royalty'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    Q2 = retrieval(1, ['servant', 'guard', 'soldier'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    Q3 = retrieval(1, ['hope', 'dream', 'sleep'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    Q4 = retrieval(1, ['ghost', 'spirit'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    Q5 = retrieval(1, ['fool', 'jester', 'player'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    Q6 = retrieval(1, ['to', 'be', 'or', 'not', 'to', 'be'], invIndex, scenes, avg, docLens, numDocs, totalTerms, constants)
    write(Q1, Q2, Q3, Q4, Q5, Q6, 'ql.trecrun', 'ql')


def write(Q1, Q2, Q3, Q4, Q5, Q6, fileName, identity):
    f = open(fileName, "w")
    num1 = 1
    while not Q1.empty():
        tup = Q1.get()
        f.write('Q1' + ' skip ' + str(tup[1]) + '    ' + str(num1) + ' ' + str(tup[0] * -1) + ' pmakka-' + str(identity) + '\n')
        num1 += 1
    num2 = 1
    while not Q2.empty():
        tup = Q2.get()
        f.write('Q2' + ' skip ' + str(tup[1]) + '    ' + str(num2) + ' ' + str(tup[0] * -1) + ' pmakka-' + str(identity) + '\n')
        num2 += 1
    num3 = 1
    while not Q3.empty():
        tup = Q3.get()
        f.write('Q3' + ' skip ' + str(tup[1]) + '    ' + str(num3) + ' ' + str(tup[0] * -1) + ' pmakka-' + str(identity) + '\n')
        num3 += 1
    num4 = 1
    while not Q4.empty():
        tup = Q4.get()
        f.write('Q4' + ' skip ' + str(tup[1]) + '    ' + str(num4) + ' ' + str(tup[0] * -1) + ' pmakka-' + str(identity) + '\n')
        num4 += 1
    num5 = 1
    while not Q5.empty():
        tup = Q5.get()
        f.write('Q5' + ' skip ' + str(tup[1]) + '    ' + str(num5) + ' ' + str(tup[0] * -1) + ' pmakka-' + str(identity) + '\n')
        num5 += 1
    num6 = 1
    while not Q6.empty():
        tup = Q6.get()
        f.write('Q6' + ' skip ' + str(tup[1]) + '    ' + str(num6) + ' ' + str(tup[0] * -1) + ' pmakka-' + str(identity) + '\n')
        num6 += 1
    f.close()

if __name__ == '__main__':
    main()
