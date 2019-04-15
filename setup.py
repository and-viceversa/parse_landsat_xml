
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="parse_landsat_xml",
    version="0.1.0",
    packages=find_packages(),
    scripts=['parse_landsat_xml.py', 'download_from_scene_list.py'],
    author="AdamR",
    author_email="25871157+and-viceversa@users.noreply.github.com",
    description="Search bulk Landsat metadata files, and then download the resulting Landsat scenes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/and-viceversa/parse_landsat_xml",
    license=open('LICENSE').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Unlicense',
        'Topic :: Landsat :: data conversion']
)
