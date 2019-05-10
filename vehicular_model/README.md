OSM vehicular graph generator
=============================

This software uses Open Street Map for deriving NetworkX vehicle connectivity graphs.
Input is GPS coordinate and radius in a city and output is a (random) graph representing inter-vehicle connections.
Vehicles are placed in roads with uniform probability with respect to the number of lanes.


Usage
=====
To download the Open Street Map you need to the "download" function:
```
import osm
osm.download()
```
To generate a random realization of vehicular network, just execute osm.py.

Reference
=========
If you use this generative model, please cite:

Luca Baldesi and Leonardo Maccari and Renato Lo Cigno,"Keep It Fresh: Reducing the Age of Information in V2X Networks", TOP-Cars workshop, 2019
