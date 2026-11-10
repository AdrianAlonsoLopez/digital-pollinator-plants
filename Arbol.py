import pandas as pd

data = pd.read_csv('./BDPoli.csv') 
"""
def convert_drive_link(link):
    if 'drive.google.com' in link:
        if 'open' in link:
            file_id = link.split('=')[-1]
        else:
            file_id = link.split('/')[-2]
        return f'https://drive.google.com/uc?export=view&id={file_id}'
    return link

data['FOTO'] = data['FOTO'].apply(convert_drive_link)
"""
# Mapeos
forma_map = {'ARBOREO': 1, 'ARBUSTIVO': 2, 'HERBACEA': 3}
hoja_map = {'PERENNE': 1, 'ANUAL': 2}
frutas_map = {'SI': 1, 'NO': 0}
heladas_map = {'SI': 1, 'NO': 0, 'LIGERA': 2}
riego_map = {'BAJO': 1, 'MODERADO': 2, 'ABUNDANTE': 3}
insolacion_map = {'SOL': 1, 'SOMBRA': 2}
velocidad_map = {'LENTO': 1, 'MODERADO': 2, 'RAPIDO': 3}
cmo_map = {'POBRE': 1, 'MODERADO': 2, 'RICO': 3}

estados_map = {
    "AGUASCALIENTES": 1, "BAJACALIFORNIA": 2, "BAJACALIFORNIASUR": 3, "CAMPECHE":4, "CHIAPAS":5,
    "CHIHUAHUA":6, "CIUDADMEXICO":7, "COAHUILA":8, "COLIMA":9, "DURANGO":10, "GUANAJUATO":11,
    "GUERRERO":12, "HIDALGO":13, "JALISCO":14, "ESTADOMEXICO":15, "MICHOACAN":16, "MORELOS":17,
    "NAYARIT":18, "NUEVOLEON":19, "OAXACA":20, "PUEBLA":21, "QUERETARO":22, "QUINTANAROO":23,
    "SANLUIS":24, "SINALOA":25, "SONORA":26, "TABASCO":27, "TAMAULIPAS":28, "TLAXCALA":29,
    "VERACRUZ":30, "YUCATAN":31, "ZACATECAS":32
}

uso_map = {'MEDICINAL':1, 'ORNAMENTAL':2, 'FORRAJE':3}
herbacea_map = {'TREPADORA':1, 'ENREDADERA':2, 'POSTRADA':3}
suelo_map = {'ARCILLOSO':1, 'ARENOSO':2, 'FRANCO':3, 'FRANCOARENOSO':4, 'LIMOSO':5, 'PANTANOSO':6, 'PEDREGOSO':7}
cflor_map = {'AMARILLO':1, 'AZUL':2, 'BLANCO':3, 'LILA':4, 'MORADO':5, 'NARANJA':6, 'ROJO':7, 'ROSA':8, 'VERDE':9}

# Funciones para mapear las columnas

def map_single_value_col(df, col, mapping):
    if col in df.columns:
        df[col] = df[col].map(mapping)

def map_multi_value_col(df, col, mapping, is_estado=False):
    if col in df.columns:
        def map_values(cell):
            if pd.isna(cell):
                return set()
            parts = [p.strip() for p in cell.split('/')]
            codes = set()
            for p in parts:
                if is_estado:
                    key = p.upper().replace(" ", "")
                    if key in estados_map:
                        codes.add(estados_map[key])
                else:
                    # Para USO, CFLOR, HERBACEA, SUELO asumir que p viene tal cual las keys del mapping
                    # Convertir a mayúsculas si es necesario
                    p_upper = p.upper()
                    if p_upper in mapping:
                        codes.add(mapping[p_upper])
            return codes
        df[col] = df[col].apply(map_values)

# Mapeo de columnas con un valor
map_single_value_col(data, 'FORMA', forma_map)
map_single_value_col(data, 'HOJA', hoja_map)
map_single_value_col(data, 'FRUTAS', frutas_map)
map_single_value_col(data, 'HELADAS', heladas_map)
map_single_value_col(data, 'RIEGO', riego_map)
map_single_value_col(data, 'INSOLACION', insolacion_map)
map_single_value_col(data, 'VELOCIDAD', velocidad_map)
map_single_value_col(data, 'CMO', cmo_map)

