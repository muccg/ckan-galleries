from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-dfmp',
    version=version,
    description="DFMP extension",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Sergey Motornyuk',
    author_email='sergey.motornyuk@linkdigital.com.au',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.dfmp', 'ckanext.s3con'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ckanapi',
        'flickrapi',
        'celery',
        'tweepy',
        'ckanapi',
        'requests',
        'Polygon2',
        'nose',
        'coverage',
        'selenium',
        'boto',
        'pillow',
    ],
    entry_points='''
        [ckan.plugins]
        dfmp=ckanext.dfmp.plugin:DFMPPlugin
        drupal7=ckanext.dfmp.drupal_plugin:DrupalAuthPlugin
        s3con_dfmp=ckanext.s3con.plugin:S3Plugin

        [ckan.celery_task]
        tasks = ckanext.dfmp.celery_import:task_imports
    ''',
)
