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

#Basic tokenization program
from bs4 import BeautifulSoup
with open("/Users/mouadbouras/Desktop/SOEN 479/reuters21578/reut2-000.sgm") as fp:
    soup = BeautifulSoup(fp, "xml")

id = soup.REUTERS["NEWID"]
s =  soup.BODY.string.strip()
s = s.replace("\t", " ").replace("\n", " ").replace("\r", " ") 
#strip(' \t\n\r') #"/this is/a test of the/class// and/all//last"

stopwords = [ "a" , "an" , "and" , "are", "as", 
              "at" , "be" ,"by" , "for", "from",
              "has" , "he", "in" , "is" , "it", 
              "its" , "of" , "on" , "that" , "the",
              "to" , "was" , "were", "will", "with"] 

#print(soup.TITLE.string)
print("Id : " + id)

delimiter =  ' '

# calculate number of delimiter characters
n = 0
for i in range (0,len(s)):
    if (s[i] == delimiter):
        n+=1

tokens = []
# parse n+1 tokens and store in an array

right = 0 
left = 0
for i in range (0,n):
    while (s[right] != delimiter):
        right += 1
    tmp = s[left: right] 
    tmp = tmp.strip('.,?!')
    valid = True 
    if (tmp.strip()!="" and is_number(tmp[0])==False) :
        for j in range (0,len(stopwords)):
            if(tmp == stopwords[j]):
                valid = False
                break 
    else : 
        valid = False         
    
    if(valid == True):
        tokens.append(tmp)
    right+=1
    left = right
    
        
tokens.append(s[right:len(s)])

# print results for testing
for i in range (0,len(tokens)):
    print(str(i) + ': ' + tokens[i])


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
    