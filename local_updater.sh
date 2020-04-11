#!/usr/bin/env bash

echo $1 >> 'core/data/peru.csv'
/home/nucleus/projects/covid-19/plotter/plotter/bin/python core/local_updater.py
