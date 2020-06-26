import psycopg2
import xlrd 
import networkx as nx
import os

columns = []
def mapping_bgt(layer_name, conn, cur): 
    #2. Drop columns 
    drop_attributes = [
        'ogc_fid', 'inonderzoek', 'namespace', 
        'plus_status', 'begroeidterreindeeloptalud', 'kruinlijnbegroeidterreindeel',
        'bgt_status', 'plus_fysiekvoorkomen', 'onbegroeidterreindeeloptalud',
        'plus_functieondersteunendwegdeel', 'plus_fysiekvoorkomenondersteunendwegdeel',
        'kruinlijnondersteunendwegdeel', 'identificatiebagopr', 'tekst', 'hoek', 
        'hoortbijtypeoverbrugging', 'identificatiebagpnd', 'identificatiebagvbolaagstehuisnummer', 
        'identificatiebagvbohoogstehuisnummer', 'kruinlijnwegdeel', 'wegdeeloptalud', 
        'plus_fysiekvoorkomenwegdeel', 'plus_functiewegdeel', 'overbruggingisbeweegbaar', 
        'ondersteunendwegdeeloptalud', 'kruinlijnonbegroeidterreindeel', 'plus_type']

    for attribute in drop_attributes:
        drop_column = """ALTER TABLE {} DROP COLUMN IF EXISTS {}""".format(layer_name, attribute)
        cur.execute(drop_column)
        conn.commit()

    columns_in_layer = []
    layers = """SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = '{}'""".format(layer_name)
    cur.execute(layers)
    layers = cur.fetchall()
    for layer in layers:
        columns_in_layer.append(layer[0])
        if layer[0] not in columns:
            columns.append(layer[0])
    
    #3. Alter columns      
    alter_attributes = [
        'gml_id', 'relatievehoogteligging', 'creationdate', 
        'lv_publicatiedatum', 'tijdstipregistratie', 'lokaalid', 
        'terminationdate', 'eindregistratie', 'bronhouder', 
        'wkb_geometry', 'bgt_type', 'class', 
        'bgt_fysiekvoorkomen', 'surfacematerial',  'function', 
        ]
    #dtb_geobgt later added as layer 
    
    renamed_attributes = [
        'bgt_id', 'bgt_niveau', 'bgt_datum1', 
        'bgt_datum2', 'bgt_datum3', 'bgt_lokaal',
        'bgt_datum4', 'bgt_datum5', 'bgt_bronh',
        'bgt_geom', 'bgt_plus', 'bgt_fys1', 
        'bgt_fys2','bgt_fys3','bgt_func']
    
    for i, attribute in enumerate(alter_attributes, 0):
        if attribute not in columns_in_layer:
            continue
        elif attribute == renamed_attributes[i]:
            continue 
        else: 
            alter_column = """ALTER TABLE {} RENAME COLUMN {} TO {}""".format(layer_name, attribute, renamed_attributes[i])
            cur.execute(alter_column)
            conn.commit()
    
def main():
    #1. Connect to BGT database 
    conn = psycopg2.connect("dbname= bgtdatabase user=postgres password=1234")
    cur = conn.cursor()

    layers = ['bgt_begroeidterreindeel', 'bgt_functioneelgebied', 'bgt_gebouwinstallatie',
    'bgt_kunstwerkdeel','bgt_onbegroeidterreindeel', 'bgt_ondersteunendwaterdeel', 
    'bgt_ondersteunendwegdeel','bgt_ongeclassificeerdobject', 'bgt_overbruggingsdeel', 
    'bgt_overigbouwwerk', 'bgt_overigescheiding', 'bgt_pand', 
    'bgt_scheiding', 'bgt_tunneldeel', 'bgt_vegetatieobject', 
    'bgt_waterdeel', 'bgt_wegdeel', 'bgt_weginrichtingselement']

    tables_in_bgt = ''
    cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    for table in cur.fetchall():
        if table[0] in layers: 
            tables_in_bgt = tables_in_bgt + str(table[0]) + ' '
            try: 
                mapping_bgt(table[0], conn, cur)
            except:
                print('layer not available in BGT: ' + str(table[0]))
                pass 
    conn.close() 
    print(tables_in_bgt)
    return tables_in_bgt

main()
