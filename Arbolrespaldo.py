import pandas as pd
from IPython.display import display, HTML

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
filtered = data.copy()

#ESTA ES LA FUNCION QUE VA A JALAR EL FLASK
def procesar_respuestas(respuestas: dict) -> str:

#Lifesaver por si se manda un string
    respuestas["amin"] = float(respuestas["amin"])
    respuestas["altura"] = float(respuestas["altura"])
    respuestas["temp"] = float(respuestas["temp"])
    if respuestas["phCond"] == 1:
        respuestas["ph"] = float(respuestas["ph"])

# Iniciamos con todas las plantas
 
    #print("Plantas iniciales:", len(filtered))

    def filtrar_y_mostrar(filtro_func, descripcion):
        """Aplica una función de filtrado a 'filtered', muestra cuántas quedan y si llega a 0, termina."""
        global filtered
        filtered = filtro_func(filtered)
    # print(f"Después de {descripcion}: {len(filtered)}")
        if len(filtered) == 0:
        #    print("\nNo se encontró ninguna planta viable con los criterios seleccionados.")
            return False
        return True

    # Aquí realizaremos las preguntas una por una, filtrando inmediatamente
    #respuestas = [] se va a mandar por POST

    # Pregunta 1: Estado
    estados_list = [
        "AGUASCALIENTES", "BAJACALIFORNIA", "BAJACALIFORNIASUR", "CAMPECHE", "CHIAPAS",
        "CHIHUAHUA", "CIUDADMEXICO", "COAHUILA", "COLIMA", "DURANGO", "GUANAJUATO",
        "GUERRERO", "HIDALGO", "JALISCO", "ESTADOMEXICO", "MICHOACAN", "MORELOS", "NAYARIT",
        "NUEVOLEON", "OAXACA", "PUEBLA", "QUERETARO", "QUINTANAROO", "SANLUIS", "SINALOA",
        "SONORA", "TABASCO", "TAMAULIPAS", "TLAXCALA", "VERACRUZ", "YUCATAN", "ZACATECAS"
    ]

    estado_idx = respuestas["estado"]
    if 1 <= estado_idx <= 32:
        estado_elegido = estados_map[estados_list[estado_idx - 1].upper().replace(" ","")]
        # Filtrar por estado
        if not filtrar_y_mostrar(lambda df: df[df['ESTADO'].apply(lambda s: estado_elegido in s)], f"filtrar por ESTADO={estado_elegido}"):
            raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 2: FORMA
    forma_choice = respuestas["forma"]
    if forma_choice == 1:
        forma_val = 2
    elif forma_choice == 2:
        forma_val = 3
    elif forma_choice == 3:
        forma_val = 1

    if not filtrar_y_mostrar(lambda df: df[df['FORMA'] == forma_val], f"filtrar por FORMA={forma_val}"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Si elige HERBACEA, pregunta el tipo
    if forma_val == 3:
        herbacea_idx = respuestas["herbacea"]
        # HERBACEA es multivalor
        if not filtrar_y_mostrar(lambda df: df[df['HERBACEA'].apply(lambda s: herbacea_idx in s)], f"filtrar por HERBACEA={herbacea_idx}"):
            raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 3: AMIN
    user_AMIN = respuestas["amin"]
    if not filtrar_y_mostrar(lambda df: df[(df['AMIN'] <= user_AMIN) & (df['AMAX'] >= user_AMIN)], "filtrar por AMIN-AMAX"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 4: FRUTAS

    frutas_choice = respuestas["fruta"]
    frutas_val = 1 if frutas_choice == 1 else 0
    if not filtrar_y_mostrar(lambda df: df[df['FRUTAS'] == frutas_val], f"filtrar por FRUTAS={frutas_val}"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 5: HOJA

    hoja_choice = respuestas["hoja"]
    hoja_val = 1 if hoja_choice == 1 else 2
    if not filtrar_y_mostrar(lambda df: df[df['HOJA'] == hoja_val], f"filtrar por HOJA={hoja_val}"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 6: USO

    uso_idx =respuestas["uso"]
    # USO es multivalor
    if not filtrar_y_mostrar(lambda df: df[df['USO'].apply(lambda s: uso_idx in s)], f"filtrar por USO={uso_idx}"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 7: CFLOR

    colores = ["AMARILLO", "AZUL", "BLANCO", "LILA", "MORADO", "NARANJA", "ROJO", "ROSA", "VERDE"]

    color_idx = respuestas["cflor"]
    if color_idx != 0:
        # CFLOR es multivalor
        if not filtrar_y_mostrar(lambda df: df[df['CFLOR'].apply(lambda s: color_idx in s)], f"filtrar por CFLOR={color_idx}"):
            raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 8: ALTURA
    user_ALT = respuestas["altura"]
    if not filtrar_y_mostrar(lambda df: df[(df['ALTMIN'] <= user_ALT) & (df['ALTMAX'] >= user_ALT)], "filtrar por rango ALTURA"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 9: TEMP
    user_T = respuestas["temp"]
    if not filtrar_y_mostrar(lambda df: df[(df['TMIN'] <= user_T) & (df['TMAX'] >= user_T)], "filtrar por TMIN-TMAX"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 10: HELADAS
    heladas_choice = respuestas["heladas"]
    if heladas_choice == 1:
        heladas_val = 1
    elif heladas_choice == 2:
        heladas_val = 0
    elif heladas_choice == 3:
        heladas_val = 2
    if not filtrar_y_mostrar(lambda df: df[df['HELADAS'] == heladas_val], f"filtrar por HELADAS={heladas_val}"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 11: RIEGO
    riego_choice = respuestas["riego"]
    if riego_choice == 1:
        riego_val = 3
    elif riego_choice == 2:
        riego_val = 2
    elif riego_choice == 3:
        riego_val = 1
    if not filtrar_y_mostrar(lambda df: df[df['RIEGO'] == riego_val], f"filtrar por RIEGO={riego_val}"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 12: INSOLACION
    insolacion_choice =  respuestas["sol"]
    if not filtrar_y_mostrar(lambda df: df[df['INSOLACION'] == insolacion_choice], f"filtrar por INSOLACION={insolacion_choice}"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 13: VELOCIDAD
    velocidad_choice =  respuestas["velocidad"]
    if not filtrar_y_mostrar(lambda df: df[df['VELOCIDAD'] == velocidad_choice], f"filtrar por VELOCIDAD={velocidad_choice}"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 14: PH
    ph_conocido =  respuestas["phCond"]
    if ph_conocido == 1:
        user_PH = respuestas["ph"]
        if not filtrar_y_mostrar(lambda df: df[(df['PHMIN'] <= user_PH) & (df['PHMAX'] >= user_PH)], "filtrar por PHMIN-PHMAX"):
            raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 15: SUELO
    tipos_suelo = ["ARCILLOSO", "ARENOSO", "FRANCO", "FRANCOARENOSO", "LIMOSO", "PANTANOSO", "PEDREGOSO"]

    suelo_idx =  respuestas["suelo"]
    # SUELO es multivalor
    if not filtrar_y_mostrar(lambda df: df[df['SUELO'].apply(lambda s: suelo_idx in s)], f"filtrar por SUELO={suelo_idx}"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")


    # Pregunta 16: CMO
    cmo_choice =  respuestas["CMO"]
    if cmo_choice == 1:
        cmo_val = 3
    elif cmo_choice == 2:
        cmo_val = 2
    elif cmo_choice == 3:
        cmo_val = 1
    if not filtrar_y_mostrar(lambda df: df[df['CMO'] == cmo_val], f"filtrar por CMO={cmo_val}"):
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")




    # Si se llega aquí, quedan algunas plantas viables:
    if len(filtered) == 0:
        raise ValueError("No se encontró ninguna planta viable con los criterios seleccionados.")
    return filtered.iloc[0]['FOTO']  # Regresa solo la URL de la imagen   