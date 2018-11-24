#importation de randint provenant de numpy.random
from random import randint
from random import randrange

try:
   input = raw_input
except NameError:
   pass
try:
   chr = unichr
except NameError:
   pass
   
#Generateur de nombre premier
def est_premier(nombre_p):
    if nombre_p <= 3:
        if nombre_p <= 1:
            return False
        return True
    if not nombre_p % 2 or not nombre_p % 3:
        return False
    for i in range(5, int(nombre_p ** 0.5) + 1, 6):
        if not nombre_p % i or not nombre_p % (i + 2):
            return False
    return True

def genPrime(n,m):
    a = 0
    while not est_premier(a):
        a = randint(n,m)
    return a

#DEBUT
print("---------------------------------\n----------ALGORITHME RSA---------\n---------------------------------\n")

#création des nombres premiers p et q
p=genPrime(100000000, 999999999)
q=genPrime(100000000, 999999999)
print("\nLes nombres premier choisis sont:\np=" + str(p) + ", q=" + str(q) + "\n")

n=p*q
print("\nn = p * q = " + str(n) + "\n")
phi=(p-1)*(q-1)
print("fonction de Euler [phi(n)=(p-1)(q-1)]: " + str(phi) + "\n")

def pgcd(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a

#inverse multiplicatif modulaire
def euclide_etendu(a,b):   
    x = 1 ; xx = 0
    y = 0 ; yy = 1    
    while b != 0 :        
        q = a // b        
        a , b = b , a % b       
        xx , x = x - q*xx , xx       
        yy , y = y - q*yy , yy    
    return (a,x,y)
    
def inverse(a,n):    
    c,u,v = euclide_etendu(a,n)   
        
    if c != 1 :                  
        return 0    
    else :        
        return u % n 

    
#Choisir un e dans la liste des premier appartenant à [2 ; phi(n)]
e = 2
g = pgcd(phi, e)
while g != 1:
    e = randrange(1, phi)
    g = pgcd(phi, e)
    
#Calcul de d
d=inverse(e,phi)

#On obtient donc les clés public et privé
print("\nNotre clé public est la paire des nombres (e=" + str(e) + ", n=" + str(n) + ").\n")
print("\nNotre clé privée est la paire des nombres (d=" + str(d) + ", n=" + str(n) + ").\n")


