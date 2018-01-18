#prova
#punti: come punteggiatura, come abbreviazione (cercare lista abbreviazioni italiano),
#se parola che segue è minuscolo allora abbreviazione. Eccezione: abbreviazione come ultima parola della frase.
#complicazione data dai discorsi diretti che appaiono dentro frase madre:
#es. “Why not bite the bullet?” said a spokesman <- senza frase citata manca il soggetto -> se minuscola dopo virgolette è una frase unica (non sempre vero es. “You still do that?” Abbey said.)

#punti esclamativi/interrogativi: punteggiatura quasi sempre, con rare eccezioni (yahoo!)
#due punti, punto e virgola: spesso separano due frasi, ma spesso è punteggiatura interna alla frase
#idem, a volte usati per enumerazioni -> non considerare in italiano questi casi

#espressioni multiparola: "et cetera", "ad hoc", "en vogue", "3.30 pm", "Dic. 23 1990", proper names "Daimler Chrisler AG"(<- non curartene è Named Entity Recognition)
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
    #if (re.search(r"^[(>:#;=*[8|\-B/\\@<~^%$LXO0}3Vb][a-zA-Z0-9',v(>:#;=*+[8|\-B/\\@<~^%$LXoO0}3Vb)]*$",s)):
    if s in [":D", ":(", "XD", ":-D", ":-(", ";)", ":-D", ";P", ":P"]:
        return 1
    else:
        return 0

'''if (is_emoji("🔥")):
    print("è una emoji")
else:
    print("non è una emoji")

is_emoticon("XD")'''

time_re = re.compile(r'^(([01]?\d|2[0-3])(:|.)([0-5]\d)|24:00)$')
def is_time_format(s):
    return bool(time_re.match(s))

decimalNumRe = re.compile('[0-9]+\.[0-9]+')
def is_decimal(s):
    return bool(decimalNumRe.match(s))

listaParole = []
listaAbbreviazioni = []
listaMultiparole = []
listaMesi = []
listaParoleTrattino = []
listaNonClitici = []

def createList(file, lista):
    with open(file) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip('\n') for x in content]
        for x in content:
            words = x.split()
            for y in words:
                lista.append(y)

def createList2(file, lista):
    with open(file) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip('\n') for x in content]
        for x in content:
            words = x.split()
            for y in words:
                lista.append(y.lower())
                lista.append(y)

def createListWhitespaces(file, lista):
    with open(file) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip('\n') for x in content]
        for x in content:
            lista.append(x)

createList("testo0.txt", listaParole)
createList("abbreviazioniITA.txt", listaAbbreviazioni)
createListWhitespaces("multiWordExprITA.txt", listaMultiparole)
createList("mesi.txt", listaMesi)
createList("paroleConTrattino.txt", listaParoleTrattino)
createList2("nonclitici.txt", listaNonClitici)


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


def dotIsPunctuation(s, l):
    if "www" in s or "@" in s:
        return 0
    if is_time_format(s):
        return 0
    if is_decimal(s):
        return 0
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
                if l[index+1][0].isupper() or l[index+1][0].isdigit() or is_emoji(l[index+1][0]) or is_emoticon(l[index+1][0]):
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
            return 1
        if 'am' == l[index+1] or 'pm' == l[index+1]:
            return 1
    return 0

def isDate(s,l):
    index = l.index(s)
    #se ha due parole che la seguono
    if index < len(l)-2:
        #Formati ammessi: 23 Dic 1990 oppure Dic. 23 1990
        if (s.isdigit() and l[index+2].isdigit() and l[index+1] in listaMesi) or (s in listaMesi and l[index+2].isdigit() and l[index+1].isdigit()):
            return 1
    return 0

def isClitic(s):
    #"gli" è un caso a parte
    clitic = ["mi", "ti", "ci", "vi", "lo", "la", "li", "le", "ne", "si"]
    for x in clitic:
        if s.endswith(x) and (s[len(s)-3] == 'r'):
            return 1
    if s.endswith('gli') and (s[len(s)-4] == 'r'):
        return 2
    return 0

