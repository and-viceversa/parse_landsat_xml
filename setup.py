
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mtl_to_xml",
    version="0.2.5",
    packages=find_packages(),
    scripts=['mtl_to_xml.py'],
    author="AdamR",
    author_email="25871157+and-viceversa@users.noreply.github.com",
    description="Convert Landsat MTL metadata to XML.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/and-viceversa/mtl_to_xml",
    license=open('LICENSE').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Unlicense',
        'Topic :: Landsat :: data conversion']
)
