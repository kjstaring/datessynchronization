#!/bin/bash
cd /Users/karinstaring/Documents/rijkswaterstaat/implementation/scripts/mapping 
# create databatase with postgis and sfcgal extension in Python
python3 ./create_DTBdatabase.py
# import PIVRI.gdp in PostgreSQL 
ogr2ogr -progress -overwrite -f "PostgreSQL" PG:"host=localhost user=postgres dbname=dtbdatabase password=1234" "/Users/karinstaring/Documents/rijkswaterstaat/implementation/data/PIVRI.gdb"
# data mapping, output: DTB with BGT attributes = converted DTB 
python3 ./mapping_DTBdatabase.py
# delete and rename attributes 
python3 ./change_DTBattributes.py

# AANPASSEN: linestring
#BGT: 'LINESTRING(139678.954 465524.3, 139678.954 469160.693, 142703.805 469160.693, 142703.805 465524.3, 139678.954 465524.3)'
#BGT2: 'LINESTRING(23082 398958, 23082 412612, 50654 412612, 50654 398958, 23082 398958)'
#BGT3: 'LINESTRING(95587 433303, 95587 436371, 100434 436371, 100434 433303, 95587 433303)'
#BGT4: 'LINESTRING(XMIN YMIN, XMIN YMAX, XMAX YMAX, XMAX YMIN, XMIN YMIN)'
cd /Users/karinstaring/Documents/rijkswaterstaat/implementation/shapefiles/dtb_shapesfiles 
for VARIABLE in dtb_bebouwing_vlakken dtb_bekleding_vlakken dtb_grond_vlakken dtb_installatie_vlakken dtb_overige_vlakken dtb_verharding_vlakken dtb_water_vlakken
do
    ogr2ogr -f "ESRI Shapefile" /Users/karinstaring/Documents/rijkswaterstaat/implementation/shapefiles/dtb_shapesfiles/$VARIABLE.shp PG:"host=localhost user=postgres dbname=dtbdatabase password=1234" -sql "select * from $VARIABLE where st_intersects(dtb_geom, st_polygon('LINESTRING(139678.954 465524.3, 139678.954 469160.693, 142703.805 469160.693, 142703.805 465524.3, 139678.954 465524.3)'::geometry, 28992)) and dtb_niveau = 0 and (st_geometrytype(dtb_geom) = 'ST_Polygon' or st_geometrytype(dtb_geom) = 'ST_MultiPolygon' or st_geometrytype(bgt_geom) = 'ST_CurvePolygon')"
done

cd /Users/karinstaring/Documents/rijkswaterstaat/implementation/scripts/mapping 
python3 ./create_BGTdatabase.py

# AANPASSEN:
# BGT, BGT2, BGT3, BGT4 
cd /Users/karinstaring/Documents/rijkswaterstaat/implementation/data/BGT
for f in *.gml; 
do 
    base=${f%.gml} 
    ogr2ogr -progress -overwrite -f "PostgreSQL" PG:"host=localhost user=postgres dbname=bgtdatabase password=1234" ${f} -nln $base 
done

cd /Users/karinstaring/Documents/rijkswaterstaat/implementation/scripts/mapping 
layerlist=`python3 ./change_BGTattributes.py`

cd /Users/karinstaring/Documents/rijkswaterstaat/implementation/shapefiles/bgt_shapesfiles 
for VARIABLE in bgt_begroeidterreindeel bgt_kunstwerkdeel bgt_onbegroeidterreindeel bgt_ondersteunendwaterdeel bgt_ongeclassificeerdobject bgt_functioneelgebied bgt_gebouwinstallatie bgt_ondersteunendwegdeel bgt_overbruggingsdeel bgt_overigbouwwerk bgt_overigescheiding bgt_pand bgt_scheiding bgt_tunneldeel bgt_vegetatieobject bgt_waterdeel bgt_wegdeel bgt_weginrichtingselement            
do
    ogr2ogr -f "ESRI Shapefile" /Users/karinstaring/Documents/rijkswaterstaat/implementation/shapefiles/bgt_shapesfiles/$VARIABLE.shp PG:"host=localhost user=postgres dbname=bgtdatabase password=1234" -sql "select * from $VARIABLE where bgt_niveau = 0 and (st_geometrytype(bgt_geom) = 'ST_Polygon' or st_geometrytype(bgt_geom) = 'ST_MultiPolygon' or st_geometrytype(bgt_geom) = 'ST_CurvePolygon')"
done

