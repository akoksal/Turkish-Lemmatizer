# -*- coding: utf-8 -*-
import re
import json
import pickle
import sys

#Pass parameter to identify which lexicon dataset to load
#Possible lexicons: wiktionary, zargan
#Returns dictionary with example format below:
#wordDict = {"word_1":["kok","word_2"], "word_2":["kok","word_2"], "dif_word_1":["kok","diff_word_1"]}
def loadWord(dataset):
    if dataset == "wiktionary":
        with open('Datasets/wiktionary.pkl','rb') as f:
            [wordList] = pickle.load(f)
        wordDict = {}
        for i in range(len(wordList)):
            word = wordList[i].replace("â","a")
            wordDict[findID(wordDict, word)] = ["kok",findID(wordDict, word)]
        return wordDict
    elif dataset == "zargan":
        with open('Datasets/zargan.pkl','rb') as f:
            zarganDict = pickle.load(f)
        wordDict = {}
        for word, valueList in zarganDict.items():
            word = word.replace("â","a")
            wordDict[findID(wordDict, word)] = ["kok",findID(wordDict, word)]
        return wordDict

#finds correct id for given word
#for example if there are 3 different word for "gul" and you want to add one more
#it returns gul_4 to differentiate different versions of words
def findID(wordDict, word):
    ct = 1
    while word+"_"+str(ct) in wordDict:
        ct = ct+1
    return word+"_"+str(ct)

#This function generates new word types based on ablouts on lemmas

#To generate negative words, we add -ma -me suffixes to verbs
#For example: gelmek -> gelmemek, gitmek -> gitmemek

#To handle softening of consonants, I generate softened version of each word
#For lemmas end with [p,ç,t,k] except verbs, the last consonant can be transformed into [b,c,d,[gğ]] based on the suffix it had
#g is possible only when word ends with nk.
#I generate all possible transformation and I check if softening matches in checkSuffixValidation
#For example: kitap -> kitab, küçük -> küçüğ(correct one), renk -> rengi

#To handle "becoming close(narrow) vowel", I have used explanation in TDK site.(http://www.tdk.gov.tr/index.php?option=com_content&view=article&id=194:Unlu-Daralmasi&catid=50:yazm-kurallar&Itemid=132)
#When verbs whose last wovel is "a" or "e" take "-yor" suffix, their last wovel transforms into "ı" or "i"
#Exception is for verb demek and yemek
#For example izlemek -> izli, dinlememek -> dinlemi

#Dropping a vowel
#In Turkish, when some words with two syllables take suffix starting with vowel, word's last vowel drops.
#List of these words are added to the code
#For example: alın -> aln, zehir -> zehri, oğul -> oğlu 

