import psycopg2
import datetime

def compare_attributess_no_overlap_dtb(bronh):
    if bronh == 'L0002':
        category_value = 'rws_no_dtb'
    else:
        category_value = 'no_dtb'
    return category_value 

def compare_attributes(obj):
    # Is data available [0, 1 and 2]
    further_testing = 'no'
    if obj[0] == None:
        if obj[1] == None:
            category_value = 'no_bgt_dtb'
        else:
            category_value = 'no_bgt'
    else:
        if obj[1] == None:
            if obj[2] == 'L0002':
                category_value = 'rws_no_dtb'
            else:
                category_value = 'no_dtb'
        else:
            category_value = 'dtb_bgt'
            further_testing = 'yes'
    
    # Is geobgt available? [3 and 4]
    if further_testing == 'yes':
        if obj[3] == None:
            further_testing = 'no'
            category_value = 'dtb_bgt_no_layer'
        if obj[4] == None:
            further_testing = 'no'
            category_value = 'dtb_bgt_no_geobgt'

    # Is geobgt the same? [3 and 4]
    if further_testing == 'yes':
        if obj[3].replace('bgt_', '').lower() == obj[4].replace('_v', '').lower():
            category_value = 'same_geobgt'
            further_testing == 'yes'
        else:
            category_value = 'different'
            further_testing = 'no'
    # Is fysiekvoorkomen the same? [5, 6, 7 and 8]
    if further_testing == 'yes':
        fys1_values = ['oever, slootkant', 'watervlakte', 'landhoofd', 'waardeOnbekend', 'transitie']
        fys2_values = ['transitie']
        fys3_values = ['transitie']
        if obj[5] != None: 
            if obj[5] in fys1_values:
                category_value = 'onbekende_waarden'
                further_testing = 'no'
            elif obj[5] != obj[8]:
                category_value = 'different'
                further_testing = 'no'
            else:
                category_value = 'same_fysiekvoorkomen'
                further_testing = 'yes'
        elif obj[6] != None: 
            if obj[6] in fys2_values:
                category_value = 'onbekende_waarden'
                further_testing = 'no'
            elif obj[6] != obj[8]:
                category_value = 'different'
                further_testing = 'no'
            else:
                category_value = 'same_fysiekvoorkomen'
                further_testing = 'yes'
        elif obj[7] != None: 
            if obj[7] in fys3_values:
                category_value = 'onbekende_waarden'
                further_testing = 'no'
            elif obj[7] != obj[8]:
                category_value = 'different'
                further_testing = 'no'
            else:
                category_value = 'same_fysiekvoorkomen'
                further_testing = 'yes'
        else: 
            if obj[8] == None: 
                category_value = 'same_fysiekvoorkomen'
                further_testing = 'yes'
            else:
                category_value = 'different'
                further_testing = 'no'
    
    # Is plustype the same? [9 and 10]
    if further_testing == 'yes':
        plus_values = ['transitie', 'niet-bgt']
        if obj[9] != None and obj[10] != None:
            if obj[9] in plus_values:
                category_value = 'onbekende_waarden'
                further_testing = 'no'

            elif obj[9] == obj[10]:
                category_value = 'same_plus'
                further_testing = 'yes'
            else:
                category_value = 'different'
                further_testing = 'no'

        elif obj[9] == None and obj[10] == None:
            category_value = 'same_plus'
            further_testing ='yes'
        else:
            category_value = 'different'
            further_testing = 'no'
    
    # Is function the same? [11 and 12]
    if further_testing == 'yes':
        func_values = ['ruiterpad', 'voetgangersgebied', 'overweg', 'transitie', 'niet-bgt']
        if obj[11] != None and obj[12] != None:
            if obj[11] in func_values:
                category_value = 'onbekende_waarden'
            elif obj[11] == obj[12]:
                category_value = 'same'
            else:
                category_value = 'different'
        elif obj[11] == None and obj[12] == None:
            category_value = 'same'
        else:
            category_value = 'different'
    return category_value 

