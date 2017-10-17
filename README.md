# stylesheet-label-finder
Tool for listing all locations where text is displayed on the rendered tiles. Works on mapnik stylesheets and needs Python 3.5.

## Prerequisites
* Python 3.5
* stylesheet extracted in a folder (.mss files and project.mml)

## Function
The tool parses all .mss files in the directory and lists all css selectors which use [text] somewhere. 
This is used by mapnik to display labels on the rendered map. 
In addition it lists the datasources for the selector, if the name does not specifiy what data is displayed. 
This creates a lenghy output which is split in two parts:

#### Locations
The first part of the output contains the location in the `.mss` files, where a selector references to text properties.
Example output: 
```
Checking addressing.mss
  {'#housenumbers'} has text in it
  {'#housenames'} has text in it
  {'#building-text'} has text in it
Checking admin.mss
  {'#admin-text'} has text in it
  {'#nature-reserve-text'} has text in it
Checking aerialways.mss
Checking amenity-points.mss
  {'.text', '.text-low-zoom'} has text in it
Checking buildings.mss
Checking citywalls.mss
Checking ferry-routes.mss
  {'#ferry-routes-text'} has text in it
Checking landcover.mss
  {'#text-line'} has text in it
Checking placenames.mss
  {'#text-line', '.country'} has text in it
  {'.state'} has text in it
  {'#placenames-medium::high-importance'} has text in it
  {'#placenames-medium::medium-importance'} has text in it
  {'#placenames-medium::low-importance'} has text in it
[...]
```

#### Data sources
In the second step the tool uses the `project.mml` to print the sources for these selectors. 
This can be helpful to understand what text is printed there. 
Example output: 
```
#roads-text-name has the following datasource:
{'dbname': 'gis',
 'extent': '-20037508,-20037508,20037508,20037508',
 'geometry_field': 'way',
 'key_field': '',
 'table': '(SELECT way,\n'
          "    CASE WHEN substr(highway, length(highway)-3, 4) = 'link' THEN substr(highway, 0, length(highway)-4) ELSE highway END,\n"
          "    CASE WHEN (tunnel = 'yes' OR tunnel = 'building_passage' OR covered = 'yes') THEN 'yes' ELSE 'no' END AS tunnel,\n"
          "    CASE WHEN construction IN ('service', 'footway', 'cycleway', 'bridleway', 'path', 'track') THEN 'yes' ELSE 'no' END AS int_construction_minor,\n"
          '    name\n'
          '  FROM planet_osm_line\n'
          "  WHERE highway IN ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', \n"
          "                    'tertiary_link', 'residential', 'unclassified', 'road', 'service', 'pedestrian', 'raceway', 'living_street', 'construction')\n"
          '    AND name IS NOT NULL\n'
          ') AS roads_text_name',
 'type': 'postgis'}
[...]
```

## Usage
Pass the path to the folder as first parameter to the script. 
It can be with or without the trailing slash.
It can be relative or absolute.  

Example call:
```Bash
./stylesheet-label-finder openstreetmap-carto-2.41.0/
```

