from __future__ import division
import re
from math import log
from collections import Counter
#import reuters #for testing
from collections import defaultdict
from bs4 import BeautifulSoup
import json
import sys

def docs ():
    d = {}
    for z in range (0,22):
        ss = ""
        if z < 10: ss = "0"
        with open("../reuters21578/reut2-0"+ss+str(z)+".sgm") as fp:
            data = fp.read()    
            data = data[:35] + "<ROOT>" + data[35:] + "</ROOT>"
        soup = BeautifulSoup(data, "xml")

        reuters = soup.find_all('REUTERS')

        for j in range (0 , len(reuters)):
            id = int(reuters[j]["NEWID"])
            # print(reuters[j].BODY)
            if not reuters[j].BODY : continue  
            title =  reuters[j].TITLE                 
            body = reuters[j].BODY
            # print(body.string)
            s = title.string.strip()
            s += " " + body.string.strip()
            d[id] = s
    return d
#reutersFunctions = reuters.ReutersCorpus(); #for testing
#documents = reutersFunctions.getDocuments(); #for testing

k = 1.5
b = 0.75

#documents = docs()
#N = len(documents)

#return the bm25 score
#q = query term 
#p = postings list of querry term
#D = document id
#k,b = constants
#N = total documents in collection
#dl = document length in words
#avdl = average document length
def okapi_score(q, p, D,N):
    first = idf(p, N)
    second = termFreq(q, documents[D]) * (k+1)
    third = termFreq(q, documents[D]) + k * (1 - b + b * (float(format(dl(documents[D]), '.10f')) / float(avdl(documents[D], N))))
    return first * (second / third)


#return the frequency of term q in document D
def termFreq(q, D):
    doc = re.findall(r"[\w]+", D)
    count = 0
    for d in doc:
        if d.lower() == q:
            count += 1
    return count

#print (termFreq("simple", documents[1623])) #for testing should return 1

def idf(p, N):
    #p = length of postings list for querry term
    return log( (N - len(p) + 0.5) / (len(p) + 0.5) )

def dl(D):
    doc = D.split(' ')
    count = 0
    for d in doc:
        count += 1
    return count  

def avdl(D, t):
    return format((dl(D) / t), '.10f')



def main() :
    #q = query term 
    #p = postings list of querry term
    #D = document id
    #k,b = constants
    #N = total documents in collection
    #dl = document length in words
    #avdl = average document length
    
    q1 = "drug"
    p1 = { 3589, 3091, 19479, 14359, 16413, 3106, 2594, 3108, 6693, 17959, 2093, 9774, 9262, 
           11313, 21051, 19006, 14401, 7753, 1097, 2636, 21069, 5711, 3151, 17489, 2127, 15955, 
           15445, 8789, 17495, 7260, 16994, 3682, 12903, 3176, 17514, 10858, 4715, 8813, 17520, 
           9331, 17526, 2679, 2168, 16508, 19580, 9342, 3205, 18059, 8333, 2713, 3739, 16032, 
           6304, 12962, 6309, 12968, 13993, 11434, 1705, 3756, 15537, 13489, 2226, 17588, 19640, 
           696, 1212, 15040, 8384, 3776, 192, 17604, 5319, 730, 13021, 19678, 2271, 3297, 6378,
           19691, 15088, 1269, 21239, 3328, 2305, 7940, 11525, 4871, 19720, 13576, 13068, 8461, 
           4877, 1805, 17680, 18196, 19736, 13080, 17690, 1819, 18716, 17692, 7454, 11553, 10026, 
           16692, 4917, 2868, 2356, 4408, 10554, 826, 11585, 321, 9542, 9546, 21325, 4435, 14165, 
           15703, 5466, 16219, 19292, 11613, 21348, 18792, 9579, 15213, 5486, 1391, 9585, 6514, 
           375, 18808, 9085, 16259, 4485, 902, 18318, 6031, 6544, 8594, 1432, 15257, 6553, 20892, 
           9633, 15269, 19885, 1467, 16829, 13764, 6089, 457, 1998, 6608, 12242, 7125, 15318, 6614,
           20953, 2523, 10206, 21481, 18923, 19437, 2036, 3577, 7163}
    #q2 = "company"
    #q3 = "bankruptcies"
    N = len(documents)
    
    #for p in p1 : 
    #    print( "Doc : " + str(p) + " | " + str(okapi_score(q1, p1, p, N)))
    #D=902
    #first = idf(p1, N)
    #print("f" + str(first))

    # second = termFreq(q1, documents[D]) * (k+1)
    # print("s" + str(second) + " tf " + str(termFreq(q1,documents[D])))

    # doc = re.findall(r"[\w]+", documents[D])
    # print(doc)
    # count = 0
    # for d in doc:
    #     if d.lower() == q1.lower():
    #         count += 1
    # print(count)

    #third = termFreq(q1, documents[D]) + k * (1 - b + b * (float(format(dl(documents[D]), '.10f')) / float(avdl(documents[D], N))))
    #print("t" + str(third))


# print(len(documents))
# main()
# print("done")


