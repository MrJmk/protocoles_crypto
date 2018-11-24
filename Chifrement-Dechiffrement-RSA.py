from struct import pack, unpack

def sha1(data):
    bytes=""
    
    """Retourne la somme SHA1 sous forme de 40 caractères hexadecimal"""
    h0=0x67452301
    h1=0xEFCDAB89
    h2=0x98BADCFE
    h3=0x10325476
    h4=0xC3D2E1F0
    
    for n in range(len(data)):
        bytes+='{0:08b}'.format(ord(data[n]))
    bits=bytes+"1"
    pBits=bits
    
    while len(pBits)%512!=448:
        pBits+="0"
    
    pBits+='{0:064b}'.format(len(bits)-1)
    
    def chunks(l,n):
        return [l[i:i+n] for i in range(0,len(l),n)]
    
    def rol(n,b):
        return ((n<<b)|(n>>(32-b))) & 0xffffffff
    
    for c in chunks(pBits,512):
        words=chunks(c,32)
        w=[0]*80
        for n in range(0,16):
            w[n]=int(words[n],2)
        for i in range(16,80):
            w[i]=rol((w[i-3]^w[i-8]^w[i-14]^w[i-16]),1)
        
        a=h0
        b=h1
        c=h2
        d=h3
        e=h4
        
        #MAIN LOOP
        for i in range(0,80):
            if 0<=i<=19:
                f=(b&c)|((~b)&d)
                k=0x5A827999
            elif 20<=i<=39:
                f=b^c^d
                k=0x6ED9EBA1
            elif 40<=i<=59:
                f=(b&c)|(b&d)|(c&d)
                k=0x8F1BBCDC
            elif 60<=i<=79:
                f=b^c^d
                k=0xCA62C1D6
            
            temp=rol(a,5)+f+e+k+w[i]&0xffffffff
            e=d
            d=c
            c=rol(b,30)
            b=a
            a=temp
        
        h0=h0+a&0xffffffff
        h1=h1+b&0xffffffff
        h2=h2+c&0xffffffff
        h3=h3+d&0xffffffff
        h4=h4+e&0xffffffff
    
    return '%08x%08x%08x%08x%08x' % (h0,h1,h2,h3,h4)


def euclide(a,b):   
    while b !=0 :       
        a , b = b , a % b   
    return a

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
        
        
def puissance(x,k,n):    
    puiss = 1                         
    while (k>0):       
        if k % 2 != 0 :                        
            puiss = (puiss*x) % n        
        x = x*x % n                     
        k = k // 2    
    return(puiss)
    
    
def cle_privee(p,q,e) :   
    n = p * q    
    phi = (p-1)*(q-1)   
    c,d,dd = euclide_etendu(e,phi)           
    return(d % phi)                      


def codage_rsa(m,n,e):    
    return pow(m,e,n)
    
def decodage_rsa(x,n,d):   
    return pow(x,d,n)
    
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

import random
#choisir les nombres premiers p et q
p = 0
q = 0
while not est_premier(p):
    p = random.randint(100000000, 999999999)
   
while not est_premier(q):   
    q = random.randint(100000000, 999999999)

n = p *q 
phi = (p-1)*(q-1) 
e = 2

g = euclide(phi, e)
while g != 1:
    e = random.randrange(1, phi)
    g = euclide(phi, e)

print("\nLes nombres premier choisis sont:\np=" + str(p) + ", q=" + str(q) + "\n")

print('\ncle publique :',(n,e))

d = inverse(e,phi)
print('\ncle prive :',(n,d))

message_a_chiffrer = str(input('\nEntrez le message que vous souhaitez envoyer à Michel :'))

print("\nl'empreinte numérique du message calculé par SHA1 est : ",sha1(message_a_chiffrer))

print("\nla signature du message est donc :")
l1=[]
for i in sha1(message_a_chiffrer):
    asci_mot = ord(i)
    C = pow(asci_mot,d,n)
    l1.append(C)
    print(C , end='')

print('\n\nle Message crypté à envoyer est :')
l=[]
for i in message_a_chiffrer:
    asci_mot = ord(i)
    C = pow(asci_mot,e,n)
    l.append(C)
    print(C , end='')

print("\n\nAinsi le message crypté et la signature sont envoyé à Michel")

print("\n\nMichel décrypte le Message crypté qu'il a reçu :")
mess=""
for j in l:
    Me = pow(j,d,n)
    message = (chr(Me))
    mess=mess+message
    print(message , end='')
    
print("\n\nMichel calcul l'empreinte numérique du message reçu : ",sha1(mess))

print("\n\nMichel décrypte la signature qu'il a reçu :")
for j in l1:
    Me = pow(j,e,n)
    message = (chr(Me))
    print(message , end='')



