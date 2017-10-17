# -*- coding: utf-8 -*-
import json
import sys
from itertools import chain
from collections import defaultdict
from bs4 import BeautifulSoup

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False    

def isStopword(tmp,stopwords):
    for j in range (0,len(stopwords)):
        if(tmp.lower() == stopwords[j].lower()):
            return True
            break 
    return False


def tokenize(s,id) : 
    tokens=[]
    stopwords = [ "Reuters","a" , "an" , "and" , "are", "as", 
              "at" , "be" ,"by" , "for", "from",
              "has" , "he", "in" , "is" , "it", 
              "its" , "of" , "on" , "that" , "the",
              "to" , "was" , "were", "will", "with"]   
    delimiter =  ' '   

    characters = ["\t" ,"\n", "\r", "+", "/", ".",",","?", "!", "(" , ")" , "[" , "]" , "\\" ]
    for char in characters :
        s = s.replace(char, " ")
    
    #s = s.replace("\t", " ").replace("\n", " ").replace("\r", " ").replace("+", " ").replace("/", " ").replace(".", " ").replace(",", " ").replace("?", " ").replace("!", " ")        
           
    # calculate number of delimiter characters
    n = 0
    for i in range (0,len(s)):
        if (s[i] == delimiter):
            n+=1              
    right = 0 
    left = 0
    for i in range (0,n):
        while (s[right] != delimiter):
            right += 1
        tmp = s[left: right] 
        tmp = tmp.strip('.,?!()[];:').lower()
        valid = True 
        if (tmp.strip()!= "" and is_number(tmp[0])==False and not isStopword(tmp,stopwords)) :
            tokens.append([tmp,id])
        right+=1
        left = right   
    tmp = s[right:len(s)] 
    tmp = tmp.strip('.,?!()[];:').lower()    
    if (tmp.strip()!="" and is_number(tmp[0])==False and not isStopword(tmp,stopwords) ):
        tokens.append([tmp,id])
    return tokens

def sortDictionary(dictionary):
    sorteddict = {}
    for key in sorted(dictionary):
        sorteddict[key] = dictionary[key] 
    return sorteddict

def addToList(postings_list,docid):
    if docid not in postings_list :
        return postings_list.insert(0,docid) 
    else :
        return postings_list   

def saveObject(dictionary,fileName):
    with open(fileName, 'w') as file:
        file.write(json.dumps(dictionary,sort_keys=True))   
    print("File : " + fileName + " saved! ")

def mergeDicts(dict1,dict2):
    dict3 = defaultdict(list)
    for k, v in chain(dict1.items(),dict2.items()):
        dict3[k].extend(v)
    return dict3

def SPIMI(tokens,blockSizeLimit):
    print("Runing SPIMI")
    #print(len(tokens))  
    fileCounter = 0    
    dictionary= {} 
    initLenth = len(tokens)
    postingCount = 0
    dictionaryCount = 0
    while(len(tokens)>0):
        while (sys.getsizeof(dictionary)/1024) <= blockSizeLimit : 
            sys.stdout.write("\rIndexing data %i" % (100-(len(tokens)*100/initLenth)))
            sys.stdout.flush()             
            #if((len(tokens)%10000) == 0):
            #    print("memory : " + str(sys.getsizeof(dictionary)/1024) + " " + str(len(tokens))) 
            if(len(tokens)==0) : break      
            token = tokens.pop(0)
            #print(token[0])
            if token[0] not in dictionary : 
                postings_list = [] 
                dictionary[token[0]] = postings_list
                dictionaryCount = dictionaryCount + 1
            else :
                postings_list = dictionary[token[0]]
            length = len(postings_list)
            addToList(postings_list,token[1])
            if(length != len(postings_list)): 
                postingCount = postingCount + 1
        saveObject(dictionary,"Minidict" +str(fileCounter)+ ".json" )
        fileCounter = fileCounter+1
        dictionary = {}
        print("Postings Count : "+ str(postingCount))
        print("Term Count : "+ str(dictionaryCount))
    return fileCounter

#merge blocks
def mergeFiles(fileCount):
    with open("FinalDictionary.json", 'w') as final:         
        final.write("{}")   
    for i in range(0,fileCount):
        print(i)  
        with open("Minidict"+str(i)+".json") as file1:
            data1 = json.load(file1)  
        with open("FinalDictionary.json") as file2:
            data2 = json.load(file2)     
        data3 = mergeDicts(data1,data2)           
        with open("FinalDictionary.json", 'w') as final:         
            final.write(json.dumps(data3,sort_keys=True)) 
         

tokens = []

for z in range (0,22):
    ss = ""
    if z < 10: ss = "0"
    with open("./reuters21578/reut2-0"+ss+str(z)+".sgm") as fp:
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
        tokens.extend(tokenize(s,id))

    sys.stdout.write("\rTokenizing data %i" % ((z*100/22)))
    sys.stdout.flush()
        
        # #print(dictionary)

            #print(value)
        #print(sys.getsizeof(dictionary)/1024/1024)     
        #if (sys.getsizeof(dictionary)/1024) >= blockSizeLimit :
        #print('123')    
        #break
        #
        #print(len(tokens))
        # # parse n+1 tokens and store in an array
        # for token in tokens: 
        #     #print(str(i) + ':' + token)
        #     # print(sys.getsizeof(dictionary)/1024)
sys.stdout.write("\rTokenizing data 100")
sys.stdout.flush()
print("\nTokenizing Done")
print("Token Count " + str(len(tokens)))
fileCount = SPIMI(tokens,2000)
mergeFiles(fileCount)

         


           
    
# with open("Minidict1.json") as file2:
#     data2 = json.load(file2)   
# data3 = mergeDicts(data1,data2)   
# with open("FinalDictionary.json", 'w') as final:         
#     final.write(json.dumps(data3,sort_keys=True))   

#for key in sorted(dictionary):
#    print(key, dictionary[key] ) 

# 
# print(sys.getsizeof(tokens))
# if (sys.getsizeof(blockContent)/1024/1024) >= blockSizeLimit :
#     print('123')

#  output file ← NewFile()
#  dictionary ← NewHash()
#  while (free memory available)
#  do token ← next(token stream)
#  if term(token) ∈/ dictionary
#  then postings list ← AddToDictionary(dictionary,term(token))
#  else postings list ← GetPostingsList(dictionary,term(token))
#  if full(postings list)
#  then postings list ← DoublePostingsList(dictionary,term(token))
#  AddToPostingsList(postings list,docID(token))
#  sorted terms ← SortTerms(dictionary)
#  WriteBlockToDisk(

    #         n++;
    #         String[] tokens = new String[n+1];

    # parse n+1 tokens and store in an array
    # int right = 0, left = 0;
    # for (int i = 0; i < n; i++) {
    #     while (s.charAt(right) != delimiter)
    #         right++;
    #     tokens[i] = s.substring(left, right);
    #     right++;
    #     left = right;
    # }
    # tokens[n] = s.substring(right, s.length());

    # // print results for testing
    # for (int i = 0; i < tokens.length; i++)
    #     StdOut.println(i + ": " + tokens[i]);
    