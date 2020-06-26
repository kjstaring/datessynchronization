import psycopg2
import xlrd 
import networkx as nx
import os

columns = []
def mapping_dtb(layer_name, conn): 
    #2. Drop/delete columns 
    drop_attributes = [
        'pjt_id', 'bvk_id', 'gvk_id', 
        'ivk_id', 'ovk_id', 'vvk_id',
        'wvk_id', 'dtm', 'attribuut_fout_ind', 
        'coordinaat_fout_ind', 'muteerder', 'inwinner',
        'methode_inwinning', 'naam', 'dtb_mutatie_code', 
        'ivri_mutatie_code', 'lengte', 'oppervlakte', 
        'talud', 'shape_length', 'shape_area', 
        'bkv_id', 'gdb_mutatie_code']

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
    print(columns_in_layer)

    #2. Alter/rename columns      
    alter_attributes = [
        'dtb_id', 'niveau', 'datum_mutatie', 
        'datum_inwinning', 
        'type', 'functie', 'bronhouders', 
        'shape', 'geobgt_dtb', 'plust_dtb', 
        'fysiek_dtb', 'func_dtb', 'subt_dtb']

    renamed_attributes = [
        'dtb_id', 'dtb_niveau', 'dtb_datum1', 
        'dtb_datum2', 
        'dtb_type', 'dtb_oldf', 'dtb_bronh',
        'dtb_geom', 'dtb_geobgt', 'dtb_plus', 
        'dtb_fys', 'dtb_func', 'dtb_sub']

    for i, attribute in enumerate(alter_attributes, 0):
        if attribute not in columns_in_layer:
            continue
        elif attribute == renamed_attributes[i]:
            continue 
        else: 
            alter_column = """ALTER TABLE {} RENAME COLUMN {} TO {}""".format(layer_name, attribute, renamed_attributes[i])
            cur.execute(alter_column)
            conn.commit()

#1. Mapping DTB to BGT 
conn = psycopg2.connect("host=localhost dbname= dtbdatabase user=postgres password=1234")
cur = conn.cursor()
print('started changing attributes')

layers = ['dtb_bebouwing_vlakken', 'dtb_bekleding_vlakken', 
'dtb_grond_vlakken', 'dtb_installatie_vlakken', 'dtb_overige_vlakken', 
'dtb_verharding_vlakken', 'dtb_water_vlakken']

for layer_name in layers:
    print(layer_name)
    try: 
        mapping_dtb(layer_name, conn)
    except:
        print('layer not available in DTB: ' + str(layer_name))
        pass 
print(columns)
print('finished changing attributes')
conn.close() 

#dtb_id, niveau as niv_DTB, type as t_DTB, functie as oldfunc, bronhouders as bronh_DTB, shape as shape_DTB, GEOBGT_DTB, PLUST_DTB, FYSIEK_DTB, FUNC_DTB, SUBT_DTB
    
  

