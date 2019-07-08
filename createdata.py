import sys
import re
from urllib import unquote

def cleanRes(str):
    a = str.split("resource/")
    if len(a)<2:
        return ""
    name = a[1]
    name = name.split("(")[0]
    # decode url ISO encoding
    name = unquote(name).decode('utf-8')
    name = name.replace("\t","").replace("_"," ").replace(">","").strip()
    
    # replace %28%29 if any
    name = re.sub("\ \(.*?\)","",name)
    return name

def printIR(fullname, disamb):
    if (not fullname) or (not disamb):
        return
    lab="y"
    print (fullname+"\t"+fullname+"\t"+lab).encode('utf-8')
    exp = fullname.split()
    lname = exp[-1]
    # if fullname!=disamb:
    #     if lname!=disamb and exp[0]!=disamb:
    #         lab="n"
    print (fullname+"\t"+disamb+"\t"+lab).encode('utf-8')

def printIRLog(fullname, disamb):
    if (not fullname) or (not disamb):
        return
    lab="y"
    print >> sys.stderr, fullname+"\t"+fullname+"\t"+lab
    exp = fullname.split()
    lname = exp[-1]
    if fullname!=disamb:
        if lname!=disamb and exp[0]!=disamb:
            lab="n"
    print >> sys.stderr, fullname+"\t"+disamb+"\t"+lab

lineDict=dict()
# retrieve all disambiguation phrases (with xml http tags)
# sample key:
# new lineDict key:       <http://dbpedia.org/resource/Alien_%28band%29>
# new lineDict key:       <http://dbpedia.org/resource/The_Aliens>
# new lineDict key:       <http://dbpedia.org/resource/The_Aliens_%28Australian_band%29>
# sample values:
# <http://dbpedia.org/resource/Alien> <http://dbpedia.org/ontology/wikiPageDisambiguates> <http://dbpedia.org/resource/Alien_%28law%29> .
# <http://dbpedia.org/resource/Alien> <http://dbpedia.org/ontology/wikiPageDisambiguates> <http://dbpedia.org/resource/Alien_%28franchise%29> .
# <http://dbpedia.org/resource/Alien> <http://dbpedia.org/ontology/wikiPageDisambiguates> <http://dbpedia.org/resource/Alien_%28film%29> .
maxCount=0
maxKey=''
for line in open('disambiguations_en.nt'):
    line = line.strip()
    l = line.split(" ")
    if len(l)>=3:
        # raw_input(line)
        if l[2] in lineDict:
            lineDict[l[2]].append(line)
            if len(lineDict[l[2]]) > maxCount:
                maxCount=len(lineDict[l[2]])
                maxKey=l[2]
        else:
            lineDict[l[2]]=[line]
print >> sys.stderr, ("max key:\t"+maxKey+"\tmaxCount:"+str(maxCount))
uniquePersonNames = set()
# retrieve all person phrases in a set
# sample person phrase key: 
# <http://dbpedia.org/resource/Aristotle>
# <http://dbpedia.org/resource/Aristotle>
# <http://dbpedia.org/resource/Abraham_Lincoln>
# <http://dbpedia.org/resource/Abraham_Lincoln>
for line in open('persondata_en.nt'):
    line = line.strip()
    key = line.split()[0]
    uniquePersonNames.add(key)
# retrieve if a person name has ambiguous representation
print "sep=\t"
print "name1\tname2\tissame"
for key in uniquePersonNames:
    if key in lineDict:
        candList = lineDict[key]
        for cand in candList:
            arr=cand.split()
            printIR(cleanRes(arr[2]),cleanRes(arr[0]))

for line in open('DBLP10k.csv'):
    l = line.strip().split(';')
    lab="n"
    if l[0]=="t" or l[1]=="t":
        lab="y"
    print l[2]+"\t"+l[3]+"\t"+lab
