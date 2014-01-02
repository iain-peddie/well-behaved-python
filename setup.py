from distutils.core import setup
from distutils.dir_util import *

try:
    with open('README.txt') as file:
        long_description = file.read()
    copy_tree('src/WellBehavedPython', 'WellBehavedPython')

    setup(
        name = 'WellBehavedPython', 
        packages = ['WellBehavedPython'],
        version = '0.5.0',
        description = 'Testing package with fluent API', 
        long_description = long_description,
        author = 'Iain Peddie', 
        author_email = 'inr314159@hotmail.com', 
        url = 'https://github.com/iain-peddie/well-behaved-python',
        classifiers = [
            'Language :: Python', 
            'Language :: Python :: 3.3',
            'Licence :: OSI Approved :: GNU General Public Licence v3 or later (GPLv3+)',         
            'Development Status :: 4 - Beta', 
            'Environment :: Console ',
            'Intended Audience :: Developers', 
            'Operating System :: OS Independent', 
            'Topic :: Software Development :: Testing']
        )

finally:
    remove_tree('WellBehavedPython')
