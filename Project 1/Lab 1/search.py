# -*- coding: utf-8 -*-
import json
import sys

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


while True :
    search = raw_input("Please enter search query: ")
    print "you entered", search

    tmpList = search.strip().lower().split(" or ")
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
            if(term.strip() != "") and (term.strip().lower() in dictionary) : 
                postings.append(dictionary[term])
            queryResult.extend(postings)                  
        searchResult.append(combineLists(queryResult))
    
    result = uniqueList(searchResult)
    print("")        
    print("result")
    
    print(result)
    print("count : " + str(len(result) ))
#    print(uniqueList(searchResult)) 


        
#     print("result : ")
#     print(searchResult)

            

            

    # with open("FinalDictionary.json") as f:
    #     dictionary = json.load(f)  

    # if(search.strip() != "") and (search.strip().lower() in dictionary) : 
    #     print(dictionary[search]) 
    # else : 
    #     print("nothing Found!")