# -*- coding: utf-8 -*-
import pandas as pd
import ipyleaflet
from ipyleaflet import basemaps
from adresypomoc import lokaciaUlica
from numpy import mean

def nacitajPsov():
    Psi_ukec = pd.read_json('Psi_Presov.json',orient='records') 
    Psi = Psi_ukec[['Ulica', 'Orient._č.','Plemeno']].rename(columns={'Orient._č.':'Číslo'})
    Psi = Psi[Psi['Ulica'] != '']
    NP = Psi_ukec[Psi_ukec["Nebezpečný_pes"] == "Áno"]
    NP = NP[['Ulica', 'Orient._č.','Plemeno']].rename(columns={'Orient._č.':'Číslo'})
    return Psi, NP

def psiNaUlici(Psi,ulica):
    C,Polohy = lokaciaUlica('Prešov',ulica)
    Lat, Lon = zip(*Polohy)
    Lat_s,Lon_s = mean(Lat),mean(Lon)
    ul_map = ipyleaflet.Map(basemap=basemaps.OpenStreetMap.Mapnik, center=(Lat_s,Lon_s),zoom=17)
    PsieDomy = Psi[Psi['Ulica'] == ulica]
    Pv = PsieDomy['Číslo'].values
    Pv = [p.strip() for p in Pv]
    Pp = list(PsieDomy['Plemeno'].values)
    Pdata = dict(zip(Pv,Pp))
    for p,c in zip(Polohy,C):
        if c in Pdata:                  
            ul_map.add_layer(ipyleaflet.CircleMarker(location=p,radius=6,color='red',fill_color='green',fill=True,opacity=0.3))
    return ul_map, Pv


def psiPlemeno(plemeno):
    pass
