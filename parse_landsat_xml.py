#!/usr/bin/env python
# Python 3.7

"""
Background:

    USGS conveniently hosts a bulk metadata service located at:
    https://www.usgs.gov/land-resources/nli/landsat/bulk-metadata-service

    Less conveniently, you get a large metadata file with no way to parse it.

    This project implements a CLI to parse the bulk metadata files and output .xml files
    based on the user's search parameters. It also creates a .txt file with each Landsat sceneID
    for use with EarthExplorer.
"""

import fileinput
import os
import argparse
from datetime import datetime
import xml.etree.ElementTree as eTree


def parse_xml_file(args):

    try:

        target_file = args.filename
        dir_file_list = os.listdir(path='.')             # grab all files in the current directory

        if target_file not in dir_file_list:             # make sure the target file exists
            raise FileNotFoundError

        else:
            with fileinput.input(files=target_file) as f:
                '''The Landsat bulk metadata files start with the <searchResponse> tag. We don't want that,
                so we strip out the first line of the document. We want the tags between <metaData> </metaData>.
                Therefore, <metaData> will be the root Element in each case.'''

                root = None                     # initialize root of the ElementTree
                line = f.readline()             # strip out first line of the document

                for line in f:
                    if '</metaData>' in line:               # end of metadata block. send complete xml tree for parsing.
                        xml_tree = eTree.ElementTree(root)  # create tree
                        indent(root)
                        parse_xml_tree(args, xml_tree)      # parse tree
                    elif '</searchResponse>' in line:       # hit the end of the file
                        print('End of File')
                        return
                    elif '<metaData>' in line:              # start of metadata block. make this root.
                        temp = line
                        temp = temp.strip()                 # remove white space
                        temp = temp[1:-1]                   # remove '<' and '>' from <metaData>
                        root = eTree.Element(temp)          # root will be metaData
                    else:
                        sub_element = line                  # all other xml subElements
                        sub_element = sub_element.strip()
                        root.append(eTree.fromstring(sub_element))

    except FileNotFoundError:
        print('Cannot find', args.filename, 'in this directory.')
        quit()
    except Exception as e:                                  # This is not a sophisticated testing block.
        print('Something went wrong.')
        print('The xml file line number is:', f.lineno())
        print('Root node is:', root)
        print(e)


def parse_xml_tree(args, xml_tree):

    # If the user entered a date range, parse dates.
    if args.date_range:
        date_range = args.date_range
        image_date = xml_tree.find('acquisitionDate').text.replace('-', '')

        start_date = datetime(
            int(date_range[0:4]),
            int(date_range[4:6]),
            int(date_range[6:8])
        ).date()

        end_date = datetime(
            int(date_range[9:13]),
            int(date_range[13:15]),
            int(date_range[15:17])
        ).date()

        date = datetime(
            int(image_date[0:4]),
            int(image_date[4:6]),
            int(image_date[6:8])
        ).date()

        if not start_date <= date <= end_date:
            return

    # If the user entered a cloud cover value, parse cloud cover.
    if args.cloud_cover:
        cloud_cover = float(args.cloud_cover)
        scene_cloud_cover = float(xml_tree.find('cloudCover').text)

        if not scene_cloud_cover <= cloud_cover:
            return

    # If the user entered lat/lon point value, check to see if the point is within the scene.
    if args.boundary:
        point = args.boundary
        point = point.split(',')
        lat = float(point[0])
        lon = float(point[1])

        # camel case it is.
        upperLeftCornerLat = float(xml_tree.find('upperLeftCornerLatitude').text)
        upperLeftCornerLon = float(xml_tree.find('upperLeftCornerLongitude').text)
        upperRightCornerLat = float(xml_tree.find('upperRightCornerLatitude').text)
        upperRightCornerLon = float(xml_tree.find('upperRightCornerLongitude').text)
        lowerLeftCornerLat = float(xml_tree.find('lowerLeftCornerLatitude').text)
        lowerLeftCornerLon = float(xml_tree.find('lowerLeftCornerLongitude').text)
        lowerRightCornerLon = float(xml_tree.find('lowerRightCornerLongitude').text)
        lowerRightCornerLat = float(xml_tree.find('lowerRightCornerLatitude').text)

        if not point_is_left_of_line(lowerRightCornerLon, lowerRightCornerLat, upperRightCornerLon,
            upperRightCornerLat, lon, lat):
            return
        if not point_is_left_of_line(upperRightCornerLon, upperRightCornerLat, upperLeftCornerLon,
            upperLeftCornerLat, lon, lat):
            return
        if not point_is_left_of_line(upperLeftCornerLon, upperLeftCornerLat, lowerLeftCornerLon,
            lowerLeftCornerLat, lon, lat):
            return
        if not point_is_left_of_line(lowerLeftCornerLon, lowerLeftCornerLat, lowerRightCornerLon,
            lowerRightCornerLat, lon, lat):
            return

    with open('scene_id_list.txt', 'a') as file:
        scene_line = '{}{}'.format(xml_tree.find('sceneID').text, '\n')
        file.write(scene_line)

    # Add your own additional search logic here.

    # Write .xml for each individual scene that matches search parameters.
    file_name = xml_tree.find('LANDSAT_PRODUCT_ID').text
    xml_tree.write(file_name + '.xml', encoding="utf-8", xml_declaration=True)
    print('Wrote out', xml_tree.find('LANDSAT_PRODUCT_ID').text)