def compare_dates(obj):
    layers_used_for_comparison = ['dtb_bgt_no_layer', 'dtb_bgt_no_geobgt', 'different']
    if obj[0] in layers_used_for_comparison: 
        # select lv_formal 
        if obj[2] != None and obj[3] != None:
            # convert dates to be usefull 
            lv_unfinished = obj[2].split('T')[0]
            lv = lv_unfinished.split('-')
            formal_unfinished = obj[3].split('T')[0]
            formal = formal_unfinished.split('-')
            lv_date = datetime.date(int(lv[0]), int(lv[1]), int(lv[2]))
            formal_date = datetime.date(int(formal[0]), int(formal[1]), int(formal[2]))
            # formal_date = more accurate
            if lv_date < formal_date: 
                lv_formal = formal_date
            # lv_date = more accurate 
            elif lv_date > formal_date: 
                lv_formal = lv_date
            else:
                lv_formal = lv_date
        elif obj[2] != None:
            lv_formal = obj[2]
        elif obj[3] != None:
            lv_formal = obj[3]
        else:
            synchronization_value = 'not_possible'

        # checker presence of bgt_reality [1], dtb_collection [5] and dtb_mutation [4]
        if obj[1] == None or obj[4] == None or obj[5] == None: 
            synchronization_value = 'not_possible'
        else:
            # bgt: lv_formal is more accurate than the object in reality
            bgt_datum1 = obj[1].split('-')
            bgt_reality = datetime.date(int(bgt_datum1[0]), int(bgt_datum1[1]), int(bgt_datum1[2]))
            if lv_date < bgt_reality:
                synchronization_value = 'not_possible'
                
            else:
                dtb_mutation = obj[4]
                dtb_collection = obj[5]
                if dtb_mutation < dtb_collection:
                    synchronization_value = 'not_possible'
                else:
                    cdiff = bgt_reality - dtb_collection
                    collection_diff = abs(cdiff.days)
                    # same object
                    if bgt_reality == dtb_collection or collection_diff < 180:
                        mdiff = lv_formal - dtb_mutation
                        mutation_diff = abs(mdiff.days)
                        if lv_formal == dtb_mutation or mutation_diff < 180:
                            synchronization_value = 'same_object_same_mutation'
                        else:
                            if lv_formal < dtb_mutation:
                                synchronization_value = 'dtb_mutation_more_accurate'
                            else:
                                synchronization_value = 'bgt_mutation_more accurate'
                    # different object 
                    else:
                        if bgt_reality < dtb_collection: 
                            synchronization_value = 'dtb_object_more_accurate'
                        else: 
                            synchronization_value = 'bgt_object_more_accurate' 
        
    # untill here: layers_used_for_comparison
    elif obj[0] == 'rws_no_dtb':
        synchronization_value = 'rws_no_dtb'
    elif obj[0] == 'same_func':
        synchronization_value = 'same_attributes'
    else:
        synchronization_value = 'None'
    return synchronization_value
    
