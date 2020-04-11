#!/usr/bin/env bash

echo $1 >> 'core/data/peru.csv'
$(pwd)/plotter/bin/python core/local_updater.py