def isCliticCumulo(s):
    clitic = ["lo", "la", "li", "le", "ne"]
    for x in clitic:
        if s.endswith(x) and s not in listaNonClitici:
            radice = s[0:len(s)-2]
            if radice.endswith("me") or radice.endswith("te") or radice.endswith("ce"):
                return 1
            if radice.endswith("glie"):
                return 2
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
        if is_emoticon(x[0:2]):
            index = lista.index(x)
            emoticon = x[0:2]
            parola = x[2:len(x)]
            lista.pop(index)
            if emoticon != '':
                lista.insert(index, emoticon)
            if parola != '':
                lista.insert(index+1, parola)
        else:
            if is_emoticon(x[0:3]):
                index = lista.index(x)
                emoticon = x[0:3]
                parola = x[3:len(x)]
                lista.pop(index)
                if emoticon != '':
                    lista.insert(index, emoticon)
                if parola != '':
                    lista.insert(index+1, parola)
            else:
                if is_emoticon(x[len(x)-2:len(x)]):
                    index = lista.index(x)
                    parola = x[0:len(x)-2]
                    emoticon = x[len(x)-2:len(x)]
                    lista.pop(index)
                    if emoticon != '':
                        lista.insert(index, emoticon)
                    if parola != '':
                        lista.insert(index, parola)
                else:
                    if is_emoticon(x[len(x)-3:len(x)]):
                        index = lista.index(x)
                        parola = x[0:len(x)-3]
                        emoticon = x[len(x)-3:len(x)]
                        lista.pop(index)
                        if emoticon != '':
                            lista.insert(index, emoticon)
                        if parola != '':
                            lista.insert(index, parola)

    for x in lista:
        if '!' in x:
            parole = splitKeep('!', x)
            index = lista.index(x)
            lista.pop(index)
            counter = 0
            for y in parole:
                if y != '':
                    lista.insert(index+counter, y)
                    counter=counter+1
    for x in lista:
        if '?' in x:
            parole = splitKeep('?', x)
            index = lista.index(x)
            lista.pop(index)
            counter = 0
            for y in parole:
                if y != '':
                    lista.insert(index+counter, y)
                    counter=counter+1
    for x in lista:
        if ':' in x and not is_emoticon(x) and not x.startswith("http"):
            parole = splitKeep(':', x)
            index = lista.index(x)
            lista.pop(index)
            counter = 0
            for y in parole:
                if y != '':
                    lista.insert(index+counter, y)
                    counter=counter+1
    for x in lista:
        if ';' in x and not is_emoticon(x):
            parole = splitKeep(';', x)
            index = lista.index(x)
            lista.pop(index)
            counter = 0
            for y in parole:
                if y != '':
                    lista.insert(index+counter, y)
                    counter=counter+1
    for x in lista:
        if ',' in x:
            parole = splitKeep(',', x)
            index = lista.index(x)
            lista.pop(index)
            counter = 0
            for y in parole:
                if y != '':
                    lista.insert(index+counter, y)
                    counter=counter+1
    for x in lista:
        if '\'' in x:
            parole = splitKeep('\'', x)
            index = lista.index(x)
            lista.pop(index)
            counter = 0
            for y in parole:
                if y != '':
                    lista.insert(index+counter, y)
                    counter=counter+1
    for x in lista:
        if '"' in x:
            parole = splitKeep('"', x)
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

    for x in lista:
        if isDate(x, lista):
            index = lista.index(x)
            #concateno data anno e mese
            data = lista[index] + ' ' + lista[index+1]+ ' ' + lista[index+2]
            lista.pop(index)
            lista.pop(index)
            lista.pop(index)
            lista.insert(index, data)
    #gestisce la dehypenation
    for x in lista:
        index = lista.index(x)
        #non considero i casi in cui c'è solamente la "-"
        if x.endswith("-") and len(x)>1 and index<len(lista):
            tmp = x[0:len(x)]+lista[index+1]
            if tmp in listaParoleTrattino:
                parola = tmp
            else:
                parola = x[0:len(x)-1]+lista[index+1]
            lista.pop(index)
            lista.pop(index)
            lista.insert(index, parola)
    for x in lista:
        index = lista.index(x)
        if isClitic(x) == 1:
            parola = x[0:len(x)-2]
            clitico = x[len(x)-2:len(x)]
            lista.pop(index)
            lista.insert(index, parola)
            lista.insert(index+1, clitico)
        else:
            if isClitic(x) == 2:
                parola = x[0:len(x)-3]
                clitico = x[len(x)-3:len(x)]
                lista.pop(index)
                lista.insert(index, parola)
                lista.insert(index+1, clitico)
    for x in lista:
        index = lista.index(x)
        if isCliticCumulo(x) == 1:
            parola = x[0:len(x)-4]
            pronome = x[len(x)-4:len(x)-2]
            clitico = x[len(x)-2:len(x)]
            lista.pop(index)
            lista.insert(index, parola)
            lista.insert(index+1, pronome)
            lista.insert(index+2, clitico)
        else:
            if isCliticCumulo(x) == 2:
                parola = x[0:len(x)-6]
                pronome = x[len(x)-6:len(x)-2]
                clitico = x[len(x)-2:len(x)]
                lista.pop(index)
                lista.insert(index, parola)
                lista.insert(index+1, pronome)
                lista.insert(index+2, clitico)
    #gestione emoji
    for x in lista:
        for carattere in x:
            if is_emoji(carattere):
                parole = splitKeep(carattere, x)
                index = lista.index(x)
                lista.pop(index)
                counter = 0
                for y in parole:
                    if y != '':
                        lista.insert(index+counter, y)
                        counter=counter+1
                break

    return lista


lista2 = createToken(listaParole)
for x in lista2:
    print(x)
