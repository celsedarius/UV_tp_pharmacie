import connexion
import six
import pymongo
import json
import random

from bson import ObjectId
from bson.json_util import dumps
from datetime import datetime


from swagger_server.models.centre import Centre  # noqa: E501
from swagger_server.models.medecin import Medecin  # noqa: E501
from swagger_server.models.pharmacie import Pharmacie  # noqa: E501
from swagger_server.models.produit import Produit  # noqa: E501
from swagger_server import util

con = pymongo.MongoClient()
db = con["pharmacie"]

DISTANCE_MAX=300000


def traitement(text):  # noqa: E501
    text= text.lower()
    #text=text.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    return text.strip()

def check_dci(a,b):  # noqa: E501
    liste_a_verif=a.split(',')
    liste=b.split(',')
    if len(liste)!=len(liste_a_verif):
        return False
    for x in liste_a_verif:
        if x not in liste:
            return False
    return True


def recherche(long, lat, x):  # noqa: E501

    
    return db['pharmacies'].aggregate( [
            {
                "$geoNear": {
                    "near": { "type": "Point", "coordinates": [ long, lat ] },
                    "spherical": False,
                    
                    "distanceField": "calcDistance",
                    "$maxDistance": DISTANCE_MAX
                }
                
            },
            {   "$match": { "_id": x['pharmacie'][0]['_id'] }}
        ])
    

def recherche_medicament(long, lat, medicament):  # noqa: E501
    
    # query = { "nom": { "$regex": '.*'+a+'.*', "$options" :'i' } }

    pharmacies=[]
    nom_pharmacies=['']
    for x in db['produits'].aggregate([
        {   "$match": { "nom": traitement(medicament) }},
        {
            "$lookup":
            {
                "from": "pharmacies",
                "localField": "pharmacies._id",
                "foreignField": "_id",
                "as": "pharmacie"
            }
        },
        { "$project": { "pharmacie": 1,  "_id": 0 }}
    ]):  # noqa: E501
        
        for i in recherche(long, lat, x):
            if i['nom'] not in nom_pharmacies:
                nom_pharmacies.append(i['nom'])  
                pharmacies.append(json.loads(dumps(i))) 
    return pharmacies
   


def medicament_equivalent(long, lat, medicament):  # noqa: E501
    pharmacies={}
    produits=[]
    query = { "nom": traitement(medicament) }

    #on recuperer les produits de meme noms , afin de trouver les equivalents de chacun 
    for y in db['produits'].find(query):  # noqa: E501
        
        #pour tout les produits du meme nom on verifie si il ya une equivalence
        #equivalence= dci, dosage, forme_galenique
        for w in db['produits'].find({ 
            'dci':y['dci'], 
            'dosage': y['dosage'],
            'forme_galenique':y['forme_galenique'],
        }):
            if w['nom']!=traitement(medicament):
                produits.append(w)

    # for w in db['produits'].find({ "nom": { traitement(x)+'.*', "$options" :'i' } }):
    #     if w['nom']!=traitement(medicament):
    #             produits.append(w)

    
    for x in produits:
        liste=[]
        for w in db['produits'].aggregate([
            {   "$match": { "nom": x['nom'] }},
            {
                "$lookup":
                {
                    "from": "pharmacies",
                    "localField": "pharmacies.id",
                    "foreignField": "_id",
                    "as": "pharmacie"
                }
            },
            { "$project": { "pharmacie._id": 1,  "_id": 0 }}
        ]):  # noqa: E501
            nom_pharmacies=[]
            for i in recherche(long, lat, w):
                if i['nom'] not in nom_pharmacies:
                    nom_pharmacies.append(i['nom'])                
                    liste.append(json.loads(dumps(i))) 
            pharmacies[x['nom']]=liste
    return pharmacies






def pharmacie_garde(long, lat):  # noqa: E501

    garde=''
    groupe=['groupe_1','groupe_2','groupe_3','groupe_4']
    for g in groupe:
        for x in db['pharmacie_groupe'].find({'nom':g}, {'debut'}):  # noqa: E501
            d,m,y= x['debut'].split('-')
            diff = datetime.now() - datetime(int(y),int(m),int(d))
            if diff.days%28<21:
                garde=g
                break
    


   

    return json.loads(dumps(db['pharmacies'].find({'groupe':garde})))


def pharmacie_proche(long, lat):  # noqa: E501
    
    pharmacies=[]
    for x in db['pharmacies'].aggregate( [
            {
                "$geoNear": {
                    "near": { "type": "Point", "coordinates": [ long, lat ] },
                    "spherical": False,
                    
                    "distanceField": "distance",
                    "$maxDistance": DISTANCE_MAX
                }
                

            }
        ]):
        pharmacies.append(json.loads(dumps(x)))
    return pharmacies



