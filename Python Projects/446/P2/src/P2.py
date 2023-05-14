import gzip
import sys
def mainFunc(l, t):
    # This is where I begin the pagerank algorithm
    def pageRank(file, l, t):
        line = file.readline()
        line = line.decode('utf-8')
        pages = {}
        while (line != ''):
            arr = line.split('\t')
            source = arr[0]
            target = arr[1]
            target.strip('\n')
            if pages.get(target, -1) == -1:
                    pages.update({target : []})
            if pages.get(source, -1) == -1:
                    pages.update({source : [target]})
            else:
                pages[source].append(target)
            line = file.readline()
            line = line.decode('utf-8')
        I = {}
        for entries in pages:
            I.update({entries: 1/len(pages)})
        R = I.copy()
        doesConverage = False
        while(doesConverage == False):
            accumulator = 0
            for entry in R:
                R.update({entry : l / len(pages)})
            for page in pages:
                Q = pages[page]
                if (len(Q) > 0):
                    for pageQ in Q:
                        R[pageQ] += (1 - l) * I[page] / len(Q)
                else:
                    accumulator += (1 - l) * I[page] / len(pages)
            for entry in R:
                R[entry] += accumulator
            summation = 0
            for entry in R:
                summation += abs(R[entry] - I[entry])
            if summation < t:
                doesConverage = True
            I = R.copy()
        return R

    def keyWithMaxVal(d):
        v=list(d.values())
        k=list(d.keys())
        return k[v.index(max(v))]

    inlinks = {}
    pageranks = {}

    with gzip.open('links.srt.gz','r') as file1:
        line = file1.readline()
        line = line.decode('utf-8')
        while (line != ''):
            pages = line.strip('\n').split('\t')
            target = pages[1]
            if inlinks.get(target, -1) == -1:
                inlinks.update({target : 1})
            else:
                inlinks[target] = inlinks[target] + 1
            line = file1.readline()
            line = line.decode('utf-8')    
    file1.close()

    with gzip.open('links.srt.gz','r') as file1:
        pageranks = pageRank(file1, l, t)
    file1.close()

    inlinksHundred = {}
    pagerankHundred = {}
    inlinksOrder = []
    pageranksOrder = []
    
    for num in range(100):
        maxInlink = keyWithMaxVal(inlinks)
        maxPagerank = keyWithMaxVal(pageranks)
        inlinksHundred.update({maxInlink: inlinks[maxInlink]})
        pagerankHundred.update({maxPagerank: pageranks[maxPagerank]})
        inlinksOrder.append(maxInlink)
        pageranksOrder.append(maxPagerank)
        inlinks.pop(maxInlink)
        pageranks.pop(maxPagerank)

    file2 = open("inlinks.txt", "w")
    file3 = open("pagerank.txt", "w")
    for num in range(100):
        file2.write(inlinksOrder[num] + ' ' + str(num + 1) + ' ' + str(inlinksHundred[inlinksOrder[num]]) + '\n')
        file3.write(str(pageranksOrder[num].strip('\n')) + ' ' + str(num + 1) + ' ' + str(pagerankHundred[pageranksOrder[num]]) + '\n')
    file2.close()
    file3.close()
        
if __name__ == '__main__':
    l = float(sys.argv[1])
    t = float(sys.argv[2])
    mainFunc(l, t)

