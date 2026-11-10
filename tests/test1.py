"""Pruebas reproducibles para Arbol_etapas.py con oráculo independiente (CSV crudo).
Ejecutar desde la carpeta que contiene BDPoli.csv: python pruebas_revisor1_observacion3.py
"""
import csv, sys, unittest
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import os
os.chdir(ROOT)
from Arbol import procesar_respuestas

with (ROOT/'BDPoli.csv').open(encoding='utf-8-sig',newline='') as f:
    RECORDS=list(csv.DictReader(f))
ESTADOS=['AGUASCALIENTES','BAJACALIFORNIA','BAJACALIFORNIASUR','CAMPECHE','CHIAPAS','CHIHUAHUA','CIUDADMEXICO','COAHUILA','COLIMA','DURANGO','GUANAJUATO','GUERRERO','HIDALGO','JALISCO','ESTADOMEXICO','MICHOACAN','MORELOS','NAYARIT','NUEVOLEON','OAXACA','PUEBLA','QUERETARO','QUINTANAROO','SANLUIS','SINALOA','SONORA','TABASCO','TAMAULIPAS','TLAXCALA','VERACRUZ','YUCATAN','ZACATECAS']
SUELOS=['ARCILLOSO','ARENOSO','FRANCO','FRANCOARENOSO','LIMOSO','PANTANOSO','PEDREGOSO']
BASE=dict(estado=16,amin=0.5,temp=20,heladas=2,riego=2,sol=1,suelo=2,CMO=2,phCond=2,forma=1,fruta=2,hoja=1,uso=2,cflor=0,altura=1,velocidad=2)
def ref_filtrar(r):
    """Implementación independiente: trabaja con etiquetas originales, no usa pandas ni mapeos del algoritmo."""
    def incluye(celda,valor):
        return valor in [x.strip().upper().replace(' ','') for x in celda.split('/')]
    out=[]
    for x in RECORDS:
        if not incluye(x['ESTADO'],ESTADOS[r['estado']-1]):continue
        if not float(x['AMIN'])<=r['amin']<=float(x['AMAX']):continue
        if not float(x['TMIN'])<=r['temp']<=float(x['TMAX']):continue
        if x['HELADAS']!={1:'SI',2:'NO',3:'LIGERA'}[r['heladas']]:continue
        if x['RIEGO']!={1:'ABUNDANTE',2:'MODERADO',3:'BAJO'}[r['riego']]:continue
        if x['INSOLACION']!={1:'SOL',2:'SOMBRA'}[r['sol']]:continue
        if not incluye(x['SUELO'],SUELOS[r['suelo']-1]):continue
        if x['CMO']!={1:'RICO',2:'MODERADO',3:'POBRE'}[r['CMO']]:continue
        if r['phCond']==1 and not float(x['PHMIN'])<=r['ph']<=float(x['PHMAX']):continue
        out.append(x)
    return out

def preferencias(x,r):
    def incluye(celda,valor):return valor in [v.strip().upper() for v in celda.split('/')]
    forma={1:'ARBUSTIVO',2:'HERBACEA',3:'ARBOREO'}[r['forma']]
    return (x['FORMA']==forma and x['FRUTAS']=={1:'SI',2:'NO'}[r['fruta']] and x['HOJA']=={1:'PERENNE',2:'ANUAL'}[r['hoja']] and incluye(x['USO'],{1:'MEDICINAL',2:'ORNAMENTAL',3:'FORRAJE'}[r['uso']]) and float(x['ALTMIN'])<=r['altura']<=float(x['ALTMAX']) and x['VELOCIDAD']=={1:'LENTO',2:'MODERADO',3:'RAPIDO'}[r['velocidad']] and (forma!='HERBACEA' or incluye(x['HERBACEA'],{1:'TREPADORA',2:'ENREDADERA',3:'POSTRADA'}[r['herbacea']])) and (r['cflor']==0 or incluye(x['CFLOR'],['','AMARILLO','AZUL','BLANCO','LILA','MORADO','NARANJA','ROJO','ROSA','VERDE'][r['cflor']])))

