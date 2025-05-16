# network-project


* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [References](#references)



  
## Overview 
This repository hosts the implementation of a python code useful for analysing how attacks and errors on networks may affect network structure and epidemic spreading. 
The networks under study are: 
+ **Erdos-Renyi (ER)**: Erdos-Renyi network is a type of random graph composed by a set of _N_ nodes which has been randonly linked parwise with a probability _p_; so the degree (number of total links) of each node follows, _k_, follows a Binomial distribution _Bin(N-1, p)_, which tends to a Poisson distribution for large _N_. Roughly speaking, this implies that most of nodes in an ER network have a similar number of connections, and the network has no significant hubs.  
+ **Scale-Free (SF)**: A scale-free network is a network whose degree distribution follows a power law _P(k)∝ k<sup>-γ</sup>_. This means that the large majority of the nodes are poorly connected, while there is a very small fraction, called _hubs_, that are highly connected.
+ **Global Air Transportation**: A real-world network where nodes represent airports, and edges correspond to airlines connecting them. This network displays a scale-free behaviour. The source of the dataset is ['Kaggle'](https://www.kaggle.com/datasets/thedevastator/global-air-transportation-network-mapping-the-wo).

This study examines how a network’s topology influences its resilience when undergoes errors or attacks. 
+ **Errors**: an error corresponds to the remotion of a node randomly chosen among the whole set.
+ **Attacks**: an attack is the remotion of the most connected node of the network.

An attack or an error implies, together with the node, the removal of all its links. 

To understand the impact of errors/attacks on the network structure you can calculate different features that embodies the connectivity of the graph as the nodes removed increase:
+ **_d_**: the diameter measures how topologically near two nodes are; the smaller _d_ is, theshorter the shortest path between them.
+ **_S_**: the size of the giant components detects the disgragation process from one single aggregate into smaller and disconnected subgroups.  
+ **_<_s_>_**: the average size of all the connected components except the largest one: reveals the organization of the fragments into smaller and bigger clusters following fragmentation.
**add image**
- Scale-Free networks rely on a few highly connected hubs, explaining: 
  - Resilience to random errors (removing random nodes barely affects connectivity).
  - Vulnerability to targeted attacks: removing a small fraction of hubs quickly fragments the giant component and collapses overall connectivity.
- Erdős–Rényi networks due to their homogeneous degree distribution:
  - Show a more uniform response to both errors and attacks.
  - Less dependent on any individual node, so fragmentation under targeted attacks occurs more gradually.
-Air Traffic network, records results that align with the characteristics of a Scale-Free topology.

Furthermore, the study incorporates simulations of epidemic spreading using the SIR model to quantify how errors/attacks affect disease transmission dynamics. Through the SIR model, each node/individual within the network can be in one of three stages: Susceptible (S), Infected (I), or Recovered (R). Susceptible nodes can be infected only by the infected nodes they are attached to; once infected, they may recover and acquire immunization. The epidemic ends when all the infected nodes move to the recovered stage. The epidemic dynamics are represented by the infective and recovery curves, which correspond respectively to the count of infected and recovered cases over time (Figure 2).
The reasons that lead network structure to influence epidemic dynamics are researched in the analysis of the epidemic dynamics, as shown in Figure 2:
+ _peak_  
+ _t_peak_
+ _epidemic_duration_
+ _total_infected_

Results show that while SF networks are robust to random errors, they are highly vulnerable to targeted attacks due to their reliance on a few central hubs. Conversely, the homogeneous degree distribution of ER networks makes them less affected by specific attacks or errors 

-In Scale-Free networks, targeted attacks drastically reduce epidemic metrics (duration, total infections, peak infection), while random errors have minimal impact, reflecting the network’s robustness to diffuse disruptions.
-In Erdős–Rényi networks, at high attack intensities they eventually follow the Scale-Free behavior, exhibiting a sharp decline not only in connectivity but also in epidemic measures.
- The real-world air traffic network mirrors the behavior of SF networks, underscoring the importance of hubs in maintaining connectivity. The removal of the largest 10% of airports effectively halts epidemic spread, demonstrating the critical role of key nodes in disease containment.
## Prerequisites

In ['requirements.txt'](https://github.com/mianascimben/network-project/blob/main/requirements.txt) there is a list of all the libraries needed to run the package properly.

## Installation

Python version supported : ![Python version](https://img.shields.io/badge/python-3.8|3.9|3.10|3.11-blue.svg)

1. Clone the 'network-project' repository in from GitHub:
```bash
git clone https://github.com/mianascimben/network-project
```

2. Enter the directory of the cloned package:
```bash
cd network-project
```

3. If necessary install the requirements by using:
```bash
pip install -r requirements.txt
```

4. Run the installation command using ['setup.py'](https://github.com/mianascimben/network-project/blob/main/setup.py). This will install the package and its dependencies in your Python environment:
```bash
python setup.py install
```


## Usage
You can create your pipeline in your Python scripts or run simulations directly via command line.

To run the network-project via command line you should digit ```network_code``` and use the following flags:
```-n -m -f```
To have a list of all flags via commandline digit the following:
```
> python network_code -h
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
python network_code -n SF -m epidemic -f duration - N 50 -steps 25 -num_sim 20 -num_points 15
```
# To be changed 
In the sections ['how-to-guide'](https://github.com/mianascimben/network-project/tree/main/how-to-guide) there is a list of examples that will guide you in recreating the same simulations and analysis showed in the ['report'](https://github.com/mianascimben/network-project/blob/main/report.pdf). In particular, one file is about simulating error/attack on networks and visualising the changes in graph feature; the other one focuses on simulating an epidemic and investigating on how nodes removing affects its spreading through analyzing different epidemic features. 

## References
>1. Albert, R. et al. (2000). "Error and attack tolerance of complex networks". Nature, vol. 406,6794.

>2. Erdős, P. & Rényi, A. (1959). "On random graphs". Publicationes Mathematicae, 6, 290–297.
  
>3. The Devastator. (2020). "Global Air Transportation Network: Mapping the World’s Air Traffic". Kaggle. Available at: Global Air Transportation Network. Accessed: August 18, 2024.
