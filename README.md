IFloodS - Information Flooding Simulator
========================================

IFloodS simulates packet/information spreading in a network.
Currently it comes with three distribution models:

* tree
* epidemics with uniform probabilities
* epidemics with reception-equal strategy [1] 

IFloodS can be used to compare delay and age of information results following different distribution paradigms for a given set of network topologies.
IFloodS takes as input the network topologies in the _topos/_ folder, performs the simulations and produce a CSV result file on delay reception.

Usage
=====
To compute delays:
```
./ifloods.py
```
To preprocess age of information
```
./analyse_aoi.py
```
Data can be then plotted using the script in the _img_ folder.


Graph dataset
=============

IFloodS uses by default topologies in the _topos/_ folder. You may use any other topologies, provided they come in __.edges__ format.
In the vehicular_model folder there is a generative model for urban traffic networks, refer to the inner README file for further information.

Reference
=========
If you use this software, please cite:

[1] Baldesi, Luca, Leonardo Maccari, and Renato Lo Cigno. “On the Properties of Infective Flooding in Low-Duty-Cycle Networks.” In 2019 15th Annual Conference on Wireless On-Demand Network Systems and Services (WONS), 2019.

[2] Baldesi, Luca, Leonardo Maccari and Renato Lo Cigno. "Keep It Fresh: Reducing the Age of Information in V2X Networks", In TOP-Cars workshop, 2019.
