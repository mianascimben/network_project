
import argparse
import random 
import numpy as np
import matplotlib.pyplot as plt
import time 
import pickle
from simulation_tools.analysis_functions  import *
from simulation_tools.simulation import ToleranceSimulation, EpidemicToleranceSimulation
from simulation_tools.plot_functions import make_plot, make_plot_fragmentation, make_plot_2networks

from constants import EPIDEMICS_FUNCS
def parse_args():
    
    # global softwer information 
    parser = argparse.ArgumentParser(
                            prog = "network_code",
                            description = "Code for analysing how attacks and "
                            "errors on networks may affect network structure and" 
                            "epidemic spreading.",
                        )
    # selection of network type: -n
    parser.add_argument(
            "-n",
            choices = ["ER", "SF", "ER_SF", "airports"],
            required = True,
            help = "Select the type of network to study."
        )
    # type of simulation: -m
    parser.add_argument(
            "-m",
            choices = ["epidemic", "structural"],
            required=True,
            help="Select the type of simulation to run on the network."
        )
    # function to analyse: -f
    parser.add_argument(
            "-f",
            required = True,
            metavar="FEATURE",
                help = "Select the feature to analyze during the simulation.\n"
            "  • For '-m epidemic' → peak, t_peak, duration, total_infected"
            "  • For '-m structural' → connectivity, fragmentation"
        )
    
    parser.add_argument('-N', type=int, default=100,
                        help = "Number of nodes of the network, default = 100")
    parser.add_argument('-p', type=float, default=0.04,
                        help = "Probability for ER to connect with other nodes, default = 0.04")
    parser.add_argument('-seed', type=int, default=102,
                        help = "For reproducibility, default = 102")
    parser.add_argument('-max_rate', type=float, default=0.5,
                        help = "The maximum rate of removable nodes, default = 0.5")
    parser.add_argument('-mu', type=float, default=0.2,
                        help = "Probability of disease transmission, default = 0.2")
    parser.add_argument('-nu', type=float, default=0.05,
                        help = "Probability to recover from infection, default = 0.05")
    parser.add_argument('-steps', type=int, default=50,
                        help = "Number of steps the epidemics simulation lasts, default = 50")
    parser.add_argument('-infected', type=int, default=1,
                        help = "Number of infected cases at the epidemic starting, default = 1")
    parser.add_argument('-num_sim', type=int, default=100,
                        help = "Number of simulations of the epidemic to run to average the epidemic features, default = 100")
    parser.add_argument('-num_points', type=int, default=15,
                        help = "Number of data to acquire, default = 15")
    
    args = parser.parse_args()
    
    # check the validity of input -f
    if args.m == "epidemic":
        valid_funcs = {"peak", "t_peak", "duration", "total_infected"}
        
    else:
        valid_funcs = {"connectivity", "fragmentation"}

    if args.f not in valid_funcs:
        parser.error(
            f"For -m = {args.m!r}, -f must be one among: {sorted(valid_funcs)}"
        )
    

    return args

 

