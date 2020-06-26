# datessynchronization
synchronization of two related geospatial databases, use case: BGT en DTB

ArcGIS is a commercial \ac{GIS}. In ArcGIS, ESRI FileGDP are used when the attribute table of an individual shapefile exceeds the data size of 2GB. Since ArcGIS is commercial, the open source competitor QGIS is used. QGIS has standard read capabilities for ESRI FileGDPs, but no standard write capabilities. Therefore, additional software has to be installed, which is Osgeo4mac for Mac OSX or Osgeo4W for Windows. This software is needed to handle ESRI FileGDPs in PostgreSQL as well. PostgreSQL is an open-source relational database. Besides PostgreSQL and QGIS, the programming language Python is used to access PostgreSQL. 

Installations used for the insertion of an ESRI FileGDP in PostgreSQL:  
```
brew tap osgeo/osgeo4mac
brew install osgeo-postgresql
brew install osgeo-gdal
brew install osgeo-gdal-filegdb
brew install osgeo-postgis
```
Installed and used python modules: 
```
pip3 install psycopg2
pip3 install pandas 
pip3 install xlrd
````

Folders
- data contains BGT test data and the excel file LookUpTable. The DTB data must be added manually as PIVRI.gdb. 
- styles contains styles for GIS
- shapefiles contains temporary and final results
- mapping contains script to do data mapping
- comparison contains scrip to do attribute and date comparisons 