def use_bgt_geometries():
    bgt_vlakken = """select st_astext(wkb_geometry), bgt_id, bgt_bronh, layer, bgt_fys1, bgt_fys2, bgt_fys3, bgt_plus, bgt_func, ogc_fid from public.bgt_merged"""
    cur.execute(bgt_vlakken)
    bgt = cur.fetchall()

    add_compared = """ALTER TABLE public.bgt_merged ADD COLUMN IF NOT EXISTS category text"""
    cur.execute(add_compared)

    add_compared = """ALTER TABLE public.bgt_merged ADD COLUMN IF NOT EXISTS dtb_datum1 date"""
    cur.execute(add_compared)

    add_compared = """ALTER TABLE public.bgt_merged ADD COLUMN IF NOT EXISTS dtb_datum2 date"""
    cur.execute(add_compared)

    k_bgt = 0 
    bgt_count = len(bgt)

    for obj_bgt in bgt: 

        print("{:.2f}".format((k_bgt / bgt_count) * 100), end='\r')
        k_bgt = k_bgt + 1
        #print(obj_bgt[0])
        overlap = """select dtb_merged.ogc_fid, (st_area(st_intersection(st_setsrid('{}'::geometry, 900914), dtb_merged.wkb_geometry))/st_area(st_setsrid('{}'::geometry, 900914))), dtb_merged.dtb_geobgt from public.dtb_merged where (st_area(st_intersection(st_setsrid('{}'::geometry, 900914), dtb_merged.wkb_geometry))/st_area(st_setsrid('{}'::geometry, 900914))) > 0.6""".format(obj_bgt[0],obj_bgt[0], obj_bgt[0], obj_bgt[0])
        cur.execute(overlap)
        overlappend_vlak = cur.fetchall()

        number_vlakken = len(overlappend_vlak)
        if number_vlakken > 0:
            percentage = 0
            index = 0 
            if number_vlakken > 1:
                for i in range(number_vlakken):
                    print(overlappend_vlak[i])
                    if overlappend_vlak[i][1] > percentage:
                        percentage = overlappend_vlak[i][1]
                        index = i 
            object_dtb = """select dtb_id, dtb_geobgt, dtb_fys, dtb_plus, dtb_func, dtb_datum1, dtb_datum2 from public.dtb_merged where ogc_fid = '{}'""".format(overlappend_vlak[index][0])
            cur.execute(object_dtb)
            obj_dtb = cur.fetchall()[0]
            #dtb_id [0], dtb_geobgt [1], dtb_fys [2], dtb_plus [3], dtb_func [4], dtb_datum1 [5], dtb_datum2 [6]
            #st_astext(wkb_geometry) [0], bgt_id [1], bgt_bronh [2], layer [3], bgt_fys1 [4], bgt_fys2 [5], bgt_fys3 [6], bgt_plus [7], bgt_func [8], ogc_fid [9]
            attrList = [obj_bgt[1], obj_dtb[0], obj_bgt[2], obj_bgt[3], obj_dtb[1], obj_bgt[4], obj_bgt[5], obj_bgt[6], obj_dtb[2], obj_bgt[7], obj_dtb[3], obj_bgt[8], obj_dtb[4]]
            category_value = compare_attributes(attrList)
            sql = """ UPDATE public.bgt_merged SET category = %s WHERE ogc_fid = %s"""
            cur.execute(sql, (category_value, obj_bgt[9]))
            conn.commit()

            sql = """ UPDATE public.bgt_merged SET dtb_datum1 = %s WHERE ogc_fid = %s"""
            cur.execute(sql, (obj_dtb[5], obj_bgt[9]))
            conn.commit()

            sql = """ UPDATE public.bgt_merged SET dtb_datum2 = %s WHERE ogc_fid = %s"""
            cur.execute(sql, (obj_dtb[6], obj_bgt[9]))
            conn.commit()
        else:
            category_value = compare_attributess_no_overlap_dtb(obj_bgt[2])

            sql = """ UPDATE public.bgt_merged SET category = %s WHERE ogc_fid = %s"""
            cur.execute(sql, (category_value, obj_bgt[9]))
            conn.commit()
            # no overlap 
            continue 