#Zero Infinitive
#In Turkish, verbs lexicon form, generally, is with to infinitive. This suffix is "-mak" or "-mek".
#For example, meaning of gelmek is "to come. However, we use root form of gelmek which is gel when we use verbs with different time forms. For example, present continuous form of gelmek is geliyor(without -mek part)
#Last action transforms verbs to the zero infinitive format
#For example: gelmek -> gel, almak -> al
def generate(wordDict, olay):
    newDict = {}
    if olay == "olumsuzluk eki":
        for kelime, valueList in wordDict.items():
            ind = kelime[kelime.index("_")+1:]
            kelime = kelime[:kelime.index("_")]
            if kelime.endswith("mak"):
                kelime = kelime[:-3]+"mamak"
                newDict[findID(wordDict, kelime)] =  ["olumsuzluk",kelime+"_"+ind]
            if kelime.endswith("mek"):
                kelime = kelime[:-3]+"memek"
                newDict[findID(wordDict, kelime)] =  ["olumsuzluk",kelime+"_"+ind]
    elif olay == "unsuz yumusamasi":
        for kelime, valueList in wordDict.items():
            ind = kelime[kelime.index("_")+1:]
            kelime = kelime[:kelime.index("_")]
            if not (kelime.endswith("mak") or kelime.endswith("mek")):
                if kelime.endswith("p"):
                    newDict[findID(wordDict, kelime[:-1]+"b")] = ["unsuz yumusamasi", kelime+"_"+ind]
                elif kelime.endswith("ç"):
                    newDict[findID(wordDict, kelime[:-1]+"c")] = ["unsuz yumusamasi", kelime+"_"+ind]
                elif kelime.endswith("t"):
                    newDict[findID(wordDict, kelime[:-1]+"d")] = ["unsuz yumusamasi", kelime+"_"+ind]
                elif kelime.endswith("k"):
                    if kelime.endswith("nk"):
                        newDict[findID(wordDict, kelime[:-1]+"g")] = ["unsuz yumusamasi", kelime+"_"+ind]
                    else:
                        newDict[findID(wordDict, kelime[:-1]+"ğ")] = ["unsuz yumusamasi", kelime+"_"+ind]
    elif olay == "unlu daralmasi":
         for kelime, valueList in wordDict.items():
            ind = kelime[kelime.index("_")+1:]
            kelime = kelime[:kelime.index("_")]
            if kelime == "demek":
                newDict[findID(wordDict, "di")] = ["unlu daralmasi", kelime+"_"+ind]
            elif kelime == "yemek":
                newDict[findID(wordDict, "yi")] = ["unlu daralmasi", kelime+"_"+ind]
            elif kelime.endswith("amak"):
                newDict[findID(wordDict, kelime[:-4]+"ı")] = ["unlu daralmasi", kelime+"_"+ind]
                newDict[findID(wordDict, kelime[:-4]+"u")] = ["unlu daralmasi", kelime+"_"+ind]
            elif kelime.endswith("emek"):
                newDict[findID(wordDict, kelime[:-4]+"i")] = ["unlu daralmasi", kelime+"_"+ind]
                newDict[findID(wordDict, kelime[:-4]+"ü")] = ["unlu daralmasi", kelime+"_"+ind]
    elif olay == "unlu dusmesi":
         for kelime, valueList in wordDict.items():
            ind = kelime[kelime.index("_")+1:]
            kelime = kelime[:kelime.index("_")]
            dusmeDict = {'akis': 'aks', 'akıl': 'akl', 'alın': 'aln','asıl': 'asl','asır': 'asr','atıf': 'atf', 'avuç': 'avc','azim': 'azm', 'ağız': 'ağz', 'bahis': 'bahs','bağır': 'bağr','beniz': 'benz','beyin': 'beyn','boyun': 'boyn','burun': 'burn','böğür': 'böğr','cebir': 'cebr','cezir': 'cezr','cisim': 'cism','devir': 'devr','emir': 'emr','fasıl': 'fasl','fecir': 'fecr','fesih': 'fesh','fetih': 'feth','fikir': 'fikr','geniz': 'genz','gönül': 'gönl','göğüs': 'göğs','hacim': 'hacm','haciz': 'hacz','hapis': 'haps','hatır': 'hatr','hayır': 'hayr','hazım': 'hazm','hüküm': 'hükm','hüzün': 'hüzn','hısım': 'hısm','hışım': 'hışm','isim': 'ism','izin': 'izn','kabir': 'kabr','kahır': 'kahr','karın': 'karn','kasır': 'kasr','kasıt': 'kast','kayıp': 'kayb','kayıt': 'kayd','kesir': 'kesr','keyif': 'keyf','keşif': 'keşf','kibir': 'kibr','koyun': 'koyn','kusur': 'kusr','kutup': 'kutp','küfür': 'küfr','kısım': 'kısm','metin': 'metn','misil': 'misl','mühür': 'mühr','nabız': 'nabz','nakil': 'nakl','nakit': 'nakt','nefis': 'nefs','nehir': 'nehr','nesil': 'nesl','nutuk': 'nutk','omuz': 'omz','oğul': 'oğl','rehin': 'rehn','resim': 'resm','ritim': 'ritm','sabır': 'sabr','seyir': 'seyr','tavır': 'tavr','ufuk': 'ufk','umur': 'umr','vakit': 'vakt','vakıf': 'vakf','vasıf': 'vasf','zikir': 'zikr','zulüm': 'zulm','ömür': 'ömr','özür': 'özr','şahıs': 'şahs','şehir': 'şehr','şekil': 'şekl','şükür': 'şükr', 'zehir':'zehr'}
            if kelime in dusmeDict:
                newDict[findID(wordDict,dusmeDict[kelime])] = ["unlu dusmesi", kelime+"_"+ind]
    elif olay == "fiil":
        for kelime, valueList in wordDict.items():
            ind = kelime[kelime.index("_")+1:]
            kelime = kelime[:kelime.index("_")]
            if kelime.endswith("mek") or kelime.endswith("mak"):
                newDict[findID(wordDict, kelime[:-3])] = ["fiil", kelime+"_"+ind]
    return newDict

#Appending two dictionary might have conflicts because there are same words with different meanings or features.
#If both dictionaries include "kelime_index", one of them changes to the "kelime_index+1"
def appendDict(revisedDict, newDict):
    for kelime, valueList in newDict.items():
        if kelime in revisedDict:
            revisedDict[findID(revisedDict, kelime[:kelime.index("_")])] = valueList
        else:
            revisedDict[kelime] = valueList
    return revisedDict	

dataset="zargan"
if(len(sys.argv)>1):
	dataset = sys.argv[1]

wordDict = loadWord(dataset)
wordDict = appendDict(wordDict, (generate(wordDict,"olumsuzluk eki")))
print("Negative verbs are added.")
wordDict = appendDict(wordDict, (generate(wordDict,"fiil")))
print("Zero infinitive forms of verbs are added.")
revisedDict = dict(wordDict)
for olay in ["unsuz yumusamasi","unlu daralmasi","unlu dusmesi"]:
    newDict = {}
    newDict = generate(wordDict,olay)
    revisedDict = appendDict(revisedDict,newDict)
    if olay=="unsuz yumusamasi":
        print("Consonant softening forms are added.")
    if olay=="unlu daralmasi":
        print("Becoming close vowel forms are added.")
    if olay=="unsuz yumusamasi":
        print("Dropping vowel forms are added.")

with open('revisedDict.pkl', 'wb') as f:
    pickle.dump(revisedDict, f)

print("Transformed lexicon is saved to revisedDict.pkl")



