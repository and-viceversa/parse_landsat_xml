## Parse Bulk Landsat Metadata

USGS conveniently hosts a bulk metadata service located [here](https://www.usgs.gov/land-resources/nli/landsat/bulk-metadata-service).

Less conveniently, you get a large metadata file with no way to parse it.

This project implements a CLI to parse the bulk metadata files and output .xml
based on the user's search parameters. It also creates a .txt file with each Landsat sceneID
for use with [EarthExplorer](https://earthexplorer.usgs.gov/). Users can search by date-range, cloud cover percentage, and 
whether a lat/lon point is within the scene.


A USGS EROS [account](https://ers.cr.usgs.gov/login/) is required if you want to download.

## Usage

Flags:

```
-f filename 
-d YYYYMMDD_YYYYMMDD inclusive date range 
-c max acceptable cloud cover in scene
-b lat,lon boundary. the search only supports point based boundary.
```

Example Usage:

```commandline
cd /filepath/to/bulkmetadata
parse_landsat_xml.py -f LANDSAT_8_C1.xml -d 20180101_20190101 -c 50 -b 12.114993-86.236176
download_from_scene_list.py
```
