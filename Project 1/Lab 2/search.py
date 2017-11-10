# -*- coding: utf-8 -*-
import json
import sys
from collections import defaultdict
from bm25 import okapi_score
from bs4 import BeautifulSoup

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

def mergeLists(list1,list2): 
    result = []
    i1 = 0
    i2 = 0 
    #print("list 1 : " + str(len(list1)) + " list 2 : " + str(len(list2) ))
    #print(int(list1[0])+int(list2[0]))
    while i1 < len(list1) and i2 < len(list2) :         
        if int(list1[i1]) == int(list2[i2]) : 
            result.append(list1[i1])
            i1 = i1+1
            i2 = i2+1
        elif int(list1[i1]) > int(list2[i2]) :
            i1 = i1+1
        else :
            i2 = i2+1 
    return result

def combineLists(lists):
    if(len(lists)==0) :
        return []
    else : 
        mergedList = lists[0]
        for list in lists : 
            mergedList = mergeLists(mergedList,list)
        return mergedList

def uniqueList(lists):
    mergedList = []
    for list in lists : 
        mergedList.extend(list)            
    return set(mergedList)

print(combineLists([[],[1,2,3,4]]))

while True :
    search = input("Please enter search query: ")
    print ("you entered", search)

    tmpList = search.strip().lower().split(" | ")
    searchList = []    
    for query in tmpList:
        searchList.append(query.split(" "))
            
    print(searchList)

    with open("FinalDictionary.json") as f:
        dictionary = json.load(f)  

    searchResult = []
    for query in searchList:
        queryResult = []
        for term in query:
            postings = []
            if(term.strip() != "") and (term.strip() in dictionary) : 
                postings.append(dictionary[term])
            queryResult.extend(postings)                  
        searchResult.append(combineLists(queryResult))
    
    result = uniqueList(searchResult)
    print("")        
    print("result")
    
    print(result)
    print("count : " + str(len(result) ))
#    print(uniqueList(searchResult)) 

    D = docs()
    print ("Calculating Okapi/BM25 Scores")
    scores = defaultdict(list)
    for term in searchList[0]:
        for docId in result:
            scores[docId].append(okapi_score(term, result, docId, len(D)))
    
    finalScores = {}
    for key in scores.keys():
        finalScores[key] = sum(scores[key])
    print ("DocId		Score")
    print ("----------------------------------------------------")
    for i in sorted(finalScores, key=finalScores.get, reverse=True):
        print (str(i) + "		" + str(finalScores[i]))
    
    print ("----------------------------------------------------")

        
#     print("result : ")
#     print(searchResult)

            

            

    # with open("FinalDictionary.json") as f:
    #     dictionary = json.load(f)  

    # if(search.strip() != "") and (search.strip().lower() in dictionary) : 
    #     print(dictionary[search]) 
    # else : 
    #     print("nothing Found!")