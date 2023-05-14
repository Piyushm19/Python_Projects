import gzip
import json
import matplotlib as plt


def write(scenes, name, ):
    f = open(name, "w")
    for scene in scenes:
            f.write(scene + '\n')
    f.close()

# this is where is indexing is done
def indexing(C, invLists, docLens):
    index = 0
    docId = 0
    scenes = []
    plays = []
    nums = []
    accumPlays = {}
    while (index < len(C)):
        docId = docId + 1
        d = C[index]
        scenes.append(d["sceneId"])
        plays.append(d["playId"])
        nums.append(d["sceneNum"])
        tokens = d["text"].split()
        if (accumPlays.get(d["playId"], -1) == -1):
            accumPlays[d["playId"]] = len(tokens)
        else:
            accumPlays[d["playId"]] += len(tokens)
        docLens.append(len(tokens))
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
    return [invLists, scenes, plays, nums, accumPlays, docLens]


def compare(pL, arr, names, n):
    scenes = set({})
    dict1 = {}
    dict2 = {}
    sceneNum = []
    for term in arr:
        if (term == arr[0]):
            dict1 = frequency(pL, term)
        if (term == arr[-1]):
            dict2 = frequency(pL, term)
        else:
            tempDict = frequency(pL, term)
            for key in list(tempDict.keys()):
                if (dict1.get(key, -1) == -1):
                    dict1[key] = [0, tempDict[key][0]]
                else:
                    dict1[key].append(tempDict[key][0])
            for key in list(dict1.keys()):
                if len(dict1[key]) == 1:
                    dict1[key].append(0)
    keys1 = list(dict1.keys())
    keys2 = list(dict2.keys())
    th = []
    y = []
    allKeys = list(set(keys1 + keys2))
    for key in allKeys:
        if (dict1.get(key, -1) != -1 and dict2.get(key, -1) == -1):
            scenes.add(names[key - 1])
            th.append(max(dict1[key]))
            y.append(0)
            sceneNum.append(n[key - 1])
        elif (dict1.get(key, -1) != -1 and dict2.get(key, -1) != -1):
            if (max(dict1[key]) > dict2[key][0]):
                scenes.add(names[key - 1])
                th.append(max(dict1[key]))
                y.append(0)
                sceneNum.append(n[key - 1])
        elif (dict1.get(key, -1) == -1):
            th.append(0)
            y.append(dict2[key][0])
            sceneNum.append(n[key - 1])
        else:
            pass
    return [scenes, th, y, sceneNum]


def findTerm(pL, arr, names): 
    scenes = set({})
    for term in arr:
        for d in pL[term]:
            docId = list(d.keys())[0]
            scenes.add(names[docId - 1])
    return scenes


def findPhrase(pL, arr, names):
    l = []
    for i in arr:
        l.append(pL[i])
    L = intersect(l)
    scenes = set({})
    for i in L:
        docId = list(i[0].keys())[0]
        if matching(i, 1):
            scenes.add(names[docId - 1])
    return scenes

# Helper functions

def frequency(pL, word): 
    freq = {}
    for d in pL[word]:
        docId = list(d.keys())[0]
        freq[docId] = [len(d[docId])]
    return freq


def intersect(arr):
    match = []
    newList = []
    index = 0
    while (index < min(len(l) for l in arr)):
        candidate = max(list(l[index].keys())[0] for l in arr)
        curPost = allMatch(arr, candidate)
        if None not in curPost:
            for i in curPost:
                match.append(i)
            newList.append(match)
        match = []
        index = index + 1
    return newList


def allMatch(L, cand):
    temp = []
    for l in L:
        app = False
        for d in l:
            docId = list(d.keys())[0]
            if (docId == cand):
                temp.append(d)
                app = True
                break
            elif (docId > cand):
                temp.append(None)
                break
            elif (d == l[-1] and app == False):
                temp.append(None)
                break
            else:
                continue
    return temp


def matching(L, dist):
    p0 = L[0][list(L[0].keys())[0]]
    rest = L[:]
    rest.pop(0)
    temp = []
    for prev in p0:
        for post in rest:
            p = post[list(post.keys())[0]]
            found = False
            for cur in p:
                if (prev < cur and cur <= (prev + dist)):
                    found = True
                    temp.append(found)
                    prev = cur
                    break
    if len(rest) == len(temp):
        return True
    else:
        return False


def main():
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
    plays = data[2]
    nums = data[3]
    playLens = data[4]
    docLens = data[5]
    average = sum(docLens) / len(docLens)
    print(float(average))
    print(scenes[docLens.index(max(docLens))]) # longest scene length
    print(scenes[docLens.index(min(docLens))]) # shortest scene length
    print(max(playLens, key = playLens.get))   # longest play 
    print(min(playLens, key = playLens.get))   # shortest play
    save, maxTh, you, numScenes = compare(invIndex, ['thee', 'thou', 'you'], scenes, nums)
    write(sorted(save), 'terms0.txt')
    write(sorted(findTerm(invIndex, ['venice', 'rome', 'denmark'], scenes)), 'terms1.txt')
    write(sorted(findTerm(invIndex, ['goneril'], plays)), 'terms2.txt')
    write(sorted(findTerm(invIndex, ['soldier'], plays)), 'terms3.txt')
    write(sorted(findPhrase(invIndex, ['poor', 'yorick'], scenes)), 'phrase0.txt')
    write(sorted(findPhrase(invIndex, ['wherefore', 'art', 'thou', 'romeo'], scenes)), 'phrase1.txt')
    write(sorted(findPhrase(invIndex, ['let', 'slip'], scenes)), 'phrase2.txt')



if __name__ == '__main__':
    main()    # calls main function