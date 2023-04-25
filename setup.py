import sys

if not (3, 10) < sys.version_info[:2]:
    sys.exit("""
***** ERROR ***********************************************************
* use python 3.11 or above
***********************************************************************
""")

import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

with open('requirements.txt', 'r') as requirements_file:
    requirements_text = requirements_file.read()

requirements = requirements_text.split()

setuptools.setup(
    name='rss-bundle',
    version='0.0.1',
    description='rss-bundle',
    url='https://github.com/hellodword/rss-bundle',
    author='hellodword',
    author_email='',
    license='MIT',
    entry_points={
        'console_scripts': [
            "rss-bundle = rss_bundle.__main__:main",
        ]
    },
    packages=setuptools.find_packages(),
    zip_safe=False,
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=requirements
)
