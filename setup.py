from setuptools import setup, find_packages
from helper.echo import echo, ECHO_COLORS

name = 'aqa-core'
version = '12.07.2021'

setup(
    name=name,
    version=version,
    description='AQA Core',
    long_description='Automation - Quality Assurance - Core',
    long_description_content_type='text/markdown',
    url='https://github.com/remedyproduct/aqa-core',
    author='Ivan Veramyou',
    author_email='ivan.veramyou22@gmail.com',
    licence='unlicense',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'allure-behave>=2.8.40',
        'allure-python-commons>=2.8.40',
        'Appium-Python-Client>=1.1.0',
        'attrs>=20.3.0',
        'beautifulsoup4>=4.9.3',
        'behave>=1.2.6',
        'certifi>=2020.12.5',
        'chardet>=4.0.0',
        'colorama>=0.4.4',
        'configparser>=5.0.2',
        'constants>=0.6.0',
        'crayons>=0.4.0',
        'idna>=2.10',
        'names>=0.3.0',
        'parse>=1.19.0',
        'parse-type>=0.5.2',
        'pluggy>=0.13.1',
        'requests>=2.25.1',
        'selenium>=3.141.0',
        'six>=1.15.0',
        'soupsieve>=2.2.1',
        'urllib3>=1.26.4',
        'webdriver-manager>=3.3.0',
    ],
    python_requires='>=3.7'
)

echo('%s = %s' % (name, version), ECHO_COLORS.FAIL)
