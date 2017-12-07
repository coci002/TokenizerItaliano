#prova
#punti: come punteggiatura, come abbreviazione (cercare lista abbreviazioni italiano),
#se parola che segue è minuscolo allora abbreviazione. Eccezione: abbreviazione come ultima parola della frase.
#complicazione data dai discorsi diretti che appaiono dentro frase madre:
#es. “Why not bite the bullet?” said a spokesman <- senza frase citata manca il soggetto -> se minuscola dopo virgolette è una frase unica (non sempre vero es. “You still do that?” Abbey said.)

#punti esclamativi/interrogativi: punteggiatura quasi sempre, con rare eccezioni (yahoo!)
#due punti, punto e virgola: spesso separano due frasi, ma spesso è punteggiatura interna alla frase
#idem, a volte usati per enumerazioni -> non considerare in italiano questi casi

#espressioni multiparola: "et cetera", "ad hoc", "en vogue", "3.30pm", "Dic. 23 1990", proper names "Daimler Chrisler AG"(<- non curartene è Named Entity Recognition)
#clitics: opposto delle mutliparola, da una sola parola, più token "amarlo", "l'essere"

#dehypenation: togliere il trattino messo per spezzare una parola. 1) preprocessing-> pre- processing -> preprocessing
#2) pre-processing -> pre- processing -> pre-processing 2) pre- and postprocessing-> pre-\n and postprocessing-> pre- and postprocessing

#spazio mancante: es. "ore.Le" oppure "comunque,quella"

#Emoticon: :)
#Emoji: ':smiley:' or '\U0001f604' '🔥'
#URL
#Indirizzo email

from emoji import UNICODE_EMOJI
import re

def is_emoji(s):
    return s in UNICODE_EMOJI

def is_emoticon(s):
    if (re.search(r"^[(>:#;=*[8|\-B/\\@<~^%$LXoO0}3Vb][a-zA-Z0-9',v(>:#;=*+[8|\-B/\\@<~^%$LXoO0}3Vb)]*$",s)):
        print("è una emoticon")
        return 1
    else:
        print("non è una emoticon")
        return 0

'''if (is_emoji("🔥")):
    print("è una emoji")
else:
    print("non è una emoji")

is_emoticon("XD")'''

listaParole = []
listaAbbreviazioni = []
listaMultiparole = []

def createList(file, lista):
    with open(file) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip('\n') for x in content]
        for x in content:
            words = x.split()
            for y in words:
                lista.append(y)

def createListWhitespaces(file, lista):
    with open(file) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip('\n') for x in content]
        for x in content:
            lista.append(x)

createList("testo0.txt", listaParole)
#print(listaParole)
createList("abbreviazioniITA.txt", listaAbbreviazioni)
createListWhitespaces("multiWordExprITA.txt", listaMultiparole)
print(listaMultiparole)


#prova = "Nel.mezzo.del.cammin"
def splitKeep(c, s):
    result = []
    if c in s:
        i = s.index(c)
        result.append(s[0:i])
        result.append(s[i:i+1])
        if (c in s[i+1:len(s)]):
            resto = splitKeep(c, s[i+1:len(s)])
            for y in resto:
                result.append(y)
        else:
            if len(s[i+1:len(s)])>0:
                result.append(s[i+1:len(s)])
    else:
        result = s
    return result

prova2=[]
#for x in listaParole:
#    prova2.append(splitKeep('.', x))
#print(prova2)

def dotIsPunctuation(s, l):
    if s in listaAbbreviazioni:
        return 0
    #se ha un punto non alle estremità
    else:
        if s.find('.')!= len(s)-1:
            return 1
        else:
            index = l.index(s)
            #se non è l'ultimo elemento della lista, guardo la parola seguente
            if index < len(l)-1:
                #Se la prima lettera della parola seguente è maiuscola
                if l[index+1][0].isupper():
                    return 1
                else:
                    return 0
            #se è l'ultimo punto del documento, sicuramente è di punteggiatura
            else:
                return 1

def isMultiword(s, l):
    index = l.index(s)
    #se non è l'ultimo elemento della lista, guardo la parola seguente
    if index < len(l)-1:
        multiword = s + ' '+l[index+1]
        if multiword in listaMultiparole:
            print(multiword)
            return 1
    return 0

def createToken(lista):
    for x in lista:
        #vado a spezzare la parola col punto se contiene un punto e se questo è un punto di punteggiatura
        if '.' in x and (dotIsPunctuation(x, lista)):
            parole = splitKeep('.', x)
            index = lista.index(x)
            lista.pop(index)
            counter = 0
            for y in parole:
                if y != '':
                    lista.insert(index+counter, y)
                    counter=counter+1
    for x in lista:
        if isMultiword(x, lista):
            index = lista.index(x)
            #concateno le parole (per ora solo lunghezza 2)
            multiparola = lista[index] + ' ' + lista[index+1]
            lista.pop(index)
            lista.pop(index)
            lista.insert(index, multiparola)
    return lista


lista2 = createToken(listaParole)
print(lista2)
