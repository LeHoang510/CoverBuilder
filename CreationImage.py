# -*- coding: utf-8 -*-

"""
Created on Thu Feb 25 11:16:48 2021

@author: leplumey
"""

# Classes Qt necessaires
import re

from PyQt5.QtGui import QImage, qRgb, qRed, qBlue, qGreen

# Importation du module JSON
import json

# Pour effectuer des verifications sur les fichiers existants
import os.path

# La classe de gestion d'une image
class ARMImage(QImage):
    # Constructeur
  def __init__(self,L=0,H=0,F=0,nom="",output=""):
    if L>0 and H>0:
      QImage.__init__(self,L,H,F)
    elif nom!="":
      QImage.__init__(self,nom)
      print("Hauteur ("+nom+"): "+str(self.height()))

    # Gestion des entrees-sorties pour être compatible avec une interface
    if output=="":
      self.out=self
    else:
      self.out=output

  # Initialiser une image à une couleur
  def initialiserCouleur(self, couleur):
    for y in range(self.height()):
      for x in range(self.width()):
        # Mise de la couleur en chaque pixel
        self.setPixel(x,y,couleur)

  # Changer la couleur de l'image
  def changerCouler(self, couleur):
    for y in range(self.height()):
      for x in range(self.width()):
        if self.pixel(x,y) != qRgb(255,255,255):
          self.setPixel(x, y, couleur)

  # Initialiser une image à une couleur
  def initialiserRectangleCouleur(self,couleur,xd,yd,xf,yf):
    print(str(xd)+"-"+str(xf)+"/"+str(yd)+"-"+str(yf))
    for y in range(yd,yf+1):
      for x in range(xd,xf+1):
        # Mise de la couleur en chaque pixel
        self.setPixel(x,y,couleur)
        
  # Initialiser une image à une couleur
  def initialiserRectangleDegCouleur(self,tcoul1,tcoul2,xd,yd,xf,yf):
    # Calcul des cofficients pour chaque couleur
    ar=[0,0,0]
    br=[0,0,0]
    for i in range(3):
      ar[i]=(tcoul2[i]-tcoul1[i])/(yf-yd)
      br[i]=tcoul1[i]-ar[i]*yd
    for y in range(yd,yf+1):
      couleur=qRgb(int(ar[0]*y+br[0]),int(ar[1]*y+br[1]),int(ar[2]*y+br[2]))
      for x in range(xd,xf+1):
        # Mise de la couleur en chaque pixel
        self.setPixel(x,y,couleur)
        
  # Recopier une image à un endroit donne
  def recopierImage(self, image, xc, yc):
    for y in range(image.height()):
      for x in range(image.width()):
        if xc+x<self.width() and yc+y<self.height():
          self.setPixel(xc+x,yc+y,image.pixel(x,y))

  #=======================================================================
  #	Methode :	BOOL Image8bits::EcrirePoint(int x, int y, int couleur)
  #	But:		Init. d'un point dans une image 24 bits
  #	Parametres:	x, y : coordonnees du point
  #				couleur : numero du plan
  #	Retour :	L'operation s'est-elle bien passee ?
  #=======================================================================
  def ecrirePoint(self,x,y,couleur):      
    # Verification des coordonnees
    if (x<0)or(y<0)or(x>=self.width())or(y>=self.height()):
        return(False)
    
    # Modification du pixel
    self.setPixel(int(x),int(y),couleur)
    return(True)

  #=======================================================================
  #    Methode :   segment(self,xdeb,ydeb,xfin,yfin,couleur)
  #    But:        La routine Segment_unique_l trace un segment de droite
  #    Parametres:    Les coordonnees des extremites du segment:
  #                - xdeb: abscisse de l'origine
  #                - ydeb: ordonnee de l'origine
  #                - xfin: abscisse du point final
  #                - yfin: ordonnee du point final
  #                - couleur: la couleur
  #=======================================================================
  def segment(self,xdeb,ydeb,xfin,yfin,couleur):
    #    x,y   : Position courante du point a afficher  
    #    dx,dy : Ecart entre xdeb et xfin, ydeb et yfin 
    #    i     : Indice de la boucle d'affichage de l'ensemble des pixels du segment
    #    xincr : Accroissement en x d'une colonne a l'autre (1,-1) 
    #    yincr : Accroissement en y d'une ligne a l'autre (1,-1)   
    #    ecart : Valeur de l'erreur permettant de connaitre la distance de la droite 
    #            theorique a la droite tracee              
    #            Quand cette erreur depasse 1, il est temps de modifier les traces 
    #            (en realite, sa valeur est multipliee par dx dans le but d'eviter 
    #            divisions et multiplications)  

    # Affichage du point d'origine 
    self.ecrirePoint(xdeb,ydeb,couleur)

    # Coordonnees courantes = coordonnees du point initial 
    x=xdeb
    y=ydeb

    # Calcul des ecarts en x et y entre les extremites 
    dx=abs(xfin-xdeb)
    dy=abs(yfin-ydeb)

    # Calcul des facteurs d'accroissement en x et en y 
    if (xdeb<xfin):
      xincr=1
    else:
      xincr=-1;
    if (ydeb<yfin):
      yincr=1
    else:
      yincr=-1;

    # Tracage du segment suivant la direction ayant le plus faible accroissement 
    if dx>dy:
      # Au debut, pas d'erreur ce qui correspond a ecart = 0.5 (* dx) 
      ecart=dx>>1
      # Boucle de trace de chaque point du segment 
      for i in range(1,dx+1):
        # Passer au point de la colonne suivante 
        x+=xincr
        # Mettre a jour l'erreur 
        ecart+=dy
        # Quand l'erreur est trop importante, remettre a jour y 
        if ecart>=dx: 
          y+=yincr
          ecart-=dx
        # Affichage du point courant 
        self.ecrirePoint(x,y,couleur)
    else: 
      # Au debut, pas d'erreur ce qui correspond a ecart = 0.5 (* dx) 
      ecart=dy>>1
      # Boucle de trace de chaque point du segment 
      for i in range(1,dy+1):
        # Passer au point de la ligne suivante 
        y+=yincr
        # Mettre a jour l'erreur 
        ecart+=dx
        # Quand l'erreur est trop importante, remettre a jour x 
        if ecart>=dy:
          x+=xincr
          ecart-=dy
          
        # Affichage du point courant 
        self.ecrirePoint(x,y,couleur)

