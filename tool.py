#@author Carlo Maria Conti
#This script allows you to patch functions of a react application from the bundle code


#USAGE python3 ./tool [fileName.bundle]
#if [fileName] is not added, the file index.android.bundle is read by deafualt


import os
import re
import sys
from shutil import copyfile


def getAllFunctions(f):

   fin = open(f, "r")
   pattern="\w*\s*:function\(\w*[\,\w]*\)"
   lista=[]

   for linea in fin:
       x= re.findall(pattern, linea)
       if x:
          for el in x:
              lista.append(el.split(":")[0])
       
   l=list(set(lista))
   l.sort()
   for el in l:
       print(el)



   fin.close()   

def metodo1(l, funzione,f,out):
    if len(l)==1:
        funzioneDaSos=l[0]+"{"
        args=l[0].split("(")[1].split(")")[0]
        if args=="":
            print("La funzione non presenta argomenti, verrà scritto ciao nel console.log()")
            pattern=funzioneDaSos+"console.log(\"ciao\");"
        else:
            pattern=funzioneDaSos+"console.log("+args +");"
    else:
        r=input("Quale? Scrivere il numero della funzione ")
        funzioneDaSos=l[int(r)-1]+"{"

        args=l[int(r)-1].split("(")[1].split(")")[0]
        if args=="":
            print("La funzione non presenta argomenti, verrà scritto ciao nel console.log()")
            pattern=funzioneDaSos+"console.log(\"ciao\");"
        else:
            pattern=funzioneDaSos+"console.log("+args+");"
    fout = open("./tmp", "w")
    fin = open(f, "r")
    count=1
    for line in fin:
        if funzioneDaSos in line:
            fout.write(line.replace(funzioneDaSos, pattern))
            print("Modificata funzione "+ funzioneDaSos.split("{")[0]+" alla riga n°"+str(count)+" del file "+ f)
            count+=1
        else:
            fout.write(line)
            count+=1     
    
    fin.close()
    fout.close()
    copyfile("./tmp",f)
    os.remove("./tmp")



def metodo2(funzione,f,out):
    print("Se la funzione che si cerca non è nella forma "+funzione+":function( è possibile comunque patcharla tramite l'aggiunta di una funzione ausiliaria prima della prima chiamata nel codice sorgente e modificare tutte le occorrenze nel sorgente con il nome di tale funzione ausiliaria")

    ff="my_function"
    p="[^a-zA-Z\.]"+funzione+"\([^()]*\)"

    k=0
    
    fin = open(f, "r")
    print("Tutte le funzioni con lo stesso nome di "+funzione+" e chiamate : ")
    for linea in fin:
        x = re.findall(p, linea)
        if x:
            for y in x:
                print("Riga "+str(k)+": "+y)
        k+=1     
    fin.close()
    print("")
    k=0
    i=0
    T=0
    z=0
    numeroPar=0
    b="a"


    fin = open(f, "r")  
    fout = open("./tmp", "w")
    for linea in fin:
        x = re.findall(p, linea)
        if x:
            for y in x:
                print("Riga "+str(k)+": "+y)
                args=y[len(funzione)+1:].split("(")[1].split(")")
                numeroPar=args[0].split(",")
                print("Trovata una funzione "+funzione+" con "+str(len(numeroPar))+" argomenti.")
                r=input("Il numero di argomenti è giusto?[Y,N] ")
                if r=="Y" or r=="y" or r=="":
                    r=input("Vuoi patchare questa funzione con "+str(len(numeroPar))+" come numero di argomenti?[Y,N] ")
                    if r=="Y" or r=="y" or r=="":
                        T=len(numeroPar)
                        if T==0:
                            b=""
                        else:
                            for z in range(len(numeroPar)):
                                if z > 0:
                                    b=b+",a"+str(z)
                        pattern="function "+ff+"("+b+"){console.log("+b+");return "+funzione+"("+b+")};\n"
                        if i==0:                    
                            fout.write(pattern)
                            i=1
                            print("Aggiunta nuova funzione "+ff+" alla linea "+str(k -1))
                        new=y[0]+ff+y[len(funzione)+1:]
                        linea=linea.replace(y,new)
                        print("Modificata funzione "+funzione+" alla linea n°"+str(k))
                     
                else:
                    T=input("Inserire a mano il numero di argomenti giusto per questa funzione: ")
                    r=input("Vuoi patchare questa funzione con "+str(T)+" come numero di argomenti?[Y,N] ")
                    if r=="Y" or r=="y" or r=="":
                        if T==0:
                            b=""
                        else:
                            for z in range(int(T)):
                                if z > 0:
                                    b=b+",a"+str(z)
                        pattern="function "+ff+"("+b+"){console.log("+b+");return "+funzione+"("+b+")};\n"                                    
                        if i==0:                    
                            fout.write(pattern)
                            print("Aggiunta nuova funzione "+ff+" alla linea "+str(k -1))
                            i=1
                        new=y[0]+ff+y[len(funzione)+1:]
                        linea=linea.replace(y,new)
                        print("Modificata funzione "+funzione+" alla linea n°"+str(k))
        fout.write(linea)                                    
        k+=1     
    if i==0:
        print("Non ho trovato nessuna funzione con nome "+funzione+" che sia chiamata da qualcuno nel codice, termino")
            
    fout.close()
    fin.close()
    copyfile("./tmp",f)
    os.remove("./tmp")

###MAIN
if len(sys.argv) > 1:
    oldF="Old"+str(sys.argv[1])
    copyfile(str(sys.argv[1]),oldF)
    f=str(sys.argv[1])
else:
    #a default leggo il file index.android.bundle
    f="index.android.bundle"
    
    
out=f
print("Benvenuto! Questo script consente di patchare funzioni di un'applicazione react sul codice bundle")
risposta=input("Posso usare due metodi diversi fare patching, vuoi vedere quali funzioni posso supportare?[Y,N]")
if risposta=="n" or risposta=="N":
    print("")
else:
    getAllFunctions(f) 


fin = open(f, "r")

#funzione:function( è il pattern che devo cercare
funzione=input("Digitare la funzione che si desidera patchare (se tale funzione non è presente nell'elenco si può usare il metodo 2): ")

pattern="\w*\s*:function\(\w*[\,\w]*\)"
#mi trovo gli argomenti
lista=[]


for linea in fin:
    x= re.findall(pattern, linea)
    if x:
        for y in x:
            if funzione in y:
                lista.append(y)

      
fin.close()     

l=list(set(lista))
print("Trovate "+str(len(l))+" funzioni con il nome di "+ funzione)
i=1
for el in l:
    print(str(i)+") "+el)
    i=i+1

if len(l)>0:
    risposta=input("Desideri fare patching di una di queste funzioni?[Y,N] ")
    ##metodo 1
    if risposta=="Y" or risposta=="y" or risposta =="":
        metodo1(l,funzione,f,out)
    else:
        #trovate delle funzioni ma nessuna di queste mi va bene
        #metodo 2
        metodo2(funzione,f,out)
       
else:
    #non ho trovato nulla nella forma funzione:function(
    metodo2(funzione,f,out)