def hosto_proche(long, lat):  # noqa: E501
    centres=[]
    for x in db['centres'].aggregate( [
            {
                "$geoNear": {
                    "near": { "type": "Point", "coordinates": [ long, lat ] },
                    "spherical": False,
                    
                    "distanceField": "calcDistance",
                    "$maxDistance": DISTANCE_MAX
                }
            }
        ]):
        centres.append(bsonjs.dumps(x.raw))
    return centres



def hosto_add(centre):  # noqa: E501
    if connexion.request.is_json:
        centre = Centre.from_dict(connexion.request.get_json())  # noqa: E501
    db['centres'].insert_one(centre)
    return 'success'
    

def hosto_del(hosto_id):  # noqa: E501
    db['centres'].delete_one({ "_id": ObjectId(hosto_id) })
    return 'success'


def hosto_edit(hosto_id, hosto):  # noqa: E501
    if connexion.request.is_json:
        hosto = Centre.from_dict(connexion.request.get_json())  # noqa: E501
        myquery = { "_id": ObjectId(hosto_id) }
    newvalues = { "$set": { "nom": hosto['nom']} }

    db['centres'].update_one(myquery, newvalues)
    return 'success'
    

def hosto_ls():  # noqa: E501
    return json.loads(dumps(db['centres'].find())) 





def medecin_add(medecin):  # noqa: E501   
    if connexion.request.is_json:
        medecin = Medecin.from_dict(connexion.request.get_json())  # noqa: E501
    db['medecins'].insert_one(medecin)
    return 'success'


def medecin_del(medecin_id):  # noqa: E501
    db['medecins'].delete_one({ "_id": ObjectId(medecin_id) })
    return 'success'


def medecin_edit(medecin_id, medecin):  # noqa: E501
    
    if connexion.request.is_json:
        medecin = Medecin.from_dict(connexion.request.get_json())  # noqa: E501
    myquery = { "_id": ObjectId(medecin_id) }
    newvalues = { "$set": { "nom": medecin['nom'],
                            "tel" : medecin['tel'],
                            "specialite": medecin['specialite']} }

    db['medecins'].update_one(myquery, newvalues)
    return 'do some magic!'


def medecin_ls():  # noqa: E501
    
    return json.loads(dumps(db['medecins'].find()))  # noqa: E501
    


def medicament_add(produit):  # noqa: E501

    if connexion.request.is_json:
        produit = Produit.from_dict(connexion.request.get_json())  # noqa: E501
    db['produits'].insert_one(produit)
    return 'success'


def medicament_del(medicament_id):  # noqa: E501
    db['produits'].delete_one({ "_id": ObjectId(medicament_id) })
    return 'success'


def medicament_edit(medicament_id, produit):  # noqa: E501
  
    if connexion.request.is_json:
        produit = Produit.from_dict(connexion.request.get_json()) 
        
    myquery = { "_id": ObjectId(medicament_id) }
    newvalues = { "$set": { "nom_prod": produit['nom_prod'],
                            "dci" : produit['dci'],
                            "dosage": produit['dosage'],
                            "galenique": produit['galenique'],
                            "fabricant": produit['fabricant'],
                            "conditionnement": produit['conditionnement']} }

    db['produits'].update_one(myquery, newvalues) 
    return 'success'




def medicament_ls():  # noqa: E501
    return json.loads(dumps(db['produits'].find()))  # noqa: E501
    


def pharmacie_add(pharmacie):  # noqa: E501
  
    if connexion.request.is_json:
        pharmacie = Pharmacie.from_dict(connexion.request.get_json())  # noqa: E501
    db['pharmacies'].insert_one(pharmacie)
    return 'success'


def pharmacie_del(pharmacie_id):  # noqa: E501
    db['pharmacies'].delete_one({ "_id": ObjectId(pharmacie_id) })
    return 'success'





def pharmacie_ls():  # noqa: E501
   return json.loads(dumps(db['pharmacies'].find())) 
    





def pharmacie_update(pharmacie_id, pharmacie):  # noqa: E501
  
    if connexion.request.is_json:
        pharmacie = Pharmacie.from_dict(connexion.request.get_json())  # noqa: E501
    myquery = { "_id": ObjectId(pharmacie_id) }
    newvalues = { "$set": { "nom": pharmacie['nom'],
                            "ifu" : pharmacie['ifu'],
                            "tel": pharmacie['tel'],
                            "localisation": pharmacie['localisation']
                            } }

    db['pharmacies'].update_one(myquery, newvalues)
    return 'success'



def change_dispo(pharmacie, medicament, disponibilite ):  # noqa: E501

    db['produits'].update_one(  { "_id": ObjectId(medicament), "pharmacies._id": ObjectId(pharmacie) }, { "$set": { "pharmacies.$.disponible" : disponibilite} })

    return json.loads(dumps(db['produits'].find({ "_id": ObjectId(medicament)})))


def medicament_proposition(medicament):  # noqa: E501
    return json.loads(dumps(db['produits'].find({ "nom": { "$regex": '.*'+traitement(medicament)+'.*', "$options" :'i' } })))