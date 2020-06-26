#!/bin/bash
cd /Users/karinstaring/Documents/rijkswaterstaat/implementation/scripts/comparison
python3 ./create_MERGEDdatabase.py

ogr2ogr -f "PostgreSQL" PG:"host=localhost user=postgres dbname=mergeddatabase password=1234" -nlt PROMOTE_TO_MULTI "/Users/karinstaring/Documents/rijkswaterstaat/implementation/shapefiles/result_shapefiles/BGT2/bgt_merged.shp" 
ogr2ogr -f "PostgreSQL" PG:"host=localhost user=postgres dbname=mergeddatabase password=1234" -nlt PROMOTE_TO_MULTI "/Users/karinstaring/Documents/rijkswaterstaat/implementation/shapefiles/result_shapefiles/BGT2/dtb_merged.shp" 
ogr2ogr -f "PostgreSQL" PG:"host=localhost user=postgres dbname=mergeddatabase password=1234" -nlt PROMOTE_TO_MULTI "/Users/karinstaring/Documents/rijkswaterstaat/implementation/shapefiles/result_shapefiles/BGT2/union.shp" 

cd /Users/karinstaring/Documents/rijkswaterstaat/implementation/scripts/comparison
python3 ./comparison.py

ogr2ogr -f "ESRI Shapefile" /Users/karinstaring/Documents/rijkswaterstaat/implementation/shapefiles/result_shapefiles/BGT2/bgt_categories.shp PG:"host=localhost user=postgres dbname=mergeddatabase password=1234" -sql "select * from public.bgt_merged"
ogr2ogr -f "ESRI Shapefile" /Users/karinstaring/Documents/rijkswaterstaat/implementation/shapefiles/result_shapefiles/BGT2/dtb_categories.shp PG:"host=localhost user=postgres dbname=mergeddatabase password=1234" -sql "select * from public.dtb_merged"
ogr2ogr -f "ESRI Shapefile" /Users/karinstaring/Documents/rijkswaterstaat/implementation/shapefiles/result_shapefiles/BGT2/union_categories.shp PG:"host=localhost user=postgres dbname=mergeddatabase password=1234" -sql "select * from public.union"