def use_dtb_geometries():
    dtb_vlakken = """select st_astext(wkb_geometry), dtb_id, dtb_geobgt, dtb_fys, dtb_plus, dtb_func, ogc_fid from public.dtb_merged"""
    cur.execute(dtb_vlakken)
    dtb = cur.fetchall()

    add_compared = """ALTER TABLE public.dtb_merged ADD COLUMN IF NOT EXISTS category text"""
    cur.execute(add_compared)

    add_compared = """ALTER TABLE public.dtb_merged ADD COLUMN IF NOT EXISTS bgt_datum1 character varying(10)"""
    cur.execute(add_compared)

    add_compared = """ALTER TABLE public.dtb_merged ADD COLUMN IF NOT EXISTS bgt_datum2 character varying(23)"""
    cur.execute(add_compared)

    add_compared = """ALTER TABLE public.dtb_merged ADD COLUMN IF NOT EXISTS bgt_datum3 character varying(23)"""
    cur.execute(add_compared)

    k_dtb = 0 
    dtb_count = len(dtb)

    for obj_dtb in dtb: 

        print("{:.2f}".format((k_dtb / dtb_count) * 100), end='\r')
        k_dtb = k_dtb + 1

        overlap = """select bgt_merged.ogc_fid, (st_area(st_intersection(st_setsrid('{}'::geometry, 900914), bgt_merged.wkb_geometry))/st_area(st_setsrid('{}'::geometry, 900914))), bgt_merged.layer
        from public.bgt_merged where (st_area(st_intersection(st_setsrid('{}'::geometry, 900914), bgt_merged.wkb_geometry))/st_area(st_setsrid('{}'::geometry, 900914))) > 0.6""".format(obj_dtb[0],obj_dtb[0], obj_dtb[0], obj_dtb[0])
        cur.execute(overlap)
        overlappend_vlak = cur.fetchall()

        number_vlakken = len(overlappend_vlak)
        if number_vlakken > 0:
            percentage = 0
            index = 0 
            if number_vlakken > 1:
                for i in range(number_vlakken):
                    print(overlappend_vlak[i])
                    if overlappend_vlak[i][1] > percentage:
                        percentage = overlappend_vlak[i][1]
                        index = i 
            object_bgt = """select bgt_id, bgt_bronh, layer, bgt_fys1, bgt_fys2, bgt_fys3, bgt_plus, bgt_func, bgt_datum1, bgt_datum2, bgt_datum3 from public.bgt_merged where ogc_fid = '{}'""".format(overlappend_vlak[index][0])
            cur.execute(object_bgt)
            obj_bgt = cur.fetchall()[0]
            #st_astext(wkb_geometry) [0], dtb_id [1], dtb_geobgt [2], dtb_fys [3], dtb_plus [4], dtb_func [5], ogc_fid [6]
            #bgt_id [0], bgt_bronh [1], layer [2], bgt_fys1 [3], bgt_fys2 [4], bgt_fys3 [5], bgt_plus [6], bgt_func [7], bgt_datum1 [8], bgt_datum2 [9], bgt_datum3 [10]
            attrList = [obj_bgt[0], obj_dtb[1], obj_bgt[1], obj_bgt[2], obj_dtb[2], obj_bgt[3], obj_bgt[4], obj_bgt[5], obj_dtb[3], obj_bgt[6], obj_dtb[4], obj_bgt[7], obj_dtb[5]]
            category_value = compare_attributes(attrList)
            sql = """ UPDATE public.dtb_merged SET category = %s WHERE ogc_fid = %s"""
            cur.execute(sql, (category_value, obj_dtb[6]))
            conn.commit()

            sql = """ UPDATE public.dtb_merged SET bgt_datum1 = %s WHERE ogc_fid = %s"""
            cur.execute(sql, (obj_bgt[8], obj_dtb[6]))
            conn.commit()

            sql = """ UPDATE public.dtb_merged SET bgt_datum2 = %s WHERE ogc_fid = %s"""
            cur.execute(sql, (obj_bgt[9], obj_dtb[6]))
            conn.commit()

            sql = """ UPDATE public.dtb_merged SET bgt_datum3 = %s WHERE ogc_fid = %s"""
            cur.execute(sql, (obj_bgt[10], obj_dtb[6]))
            conn.commit()

        else:
            #no overlap
            continue 

