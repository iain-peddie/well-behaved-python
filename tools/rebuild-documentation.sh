#!/usr/bin/env bash

rm -f ../docs/README.html
ghmarkdown -i ../README.md -o ../docs/README.html

