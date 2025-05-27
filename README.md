# network-project


* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [References](#references)



  
## Overview 
This repository hosts the implementation of a python code useful for analysing how attacks and errors on networks may affect network structure and epidemic spreading. One use of this repository could be to examine how a network’s topology influences its resilience when undergoes errors or attacks. 
Here I give a brief overview of the topic; for a detailed expanation of the methods and the results obtained see ['report'][url](https://github.com/mianascimben/network_project/blob/main/report.pdf).

Here the values of the constants used to get the plots shown in the README and in the report.
| Command | Value |
| --- | --- |
| `-N` | 1000 |
| `-p` | 0.004 |
| `-seed` | 102 |
| `-mu` | 0.2 |
| `-nu` | 0.05 |
| `-steps` | 50 |
| `-infected` | 1 |
| `-num_sim` | 100 |
| `-num_points` | 15 |

#### What errors and attacks are?
+ **Errors**: an error corresponds to the remotion of a node randomly chosen among the whole set.
+ **Attacks**: an attack is the remotion of the most connected node of the network.
An attack or an error implies, together with the node, the removal of all its links.

Now, if you think of a network fully connected, the lack of one node doesn't make any difference in the level of network connectivity or in the information spreading: nonetheless that node is missing, there are many other paths the information can go through to spread. On the other hand, think of a network where all the nodes are connected to one central node: if you remove that central node, the network will result in a bunch of isolated nodes which don't communicate.
This is a simple example to understand the impact that the network topology can have when the network undergoes node remotion. 

The networks under study are: 
+ **Erdos-Renyi (ER)**: Erdos-Renyi network is a type of random graph composed by a set of _N_ nodes which has been randonly linked parwise with a probability _p_; so the degree (number of total links) of each node follows, _k_, follows a Binomial distribution _Bin(N-1, p)_, which tends to a Poisson distribution for large _N_. Roughly speaking, this implies that most of nodes in an ER network have a similar number of connections, and the network has no significant hubs.  
+ **Scale-Free (SF)**: A scale-free network is a network whose degree distribution follows a power law _P(k)∝ k<sup>-γ</sup>_. This means that the large majority of the nodes are poorly connected, while there is a very small fraction, called _hubs_, that are highly connected.
+ **Global Air Transportation**: A real-world network where nodes represent airports, and edges correspond to airlines connecting them. This network displays a scale-free behaviour. The source of the dataset is ['Kaggle'](https://www.kaggle.com/datasets/thedevastator/global-air-transportation-network-mapping-the-wo).

To understand the impact of errors/attacks on the network structure you can calculate different features that embodies the connectivity of the graph as the nodes removed increase:
+ **_d_**: the diameter measures how topologically near two nodes are; the smaller _d_ is, theshorter the shortest path between them.
+ **_S_**: the size of the giant components detects the disgragation process from one single aggregate into smaller and disconnected subgroups.  
+ **_<_s_>_**: the average size of all the connected components except the largest one: reveals the organization of the fragments into smaller and bigger clusters following fragmentation.

#### Structural Results: plots

![diameter and fragmentation images](https://github.com/mianascimben/network_project/blob/main/images/graph_analysis_diameter_plot.PNG)
![](https://github.com/mianascimben/network_project/blob/main/images/graph_analysis_S_plot.PNG)

#### Epidemic simulation with SIR model
Furthermore, the study incorporates simulations of epidemic spreading using the SIR model to quantify how errors/attacks affect disease transmission dynamics. Through the SIR model, each node within the network can be in one of three stages: Susceptible (S), Infected (I), or Recovered (R). Susceptible nodes can be infected only by the infected nodes they are attached to; once infected, they may recover and acquire immunization. The epidemic ends when all the infected nodes move to the recovered stage. The epidemic dynamics are represented by the infective and recovery curves, which correspond respectively to the count of infected and recovered cases over time (see next Figure).
The reasons that lead network structure to influence epidemic dynamics are researched in the analysis of these curves, as shown in the following Figure:

![](https://github.com/mianascimben/network_project/blob/main/images/scheme.PNG)

+ **peak**: the maximum number of infected cases during all the epidemic
+ **t_peak**: the time step at which the infection peak is reached
+ **epidemic_duration**: how long the epidemic has lasted 
+ **total_infected**: the total number of infected cases that have been recorded during all the epidemic (even the recovered ones).
#### Epidemic results: plots
![epidemic images](https://github.com/mianascimben/network_project/blob/main/images/epidemic_ER_SF_plot.PNG)

## Prerequisites

In ['requirements.txt'](https://github.com/mianascimben/network-project/blob/main/requirements.txt) there is a list of all the libraries needed to run the package properly.

## Installation

Python version supported : ![Python version](https://img.shields.io/badge/python-3.8|3.9|3.10|3.11-blue.svg)

The following instructions work in the command prompt of Python.

1. Clone the 'network_project' repository from GitHub and enter in its the directory:
```bash
git clone https://github.com/mianascimben/network_project
cd network_project
```
2. If necessary install the requirements by using:
```bash
python -m pip install -r requirements.txt
```
4. Install the package in *editable* mode.
```bash
python -m pip install -e .
```

## Usage
You can create your pipeline in your Python scripts or run simulations directly via command line.

### Command line
To run the network-project via command line you should digit ```network_code``` and use the following flags:
```-n -m -f```
To have a list of all flags via commandline digit the following:
```
> network_code -h
usage: network_code [-h] -n {ER,SF,ER_SF,airports} -m {epidemic,structural} -f FEATURE [-N N] [-p P] [-seed SEED]
                    [-max_rate MAX_RATE] [-mu MU] [-nu NU] [-steps STEPS] [-infected INFECTED] [-num_sim NUM_SIM]
                    [-num_points NUM_POINTS]

Code for analysing how attacks and errors on networks may affect network structure andepidemic spreading.

options:
  -h, --help            show this help message and exit
  -n {ER,SF,ER_SF,airports}
                        Select the type of network to study.
  -m {epidemic,structural}
                        Select the type of simulation to run on the network.
  -f FEATURE            Select the feature to analyze during the simulation. • For '-m epidemic' → peak, t_peak,
                        duration, total_infected • For '-m structural' → connectivity, fragmentation
  -N N                  Number of nodes of the network, default = 100
  -p P                  Probability for ER to connect with other nodes, default = 0.04
  -seed SEED            For reproducibility, default = 102
  -max_rate MAX_RATE    The maximum rate of removable nodes, default = 0.5
  -mu MU                Probability of disease transmission, default = 0.2
  -nu NU                Probability to recover from infection, default = 0.05
  -steps STEPS          Number of steps the epidemics simulation lasts, default = 50
  -infected INFECTED    Number of infected cases at the epidemic starting, default = 1
  -num_sim NUM_SIM      Number of simulations of the epidemic to run to average the epidemic features, default = 100
  -num_points NUM_POINTS
                        Number of data to acquire, default = 15
```
Here an example from the command line:
```
network_code -n SF -m epidemic -f duration -N 50 -steps 25 -num_sim 20 -num_points 15
```

### Python pipeline 
In ['how-to-guide'](https://github.com/mianascimben/network-project/tree/main/how-to-guide) there are two examples that shows how to bulid the pipeline for all the possibile simulations and analysis. In particular, one file focuses on simulating errors and attacks on networks and visualizing the resulting changes in graph structure, while the other simulates an epidemic and analyzes how node removal affects its spread by examining various epidemic characteristics.

## References
>1. Albert, R. et al. (2000). "Error and attack tolerance of complex networks". Nature, vol. 406,6794.

>2. Erdős, P. & Rényi, A. (1959). "On random graphs". Publicationes Mathematicae, 6, 290–297.
  
>3. The Devastator. (2020). "Global Air Transportation Network: Mapping the World’s Air Traffic". Kaggle. Available at: Global Air Transportation Network. Accessed: August 18, 2024.
