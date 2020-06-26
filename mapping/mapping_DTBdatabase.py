import psycopg2
import xlrd 
import networkx as nx
import os

# AANPASSEN: linestring
# BGT: 'LINESTRING(139678.954 465524.3, 139678.954 469160.693, 142703.805 469160.693, 142703.805 465524.3, 139678.954 465524.3)'
# BGT2: 'LINESTRING(23082 398958, 23082 412612, 50654 412612, 50654 398958, 23082 398958)'
# BGT3: 'LINESTRING(95587 433303, 95587 436371, 100434 436371, 100434 433303, 95587 433303)'

def mapping_dtb(layer_name): 
    #1. Import the excel file, the LookupTable
    wb = xlrd.open_workbook('/Users/karinstaring/Documents/rijkswaterstaat/implementation/data/BGTLookUp.xlsx')
    sheet = wb.sheet_by_index(0) 
    num_rows = len(sheet.col_values(0))

    #2. Add columns to the DTB objects to insert BGT attributes 
    vlakken = ["""ALTER TABLE {} ADD COLUMN IF NOT EXISTS dtb_geobgt character varying(80)""".format(layer_name), 
                """ALTER TABLE {} ADD COLUMN IF NOT EXISTS dtb_plus character varying(80)""".format(layer_name), 
                """ALTER TABLE {} ADD COLUMN IF NOT EXISTS dtb_fys character varying(80)""".format(layer_name), 
                """ALTER TABLE {} ADD COLUMN IF NOT EXISTS dtb_func character varying(80)""".format(layer_name), 
                """ALTER TABLE {} ADD COLUMN IF NOT EXISTS dtb_sub character varying(80)""".format(layer_name)]
    for add_column in vlakken: 
        cur.execute(add_column)

    #3. Select the DTB data that intersects the area of interest (Linestring, reference system = 28992)
    query_vlakken = """select * from {} where st_intersects(shape, st_polygon('LINESTRING(139678.954 465524.3, 139678.954 469160.693, 142703.805 469160.693, 142703.805 465524.3, 139678.954 465524.3)'::geometry, 28992))""".format(layer_name)
    cur.execute(query_vlakken)
    vlakken_in_area = cur.fetchall()

    k = 0 
    obj_count = len(vlakken_in_area)

    #4. Iterate over all objects in the area of interest 
    for dtb_object in vlakken_in_area: 
        
        print("{:.2f}".format((k / obj_count) * 100), end='\r')
        k = k + 1

        rowList = []
        # A unique row has to be selected to the data mapping
        for i in range(num_rows): 
            row = sheet.row_values(i)
            if dtb_object[17] == row[1]: # compare type
                if row[3] == '':
                    row[3] = None
                if dtb_object[18] == row[3]: # compare function
                    if dtb_object[3] == row[9]: # compare niveau
                        rowList.append(row)
        
        if len(rowList) == 0:
            print('length rowList is 0: ' + str(dtb_object))       
        elif len(rowList) > 1:
            print('length rowList is more than 1: ' + str(dtb_object) + ' and the rowList: ' + str(rowList))  
        else: 
            # add BGT attributes to the DTB object 
            sql = """ UPDATE {} SET dtb_geobgt = %s, dtb_plus = %s, dtb_fys = %s, dtb_func = %s, dtb_sub = %s WHERE dtb_id = %s""".format(layer_name)
            cur.execute(sql, (rowList[0][10], rowList[0][11], rowList[0][12], rowList[0][13], rowList[0][14], dtb_object[1]))
            conn.commit()
    
#1. DTB mapped to BGT
conn = psycopg2.connect("host=localhost dbname= dtbdatabase user=postgres password=1234")
cur = conn.cursor()

layers = ['dtb_bebouwing_vlakken', 'dtb_bekleding_vlakken', 
'dtb_grond_vlakken', 'dtb_installatie_vlakken', 'dtb_overige_vlakken', 
'dtb_verharding_vlakken', 'dtb_water_vlakken']

#2. Iterate over all layers 
for layer_name in layers:
    print(layer_name)
    try: 
        mapping_dtb(layer_name)
    except:
        print('layer not available in DTB: ' + str(layer_name))
        pass 

print('finished mapping')
conn.close() 