def main():
    
    # get the cmd parameters
    args = parse_args()
    
    # set constants
    N = args.N
    P = args.p
    SEED = args.seed
    MU = args.mu
    NU = args.nu
    STEPS = args.steps
    INFECTED_T0 = args.infected
    MAX_REMOVAL_RATE = args.max_rate
    NUM_POINTS = args.num_points
    NUM_SIMULATIONS = args.num_sim
    
    # for reproducibility
    random.seed(SEED)
    np.random.seed(SEED)
    
    # study of two networks: comparison Erdos-Renyi and Scale-Free
    if args.n == "ER_SF":
        print(f'Network parameters for ER and SF:\nN = {N}\np = {P}\n') 
        ER = generate_network("ER", N, P)
        SF = generate_network("SF", N, P)
        
        if args.m == "structural":
            
            Simulator_ER = ToleranceSimulation(ER, MAX_REMOVAL_RATE)
            Simulator_SF = ToleranceSimulation(SF, MAX_REMOVAL_RATE)
            
            if args.f == "connectivity":
                
                freq, d_error_ER, d_attack_ER = connectivity_analysis(Simulator_ER)
                freq, d_error_SF, d_attack_SF = connectivity_analysis(Simulator_SF)

                fig, ax = make_plot_2networks(freq, 
                                     d_error_ER, d_attack_ER, d_error_SF, d_attack_SF,  
                                     ylabel='Diameter', 
                                     title='SF and ER networks: diameter'
                                     )
                
            elif args.f == "fragmentation":
                
                freq, S_error_ER, S_attack_ER, s_error_ER, s_attack_ER = fragmentation_analysis(Simulator_ER)
                freq, S_error_SF, S_attack_SF, s_error_SF, s_attack_SF = fragmentation_analysis(Simulator_SF)
                
                # plot for the S and <s> for ER
                fig, ax = make_plot_fragmentation(freq, 
                                             S_error_ER, S_attack_ER, s_error_ER, s_attack_ER,  
                                             ylabel='S, <s>', 
                                             title='Erdos Renyi: S and <s>'
                                             )
                # plot for the S and <s> for SF
                fig, ax = make_plot_fragmentation(freq, 
                                             S_error_SF, S_attack_SF, s_error_SF, s_attack_SF, 
                                             ylabel='S, <s>',
                                             title='Scale-Free: S and <s>'
                                             )
        elif args.m == "epidemic": #epidemic study
            print(f'Epidemic parameters:\nmu = {MU}\nnu = {NU}\nsteps = {STEPS}\nnumber of starting infected cases = {INFECTED_T0}\n')
            Simulator_ER = EpidemicToleranceSimulation(ER, MU, NU, STEPS, INFECTED_T0, MAX_REMOVAL_RATE, NUM_POINTS)
            Simulator_SF = EpidemicToleranceSimulation(SF,  MU, NU, STEPS, INFECTED_T0, MAX_REMOVAL_RATE, NUM_POINTS)
            
            feature = EPIDEMICS_FUNCS[args.f][0]
            freq, results_error_ER, results_attack_ER = epidemic_feature_analysis(Simulator_ER, feature, NUM_SIMULATIONS)
            freq, results_error_SF, results_attack_SF = epidemic_feature_analysis(Simulator_SF, feature, NUM_SIMULATIONS)

            label = EPIDEMICS_FUNCS[args.f][1]
            fig, ax = make_plot_2networks(freq, 
                                         results_error_ER, results_attack_ER, results_error_SF, results_attack_SF,  
                                         ylabel=f'{label}',
                                         title=f'ER and SF networks: {label}'
                                         )
            
    # study of single network: Erdos-Renyi, Scale-Free, Air Traffic
    else:

        if args.n == "airports":
            G = generate_network(args.n)
            
        else:
            G = generate_network(args.n, N, P)
            print(f'Network parameters for {args.n}:\nN = {N}\np = {P}\n') 
            
        if args.m == "structural":

            Simulator = ToleranceSimulation(G, MAX_REMOVAL_RATE)
                
            if args.f == "connectivity":
                freq, d_error, d_attack = connectivity_analysis(Simulator)
                fig, ax = make_plot(freq, 
                                        d_error, d_attack,  
                                        ylabel='Diameter',
                                        title=f'{args.n} network: diameter'
                                        )
                
            elif args.f == "fragmentation":
                freq, S_error, S_attack, s_error, s_attack = fragmentation_analysis(Simulator)
                    
                fig, ax =make_plot_fragmentation(freq, 
                                                S_error, S_attack, s_error, s_attack,  
                                                ylabel='S, <s>',
                                                title=f'{args.n} network: S and <s>'
                                                )
            
                
        elif args.m == "epidemic":      #epidemic study
            print(f'Epidemic parameters:\nmu = {MU}\nnu = {NU}\nsteps = {STEPS}\nnumber of starting infected cases = {INFECTED_T0}\n')
            Simulator = EpidemicToleranceSimulation(G, MU, NU, STEPS, INFECTED_T0, MAX_REMOVAL_RATE, NUM_POINTS)
                
            feature = EPIDEMICS_FUNCS[args.f][0]
            freq, results_error, results_attack = epidemic_feature_analysis(Simulator, feature, NUM_SIMULATIONS)
                
            label = EPIDEMICS_FUNCS[args.f][1]
            fig, ax = make_plot(freq, 
                                results_error, results_attack,
                                ylabel=f'{label}',
                                title=f'{args.n} network: {label}'
                                )
    
    plt.show()

    
if __name__ == "__main__":
    main()