import cv2
import numpy as np

fragments = []
with open('./assets/fragments.txt', 'r') as file:
    for line in file:
        i, x, y, r = map(float, line.split())
        fragments.append((i, x, y, r))

background = np.zeros((775, 1707, 3))
# np.zeros c'est pas np.zeros(x,y,channel) ? y x channel okk

frag = cv2.imread('./assets/frag_eroded/frag_eroded_1.png')
ht, wd = frag.shape[:2]


background[0:ht, 0:wd] = frag
#je comprends pas cette ligne
#En gros : tu selectionnes la région dans background où tu veux mettre le fragment et
# tu lui assignes le fragment
#[0:ht, 0:wd] c'est la region de background où tu veux mettre le fragment
# ça selectionne un rectangle de hauteur ht et de largeur wd depuis 0
# mais euh les positions qu'on a dans le fichier texte
# ça positionne le fragment depuis son centre ? jsp faut tester
# parce que moi quand je veux positionner un fragment comme ça ba j'ai un problème de shape
# même problème ici
#Mnt c'est bon
# okk ba je vais essayer merci

(i, x, y, r) = fragments[1]

x1 = int(x)
y1 = int(y)
print(x1, y1)
x2 = int(x + wd)
y2 = int(y + ht)

background[y1:y2, x1:x2] = frag
cv2.imshow('fresque', background)
cv2.waitKey(0)