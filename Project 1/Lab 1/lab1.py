# -*- coding: utf-8 -*-
import json
import sys
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

def tokenize(s,id) : 
    tokens=[]
    stopwords = [ "Reuters","a" , "an" , "and" , "are", "as", 
              "at" , "be" ,"by" , "for", "from",
              "has" , "he", "in" , "is" , "it", 
              "its" , "of" , "on" , "that" , "the",
              "to" , "was" , "were", "will", "with"]     
    delimiter =  ' '              
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
        tmp = tmp.strip('.,?!').lower()
        valid = True 
        if (tmp.strip()!="" and is_number(tmp[0])==False) :
            for j in range (0,len(stopwords)):
                if(tmp.lower() == stopwords[j].lower()):
                    valid = False
                    break 
        else : 
            valid = False         
        
        if(valid == True):
            tokens.append([tmp,id])
        right+=1
        left = right      
    for j in range (0,len(stopwords)):
        if(s[right:len(s)].lower() != stopwords[j].lower()):
            tokens.append([s[right:len(s)],id])
            break
    return tokens

def sortDictionary(dictionary):
    sorteddict = {}
    for key in sorted(dictionary):
        sorteddict[key] = dictionary[key] 
    return sorteddict

def addToList(list,docid):
    if docid not in postings_list :
        return list.insert(0,docid) 
    else :
        return list   

def saveObject(dictionary,fileName):
    with open(fileName, 'w') as file:
        file.write(json.dumps(dictionary))   
    print("File : " + fileName + " saved! ")
         

dictionary= {}
tokens = []
fileCounter = 0

for z in range (0,6):
    ss = ""
    if z < 10: ss = "0"
    # print("/Users/mouadbouras/Desktop/SOEN 479/reuters21578/reut2-0"+ss+str(z)+".sgm")
    with open("/Users/mouadbouras/Desktop/SOEN 479/reuters21578/reut2-0"+ss+str(z)+".sgm") as fp:
        data = fp.read()    
        data = data[:35] + "<ROOT>" + data[35:] + "</ROOT>"

    soup = BeautifulSoup(data, "xml")
    #strip(' \t\n\r') #"/this is/a test of the/class// and/all//last"


    #print(soup.TITLE.string)

    #id = soup.REUTERS["NEWID"]
    #s =  soup.BODY.string.strip()
    #s = s.replace("\t", " ").replace("\n", " ").replace("\r", " ") 
    #print("Id : " + id)
    ids = soup.find_all('REUTERS')
    bodys =  soup.find_all('BODY')

    for j in range (0 , len(bodys)):
        id = ids[j]["NEWID"]
        body = bodys[j]
        s = body.string.strip()
        s = s.replace("\t", " ").replace("\n", " ").replace("\r", " ").replace("+", " ").replace("/", " ").replace(".", " ").replace(",", " ").replace("?", " ").replace("!", " ")        
        tokens.extend(tokenize(s,id))

    sys.stdout.write("\rTokenizing data %i" % ((z*100/12)))
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

blockSizeLimit = 1000    
print("\nTokenizing Done")
print("Runing SPIMI")
#print(len(tokens))   
while(len(tokens)>0):
    while (sys.getsizeof(dictionary)/512) <= blockSizeLimit :  
        #if((len(tokens)%10000) == 0):
        #    print("memory : " + str(sys.getsizeof(dictionary)/1024) + " " + str(len(tokens))) 
        if(len(tokens)==0) : break      
        token = tokens.pop(0)
        #print(token[0])
        if token[0] not in dictionary : 
            postings_list = [] 
            dictionary[token[0]] = postings_list
        else :
            postings_list = dictionary[token[0]]
        addToList(postings_list,token[1])
    saveObject(sortDictionary(dictionary),"Minidict" +str(fileCounter)+ ".json" )
    fileCounter = fileCounter+1
    dictionary = {}


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
    