def point_is_left_of_line(x1, y1, x2, y2, xp, yp):
    if (x2 - x1) * (yp - y1) - (xp - x1) * (y2 - y1) >= 0:
        return True


def indent(elem, level=0):
    # Indent method from Fredrik Lundh
    # https://effbot.org/zone/element-lib.htm#prettyprint

    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def parse_args():
    parser = argparse.ArgumentParser(
        description='Input target file and parameters to output individual .xml files and a .txt list of sceneIDs. \n')

    parser.add_argument('-f', '--filename',
                        action='store',
                        required=True,
                        help='The parse_landsat_xml command must be ran in the same'
                             ' directory as the bulk metadata .xml file. \n '
                             'The -f flag is required. Your filename immediately follows the -f flag. \n'
                             'Example: parse_landsat_xml -f your_bulk_xml_file.xml INSERT OTHER PARAMETERS HERE'
                        )

    parser.add_argument('-d', '--date-range',
                        action='store',
                        required=False,
                        help='The -d flag allows you to set an range for when the image was taken. \n'
                             'The date format must be YYYYMMDD. The date format must include year, month, and day. \n'
                             'Example: parse_landsat_xml -f your_bulk_xml_file.xml -d 20180101_20190101 \n'
                        )

    parser.add_argument('-c', '--cloud-cover',
                        action='store',
                        required=False,
                        help='The -c flag allows you to filter for \'less than or equal to\' '
                             'percentage of cloud cover. \n'
                             '-c 10 means that cloud cover values greater than 10 percent will be excluded. \n'
                             'Example: parse_landsat_xml -f your_bulk_xml_file.xml -c 44.44 '
                        )

    parser.add_argument('-b', '--boundary',
                        action='store',
                        required=False,
                        help='The -b flag allows you to specify a lat/lon point and returns all the scenes that'
                             'include the point. \n'
                             'The lat/lon format is comma separated signed degree decimal. \n '
                             'Example: parse_landsat_xml -f your_bulk_xml_file.xml -b 41.878002,-93.097702'
                        )

    args = parser.parse_args()
    print('The target filename is:', args.filename)     # test line
    return args


def main():

    args = parse_args()        # parse command line arguments
    parse_xml_file(args)       # send arguments to file converter
    print('Done!')


if __name__ == '__main__':
    main()