# Mapeo de columnas con múltiples valores
map_multi_value_col(data, 'ESTADO', estados_map, is_estado=True)
map_multi_value_col(data, 'USO', uso_map)
map_multi_value_col(data, 'CFLOR', cflor_map)
map_multi_value_col(data, 'HERBACEA', herbacea_map)
map_multi_value_col(data, 'SUELO', suelo_map)

#print("Columnas después del preprocesamiento:", data.columns)
#filtered = data.copy()

# Reglas separadas: las ambientales excluyen; las preferencias solo agrupan.
def procesar_respuestas(respuestas: dict) -> dict:
    if not isinstance(respuestas, dict):
        raise ValueError("Las respuestas deben ser un objeto JSON.")

    def numero(campo, minimo=None, maximo=None, entero=False):
        try:
            valor = int(respuestas[campo]) if entero else float(respuestas[campo])
        except (KeyError, TypeError, ValueError, OverflowError):
            raise ValueError(f"Respuesta ausente o inválida: {campo}")
        import math
        if not math.isfinite(valor) or (minimo is not None and valor < minimo) or (maximo is not None and valor > maximo):
            raise ValueError(f"Valor fuera de rango: {campo}")
        return valor

    estado = numero('estado', 1, 32, True)
    area = numero('amin', 0)
    temp = numero('temp')
    heladas = {1: 1, 2: 0, 3: 2}[numero('heladas', 1, 3, True)]
    riego = {1: 3, 2: 2, 3: 1}[numero('riego', 1, 3, True)]
    sol = numero('sol', 1, 2, True)
    suelo = numero('suelo', 1, 7, True)
    cmo = {1: 3, 2: 2, 3: 1}[numero('CMO', 1, 3, True)]
    ph_cond = numero('phCond', 1, 2, True)

    # ETAPA 1: restricciones ambientales y de espacio (sin preferencias ornamentales).
    compatibles = data.copy()
    compatibles = compatibles[compatibles['ESTADO'].map(lambda s: estado in s).astype(bool)]
    compatibles = compatibles[(compatibles['AMIN'] <= area) & (compatibles['AMAX'] >= area)]
    compatibles = compatibles[(compatibles['TMIN'] <= temp) & (compatibles['TMAX'] >= temp)]
    compatibles = compatibles[compatibles['HELADAS'] == heladas]
    compatibles = compatibles[compatibles['RIEGO'] == riego]
    compatibles = compatibles[compatibles['INSOLACION'] == sol]
    compatibles = compatibles[compatibles['SUELO'].map(lambda s: suelo in s).astype(bool)]
    compatibles = compatibles[compatibles['CMO'] == cmo]
    if ph_cond == 1:
        ph = numero('ph', 0, 14)
        compatibles = compatibles[(compatibles['PHMIN'] <= ph) & (compatibles['PHMAX'] >= ph)]

    # ETAPA 2: preferencias. Ninguna de estas condiciones excluye especies ambientales.
    forma = {1: 2, 2: 3, 3: 1}[numero('forma', 1, 3, True)]
    herbacea = numero('herbacea', 1, 3, True) if forma == 3 else None
    fruta = {1: 1, 2: 0}[numero('fruta', 1, 2, True)]
    hoja = numero('hoja', 1, 2, True)
    uso = numero('uso', 1, 3, True)
    color = numero('cflor', 0, 9, True)
    altura = numero('altura', 0)
    velocidad = numero('velocidad', 1, 3, True)

    def coincide(fila):
        condiciones = [
            fila['FORMA'] == forma,
            fila['FRUTAS'] == fruta,
            fila['HOJA'] == hoja,
            uso in fila['USO'],
            fila['ALTMIN'] <= altura <= fila['ALTMAX'],
            fila['VELOCIDAD'] == velocidad,
        ]
        if forma == 3:
            # Los subtipos desconocidos NO se consideran coincidencia de preferencia.
            condiciones.append(herbacea in fila['HERBACEA'])
        if color != 0:
            condiciones.append(color in fila['CFLOR'])
        return all(condiciones)

    preferidas, alternativas = [], []
    for _, fila in compatibles.iterrows():
        registro = {
            'especie': str(fila['ESPECIE']),
            'foto': '' if pd.isna(fila['FOTO']) else str(fila['FOTO']),
        }
        (preferidas if coincide(fila) else alternativas).append(registro)

    return {
        'preferidas': preferidas,
        'alternativas': alternativas,
        'total': len(preferidas) + len(alternativas),
    }
