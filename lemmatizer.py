import re
import json
import pickle
import sys

def check(root, suffix, guess, action):
    if action == "unsuz yumusamasi":
        return len(suffix)>0 and suffix[0] in ["a","e","ı","i","o","ö","u","ü"] and checkSuffixValidation(suffix)[0]
    if action == "unlu daralmasi":
        if guess=="demek" and checkSuffixValidation(suffix)[0]:
            return True
        if guess=="yemek" and checkSuffixValidation(suffix)[0]:
            return True
        
        if suffix.startswith("yor"):
            lastVowel = ""
            for letter in reversed(guess[:-3]):
                if letter in ["a","e","ı","i","o","ö","u","ü"]:
                    lastVowel = letter
                    break
            if lastVowel in ["a","e"] and checkSuffixValidation(suffix)[0]:
                return True
        return False
    if action == "fiil" or action == "olumsuzluk eki":
        return checkSuffixValidation(suffix)[0] and not ((root.endswith("la") or (root.endswith("le"))) and suffix.startswith("r"))
    if action == "unlu dusmesi":
        count = 0
        for letter in guess:
            if letter in ["a","e","ı","i","o","ö","u","ü"]:
                count+=1
                lastVowel = letter
        if checkSuffixValidation(suffix)[0] and count==2 and (lastVowel in ["ı","i","u","ü"]) and (len(suffix)>0 and suffix[0] in ["a","e","ı","i","o","ö","u","ü"]):
            if lastVowel == "ı":
                return suffix[0] in ["a","ı"]
            elif lastVowel == "i":
                return suffix[0] in ["e","i"]
            elif lastVowel == "u":
                return suffix[0] in ["a","u"]
            elif lastVowel == "ü":
                return suffix[0] in ["e","ü"]
        return False
    return True
	
def findPos(kelime,revisedDict):
    l = []
    if "'" in kelime:
        l.append([kelime[:kelime.index("'")]+"_1","tirnaksiz",kelime])
    mid = []
    for i in range(len(kelime)):
        guess = kelime[:len(kelime)-i]
        suffix = kelime[len(kelime)-i:]
        ct = 1
            
        while guess+"_"+str(ct) in revisedDict:
            if check(guess, suffix, revisedDict[guess+"_"+str(ct)][1], revisedDict[guess+"_"+str(ct)][0]):
                guessList = (revisedDict[guess+"_"+str(ct)])
                while guessList[0] not in ["kok","fiil","olumsuzluk"]:
                    guessList = revisedDict[guessList[1]]
                mid.append([guessList[1], revisedDict[guess+"_"+str(ct)][0],guess+"_"+str(ct)])
            ct = ct+1
            
    temp = []
    for kel in mid:
        kelime_kok = kel[0][:kel[0].index("_")]
        kelime_len = len(kelime_kok)
        if kelime_kok.endswith("mak") or kelime_kok.endswith("mek"):
            kelime_len -= 3
        not_inserted = True
        for index in range(len(temp)):
            temp_kelime = temp[index]
            temp_kelime_kok = temp_kelime[0][:temp_kelime[0].index("_")]
            temp_len = len(temp_kelime_kok)
            if temp_kelime_kok.endswith("mak") or temp_kelime_kok.endswith("mek"):
                temp_len -= 3
            if(kelime_len>temp_len):
                temp.insert(index,kel)
                not_inserted = False
        if not_inserted:
            temp.append(kel)
    output = l+temp
    if len(output)==0:
        output.append([kelime+"_1","çaresiz",kelime+"_1",])
    return output

def checkSuffixValidation(suff):
    suffixList = ["","a", "abil", "acağ", "acak", "alım", "ama", "an", "ar", "arak", "asın", "asınız", "ayım", "da", "dan", "de", "den", "dı", "dığ", "dık", "dıkça", "dır", "di", "diğ", "dik", "dikçe", "dir", "du", "duğ", "duk", "dukça", "dur", "dü", "düğ", "dük", "dükçe", "dür", "e", "ebil", "eceğ", "ecek", "elim", "eme", "en", "er", "erek", "esin", "esiniz", "eyim", "ı", "ıl", "ım", "ımız", "ın", "ınca", "ınız", "ıp", "ır", "ıyor", "ız", "i", "il", "im", "imiz", "in", "ince", "iniz", "ip", "ir", "iyor", "iz", "k", "ken", "la", "lar", "ları", "ların", "le", "ler", "leri", "lerin", "m", "ma", "madan", "mak", "maksızın", "makta", "maktansa", "malı", "maz", "me", "meden", "mek", "meksizin", "mekte", "mektense", "meli", "mez", "mı", "mış", "mız", "mi", "miş", "miz", "mu", "muş", "mü", "muz", "müş", "müz", "n", "nın", "nız", "nin", "niz", "nun", "nuz", "nün", "nüz", "r", "sa", "se", "sı", "sın", "sınız", "sınlar", "si", "sin", "siniz", "sinler", "su", "sun", "sunlar", "sunuz", "sü", "sün", "sünler", "sünüz", "ta", "tan", "te", "ten", "tı", "tığ", "tık", "tıkça", "tır", "ti", "tiğ", "tik", "tikçe", "tir", "tu", "tuğ", "tuk", "tukça", "tur", "tü", "tüğ", "tük", "tükçe", "tür", "u", "ul", "um", "umuz", "un", "unca", "unuz", "up", "ur", "uyor", "uz", "ü", "ül", "ün", "üm", "ümüz", "ünce", "ünüz", "üp", "ür", "üyor", "üz", "ya", "yabil", "yacağ", "yacak", "yalım", "yama", "yan", "yarak", "yasın", "yasınız", "yayım", "ydı", "ydi", "ydu", "ydü", "ye", "yebil", "yeceğ", "yecek", "yelim", "yeme", "yen", "yerek", "yesin", "yesiniz", "yeyim", "yı", "yım", "yın", "yınca", "yınız", "yıp", "yız", "yi", "yim", "yin", "yince", "yiniz", "yip", "yiz", "yken", "yla", "yle", "ymış", "ymiş", "ymuş", "ymüş", "yor", "ysa", "yse", "yu", "yum", "yun", "yunca", "yunuz", "yup", "yü", "yuz", "yüm", "yün", "yünce", "yünüz", "yüp", "yüz"]
    validList = []
    if suff in suffixList:
        validList.append(suff)
    for ind in range(1,len(suff)):
        if(suff[:ind] in suffixList):
            cont, contList = checkSuffixValidation(suff[ind:])
            if cont:
                contList = [suff[:ind]+"+"+l for l in contList]
                validList = validList+contList
    return len(validList)>0,validList

try:
	with open('revisedDict.pkl', 'rb') as f:
		revisedDict = pickle.load(f)
except IOError:
	print("Please run trainLexicon.py to generate revisedDict.pkl file")

if(len(sys.argv)<1):
	print("Please provide a word as a system arguments")
	sys.exit(0)

word = sys.argv[1]
print("Possible lemmas for",word,"in ranked order:")
findings = findPos(word.lower(), revisedDict)
for finding in findings:
	print(finding[0])