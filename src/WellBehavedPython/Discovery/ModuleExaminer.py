#!/usr/bin/env python3

# Copyright 2013-4 Iain Peddie inr314159@hotmail.com
# 
#    This file is part of WellBehavedPython
#
#    WellBehavedPython is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WellBehavedPython is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WellBehavedPython. If not, see <http://www.gnu.org/licenses/>.

import importlib
import builtins
from types import ModuleType
import pkgutil

class ModuleExaminer:
    """Used to examine modules in the context of a module or package."""
    
    def __init__(self, moduleName):
        """Constructor.

        Inputs
        ------
        moduleName : The name of the module to be examined. This will be imported immediately."""
        self.moduleName = moduleName
        self.module = importlib.import_module(moduleName)

    def listAllClasses(self):
        """lists all the classes defined directly in the module.

        Returns
        -------
        A list of the classes local to this module (i.e. not imported as dependencies
        from other modules."""

        # get the name of all the items in the module. Skip and starting with __
        # This gets rid of most python internal names (which we wish to avoid to
        # ensure that we don't face weird behaviour).
        itemNames= [item for item in dir(self.module) if not item.startswith('__')]
        
        # Now get the list of classes. First convert the item names to metadata types
        things = [self.module.__dict__[itemName] for itemName in itemNames]

        # class objects get a type of type. Everying else will be something different.
        classes = [thing for thing in things if type(thing) == builtins.type]

        # Finally find the classes which are locally defined, that is their __module__
        # attribute has the same name as this module...

        localClasses = [klass for klass in classes if klass.__module__ == self.moduleName]
        
        return localClasses

    def listAllModules(self):
        """lists all the modules defined directly in the package. 
        When constructed from a pakcage name find all the module children only.
        Pacakges are found separetly, in listAllPackages.

        Returns
        -------
        A list of the classes local to this module (i.e. not imported as dependencies
        from other modules."""

        package = self.module.__package__ + ".";
        try:
            return [(package + stuff[1])
                    for stuff in pkgutil.iter_modules(self.module.__path__)]
        except Exception:
            return []

    def listAllPackages(self):
        """lists all the subpackages defined directly in the package. 
        When constructed from a package name find all the module children only.
        Pacakges are found separetly, in listAllPackages.

        Returns
        -------
        A list of the classes local to this module (i.e. not imported as dependencies
        from other modules."""

        from pathlib import Path

        subpackages = []
        baseModule = self.module.__package__ + "."

        if not '__path__' in self.module.__dict__.keys():
            return subpackages

        paths = self.module.__path__
        for path in paths._path:
            nextSubdirs = [x for x in Path(path).iterdir() if x.is_dir()]
            packages = [baseModule + nextSubdir.parts[-1] for nextSubdir in nextSubdirs]
            subpackages.extend(packages)

        return subpackages

        