def union_geometries():
    union_vlakken = """select bgt_id, dtb_id, bgt_bronh, layer, dtb_geobgt, bgt_fys1, bgt_fys2, bgt_fys3, dtb_fys, bgt_plus, dtb_plus, bgt_func, dtb_func, ogc_fid from public.union"""
    cur.execute(union_vlakken)
    union = cur.fetchall()

    add_compared = """ALTER TABLE public.union ADD COLUMN IF NOT EXISTS category text"""
    cur.execute(add_compared)


    k_union = 0 
    union_count = len(union)

    for obj in union: 

        print("{:.2f}".format((k_union / union_count) * 100), end='\r')
        k_union = k_union + 1

        #dtb: st_astext(wkb_geometry) [0], dtb_id [1], dtb_geobgt [2], dtb_fys [3], dtb_plus [4], dtb_func [5], ogc_fid [6]
        #bgt: bgt_id [0], bgt_bronh [1], layer [2], bgt_fys1 [3], bgt_fys2 [4], bgt_fys3 [5], bgt_plus [6], bgt_func [7], bgt_datum1 [8], bgt_datum2 [9], bgt_datum3 [10]
        attrList = [obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7], obj[8], obj[9], obj[10], obj[11], obj[12]]
        category_value = compare_attributes(attrList)
        sql = """ UPDATE public.union SET category = %s WHERE ogc_fid = %s"""
        cur.execute(sql, (category_value, obj[13]))
        conn.commit()
    

                
# create dataset and indexes 
conn = psycopg2.connect("dbname=mergeddatabase user=postgres password=1234")
cur = conn.cursor()

create_bgt_geom_index = "CREATE INDEX bgt_geom_index ON public.bgt_merged USING GIST (wkb_geometry)"
cur.execute(create_bgt_geom_index)
conn.commit()

create_dtb_geom_index = "CREATE INDEX dtb_geom_index ON public.dtb_merged USING GIST (wkb_geometry)"
cur.execute(create_dtb_geom_index)
conn.commit()

#execute functions to add category values 
union_geometries() 

query_vlakken = """select category, bgt_datum1, bgt_datum2, bgt_datum3, dtb_datum1, dtb_datum2, ogc_fid from public.union"""
cur.execute(query_vlakken)
union_vlakken = cur.fetchall()

add_compared = """ALTER TABLE public.union ADD COLUMN IF NOT EXISTS sync text"""
cur.execute(add_compared)

for union_vlak in union_vlakken: 
    synchronization_value = compare_dates(union_vlak)
    sql = """ UPDATE public.union SET sync = %s WHERE ogc_fid = %s"""
    cur.execute(sql, (synchronization_value, union_vlak[6]))
    conn.commit()

use_dtb_geometries() 

query_vlakken = """select category, bgt_datum1, bgt_datum2, bgt_datum3, dtb_datum1, dtb_datum2, ogc_fid from public.dtb_merged"""
cur.execute(query_vlakken)
dtb_vlakken = cur.fetchall()

add_compared = """ALTER TABLE public.dtb_merged ADD COLUMN IF NOT EXISTS sync text"""
cur.execute(add_compared)

for dtb_vlak in dtb_vlakken: 
    synchronization_value = compare_dates(dtb_vlak)
    sql = """ UPDATE public.dtb_merged SET sync = %s WHERE ogc_fid = %s"""
    cur.execute(sql, (synchronization_value, dtb_vlak[6]))
    conn.commit()

use_bgt_geometries()

query_vlakken = """select category, bgt_datum1, bgt_datum2, bgt_datum3, dtb_datum1, dtb_datum2, ogc_fid from public.bgt_merged"""
cur.execute(query_vlakken)
bgt_vlakken = cur.fetchall()

add_compared = """ALTER TABLE public.bgt_merged ADD COLUMN IF NOT EXISTS sync text"""
cur.execute(add_compared)

for bgt_vlak in bgt_vlakken: 
    synchronization_value = compare_dates(bgt_vlak)
    sql = """ UPDATE public.bgt_merged SET sync = %s WHERE ogc_fid = %s"""
    cur.execute(sql, (synchronization_value, bgt_vlak[6]))
    conn.commit()









                
                