def entrada_de_registro(x):
    estado=next((i+1 for i,e in enumerate(ESTADOS) if e in [v.strip().replace(' ','') for v in x['ESTADO'].split('/')]),16)
    suelo=next((i+1 for i,s in enumerate(SUELOS) if s in x['SUELO'].split('/')),1)
    r=dict(BASE,estado=estado,amin=(float(x['AMIN'])+float(x['AMAX']))/2,temp=(float(x['TMIN'])+float(x['TMAX']))/2,heladas={'SI':1,'NO':2,'LIGERA':3}[x['HELADAS']],riego={'ABUNDANTE':1,'MODERADO':2,'BAJO':3}[x['RIEGO']],sol={'SOL':1,'SOMBRA':2}[x['INSOLACION']],suelo=suelo,CMO={'RICO':1,'MODERADO':2,'POBRE':3}[x['CMO']])
    return r

# Buscar casos reales, sin introducir datos artificiales ni modificar la BD.
CANDIDATOS=[entrada_de_registro(x) for x in RECORDS]
CANDIDATOS += [dict(r,estado=16) for r in CANDIDATOS]
CASOS={}
for r in CANDIDATOS:
    n=len(ref_filtrar(r))
    if n==1 and 'una' not in CASOS:CASOS['una']=r
    if n>1 and 'varias' not in CASOS:CASOS['varias']=r
    if len(CASOS)==2:break
CASOS['ninguna']=dict(BASE,amin=1000000)

class Pruebas(unittest.TestCase):
    def verificar(self,r):
        resultado=procesar_respuestas(r)
        referencia=ref_filtrar(r)
        preferidas=[x['ESPECIE'] for x in referencia if preferencias(x,r)]
        alternativas=[x['ESPECIE'] for x in referencia if not preferencias(x,r)]
        self.assertCountEqual([x['especie'] for x in resultado['preferidas']],preferidas)
        self.assertCountEqual([x['especie'] for x in resultado['alternativas']],alternativas)
        self.assertEqual(resultado['total'],len(referencia))
        self.assertEqual(len(resultado['preferidas'])+len(resultado['alternativas']),resultado['total'])
        return resultado
    def test_01_una_especie(self):
        self.assertIn('una',CASOS,'No se encontró un caso de una especie en los datos actuales')
        self.assertEqual(self.verificar(CASOS['una'])['total'],1)
    def test_02_varias_especies(self):
        self.assertIn('varias',CASOS,'No se encontró un caso de varias especies en los datos actuales')
        self.assertGreater(self.verificar(CASOS['varias'])['total'],1)
    def test_03_ninguna_especie(self):
        self.assertEqual(self.verificar(CASOS['ninguna'])['total'],0)
    def test_04_preferencias_no_eliminan_compatibles(self):
        r=dict(CASOS['varias'],cflor=7,forma=3,fruta=1,hoja=2,uso=3,altura=100,velocidad=1)
        self.assertEqual(self.verificar(r)['total'],len(ref_filtrar(CASOS['varias'])))
    def test_05_ph_opcional(self):
        r=dict(CASOS['varias'],phCond=2)
        r.pop('ph',None)
        self.verificar(r)
    def test_06_entrada_ausente(self):
        r=dict(BASE);r.pop('estado')
        with self.assertRaises(ValueError):procesar_respuestas(r)
    def test_07_entrada_no_numerica(self):
        with self.assertRaises(ValueError):procesar_respuestas(dict(BASE,temp='invalido'))
    def test_08_fuera_de_rango(self):
        with self.assertRaises(ValueError):procesar_respuestas(dict(BASE,estado=33))
    def test_09_no_json(self):
        with self.assertRaises(ValueError):procesar_respuestas(None)
    def test_10_nan(self):
        with self.assertRaises(ValueError):procesar_respuestas(dict(BASE,temp=float('nan')))
    def test_11_casos_adicionales_contra_csv(self):
        for r in CANDIDATOS[:40]:
            with self.subTest(estado=r['estado'],amin=r['amin'],temp=r['temp']):self.verificar(r)

if __name__=='__main__':
    print('BASE CSV:',len(RECORDS),'especies')
    for k,r in CASOS.items():
        print('CASO',k,'entradas=',r,'esperadas=',[x['ESPECIE'] for x in ref_filtrar(r)])
    unittest.main(verbosity=2)
