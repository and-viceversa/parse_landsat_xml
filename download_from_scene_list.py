#!/usr/bin/env python
# Python 3.7

import argparse
from usgsdownload.usgs import SceneInfo, USGSDownload


def download_landsat_scenes(args):
    try:
        with open('./scene_id_list.txt', 'r') as f:
            for line in f:
                line.strip()
                scene = SceneInfo(line)
                usgs = USGSDownload(scene, user=args.username, password=args.password)
                usgs.download(download_dir='$HOME/landsat_scenes')
    except Exception as e:
        print(e)


def parse_args():
    parser = argparse.ArgumentParser(
        description='A USGS EROS account from https://ers.cr.usgs.gov/login/ is required. \n'
                    'download_from_scene_list.py -u your_EROS_username -p your_EROS_password \n')

    parser.add_argument('-u', '--username',
                        action='store',
                        required=True
                        )

    parser.add_argument('-p', '--password',
                        action='store',
                        required=True
                        )

    args = parser.parse_args()
    return args


def main():

    args = parse_args()
    download_landsat_scenes(args)


if __name__ == '__main__':
    main()