# La classe qui encapsule l'ensemble des traitements
class CreationImage:
  # Methode pour generer un JSON
  def genererJSON(desc, nom="creatImage.json"):
    try:
      f = open(nom, 'w')
    except IOError:
      print("Erreur d'ouverture du fichier ", nom)
    else:
      # Sauvegarde d'un fichier au format JSON evitant de refaire la requête
      json.dump(desc,f,sort_keys=True, indent=2, ensure_ascii=False)
      f.close()
  
  # Generation d'un JSON initial   
  def genererJSONInitial(nom="creatImage.json"):
    # Essai d'ecriture d'un fichier json d'origine pour forcer 
    # les caractères au bon format
    desc={  "Image origine": "imageSaintLo1.jpg",
            "Image resultat": "imageResultat.jpg",
            "Image incrustation gauche": "blason.jpg",
            "Image incrustation droite": "blason.jpg",
            "Couleur flèche":[32,177,82],
            "Epaisseur flèche":240,
            "Position flèche":50,
            "Taille bordure":240
           }    
    CreationImage.genererJSON(desc,nom)
  
  # Constructeur  
  def __init__(self,nomjson="creatImage.json",output=""):
    # Gestion des entrees-sorties pour être compatible avec une interface
    if output=="":
      self.out=self
    else:
      self.out=output

    # Ouverture du fichier json
    try:
      f = open(nomjson, 'r')
    except IOError:
      self.out.afficher("Le fichier json associe au registre n'est pas trouve - "+nomjson)
    else:
      try:
        # Chargement du fichier json
        self.description=json.load(f)
      except:
        self.out.afficher("Echec de chargement du fichier de description (sûrement un problème de syntaxe) - "+nomjson)   
      self.out.afficher(str(self.description))
      f.close()
      
      # Memorisation du nom du fichier json
      self.nom=nomjson

  # Methode d'affichage par defaut    
  def afficher(self, chaine,fin="\n"):
    print(chaine,end=fin)
    
  # Initialiser une image à une couleur
  """def initialiserCouleur(self, image, couleur):
    for y in range(image.height()):
      for x in range(image.width()):
        # Mise de la couleur en chaque pixel
        image.setPixel(x,y,couleur)"""

  # Methode de calcul de l'image resultat avec une decoration gauche-droite style Memoire des Hommes
  def calculerImage(self):
    self.test=ARMImage(50,50,QImage.Format_RGB32)
    # Charger l'image d'origine
    self.origine=ARMImage(nom=self.description["Image origine"])
    self.incrGauche=ARMImage(nom=self.description["Image incrustation gauche"])
    self.incrDroite=ARMImage(nom=self.description["Image incrustation droite"])
    self.afficher("Après chargement")
    self.afficher("Largeur image à incruster: "+str(self.incrDroite.width()))
    print(self.origine.height())
    # Creer une image de plus grande dimension
    self.resultat=ARMImage(self.origine.width()+2*self.description["Taille bordure"],
                         self.origine.height(), self.origine.format())
    self.resultat.initialiserCouleur(qRgb(255,255,255))
    # Recopier l'image d'origine dans l'image plus grande
    self.resultat.recopierImage(self.origine,self.description["Taille bordure"],0)
    # Inclure les sous images en haut à gauche et à droite
    self.resultat.recopierImage(self.incrGauche,0,0)
    self.resultat.recopierImage(self.incrDroite,self.resultat.width()-self.incrDroite.width()-1,0)
    
    # Dessiner les flèches
    # - Flèche de gauche
    marge=self.description["Marge"]
    posy=self.description["Position flèche"]*self.resultat.height()/100
    cold=int(self.description["Taille bordure"]/4)
    colf=self.description["Taille bordure"]-1
    #couleur=qRgb(self.description["Couleur flèche claire"][0],self.description["Couleur flèche claire"][1],self.description["Couleur flèche claire"][2])
    #for i in range(self.description["Epaisseur flèche"]):
    #  self.resultat.segment(cold,posy+i,colf,posy+i,couleur)
    self.resultat.initialiserRectangleDegCouleur(self.description["Couleur flèche claire"],self.description["Couleur flèche"],cold,int(posy),colf,int(posy+self.description["Epaisseur flèche"]))
      
    couleur=qRgb(self.description["Couleur compl. 1"][0],self.description["Couleur compl. 1"][1],self.description["Couleur compl. 1"][2])
    epaisseur=self.description["Epaisseur flèche"]/4
    #self.resultat.initialiserRectangleCouleur(couleur,0,int(posy+marge),colf-marge,int(posy+marge+self.description["Epaisseur flèche"]/4))
    self.resultat.initialiserRectangleDegCouleur(self.description["Couleur compl. 1"],self.description["Couleur flèche"],0,int(posy+marge),colf-marge,int(posy+marge+self.description["Epaisseur flèche"]/4))
    #couleur=qRgb(self.description["Couleur compl. 2"][0],self.description["Couleur compl. 2"][1],self.description["Couleur compl. 2"][2])
    #self.resultat.initialiserRectangleCouleur(couleur,0,posy+20,colf,int(posy+20+self.description["Epaisseur flèche"]/4))
    #couleur=qRgb(self.description["Couleur compl. 3"][0],self.description["Couleur compl. 3"][1],self.description["Couleur compl. 3"][2])
    #self.resultat.initialiserRectangleCouleur(couleur,int(colf-marge-self.description["Epaisseur flèche"]/4),int(posy-3*marge),colf-marge,int(posy+3*marge+self.description["Epaisseur flèche"]))
    self.resultat.initialiserRectangleDegCouleur(self.description["Couleur compl. 3"],self.description["Couleur compl. 4"],int(colf-marge-self.description["Epaisseur flèche"]/4),int(posy-3*marge),colf-marge,int(posy+3*marge+self.description["Epaisseur flèche"]))
    #couleur=qRgb(self.description["Couleur compl. 2"][0],self.description["Couleur compl. 2"][1],self.description["Couleur compl. 2"][2])
    #self.resultat.initialiserRectangleCouleur(couleur,int(colf-marge-1.5*epaisseur),int(posy+marge/2),int(colf-marge-epaisseur/2),int(posy+1.5*marge+self.description["Epaisseur flèche"]/4))
    self.resultat.initialiserRectangleDegCouleur(self.description["Couleur compl. 2"],self.description["Couleur flèche claire"],int(colf-marge-1.5*epaisseur),int(posy+marge/2),int(colf-marge-epaisseur/2),int(posy+1.5*marge+self.description["Epaisseur flèche"]/4))

    # - Flèche de droite
    posy=self.description["Position flèche"]*self.resultat.height()/100
    cold=self.origine.width()+self.description["Taille bordure"]
    colf=self.origine.width()+2*self.description["Taille bordure"]-1
    couleur=qRgb(self.description["Couleur flèche"][0],self.description["Couleur flèche"][1],self.description["Couleur flèche"][2])
    # Mise en place d'une strategie de degrades
    tcoul1=self.description["Couleur flèche"]
    tcoul2=self.description["Couleur flèche claire"]
    ar=[0,0,0]
    br=[0,0,0]
    for i in range(3):
      ar[i]=(tcoul2[i]-tcoul1[i])/(self.description["Epaisseur flèche"]-1)
      br[i]=tcoul1[i]
    for i in range(self.description["Epaisseur flèche"]):
      couleur=qRgb(int(ar[0]*i+br[0]),int(ar[1]*i+br[1]),int(ar[2]*i+br[2]))
      #self.resultat.segment(i,posy-i,colf,posy-i,couleur)
      if (colf-i>cold): self.resultat.segment(cold,posy+i,colf-i,posy+i,couleur)

    # Sauvegarder l'image resultat
    # - On ne peut effectuer une sauvegarde que dans un nouveau fichier
    if len(self.description["Image resultat"])!=0 and not os.path.isfile(self.description["Image resultat"]):
      self.afficher("Sauvegarde "+self.description["Image resultat"])
      self.resultat.save(self.description["Image resultat"])
      if not os.path.isfile(self.description["Image resultat"]):
        self.afficher("Echec sauvegarde")

  def ajouter2(self):
    for i in range(len(self.description["Image incrustation"])):

      #Lien de l'image d'origine et lien resultat
      lienOrigine="./"+self.description["Dossier origine"]+"/"+self.description["Image incrustation"][i]
      lienResultat="./"+self.description["Dossier resultat"]+"/"+re.sub(".[a-z]*$",self.description["Type resultat"],self.description["Image incrustation"][i])

      self.origine = ARMImage(nom=lienOrigine)                        # Image d'origine
      self.deux = ARMImage(nom=self.description["Image numero deux"]) # Image de deux

      # Couleur de deux
      red=self.description["Couleur de deux"][i][0]
      green=self.description["Couleur de deux"][i][1]
      blue=self.description["Couleur de deux"][i][2]
      # Changer la couleur de deux
      self.deux.changerCouler(qRgb(red,green,blue))

      # Creer une image de plus grande dimension
      self.resultat = ARMImage(self.origine.width() + 2 * self.description["Taille bordure"], self.origine.height(),self.origine.format())
      self.resultat.initialiserCouleur(qRgb(255, 255, 255))
      # Recopier l'image d'origine dans l'image plus grande
      self.resultat.recopierImage(self.origine, self.description["Taille bordure"], 0)
      self.resultat.recopierImage(self.deux,2 * self.description["Taille bordure"] + self.origine.width() - self.deux.width(), self.origine.height()-self.deux.height())

      #Sauvegarder l'image
      if len(lienResultat) != 0 and not os.path.isfile(lienResultat):
        self.afficher("Sauvegarde " + lienResultat)
        self.resultat.save(lienResultat)
        if not os.path.isfile(lienResultat):
          self.afficher("Echec sauvegarde")



# ===================================================================
#                         Programme principal
# ===================================================================
if __name__ == "__main__":
  #CreationImage.genererJSONInitial()
  cim=CreationImage()
  cim.calculerImage()
  cim.ajouter2()

