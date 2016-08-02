'''
Created on Aug 2, 2016

Main test for aco

@author: UNIST
'''

import logging
import sys

from halp.directed_hypergraph import DirectedHypergraph
from opsupport_bpm.aco.aco_directed_hypergraph import aco_algorithm_norec
from opsupport_bpm.aco.aco_misc import random_init_attributes
from opsupport_bpm.models.hypergraph import tau_post_processing
from opsupport_bpm.models.hypergraph_to_pnml import reduce_opt_path_pnet
from opsupport_bpm.models.hypergraph_to_pnml import show_opt_path_pnet
from opsupport_bpm.models.pnml_to_hypergraph import convert_pnet_to_hypergraph
import xml.etree.ElementTree as ET


def main():
    #setup the logger
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='C://BPMNexamples/aco.log',level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    # increase recursion limit (if needed)
    # print(str(sys.getrecursionlimit()))
    # sys.setrecursionlimit(100000000)
    # print(str(sys.getrecursionlimit()))
    
    
    # ========================= A BUNCH OF FILES FOR TESTING =============================
    #file_name = "C://BPMNexamples/inductive/ex1_inductive.pnml"
    #file_name = "C://BPMNexamples/inductive/ex4_inductive.pnml"
    #file_name = "C://BPMNexamples/real_logs/hospital_inductive.pnml"
    #file_name = "C://BPMNexamples/inductive/repair_start_end_inductive.pnml"
    #file_name = "C://BPMNexamples/inductive/ex6_claim_inductive.pnml"
    #The following has loop:
    #file_name = "C://BPMNexamples/inductive/ex5_review_inductive.pnml"
    #file_name = "C://BPMNexamples/alpha/ex1_alpha.pnml"
    
    # =========================================================================================
    # ROOT: the identifier that will be used in the "highlighted" and "reduced" pnml versions
    # TYPE: the name of the folder were the original pnml file can be found (and that should
    # reflect the discovery algorithm used for mining
    
    #file_root = "ex1_inductive"
    file_root = "bpi_challenge2012"
    #file_root = "road_fine_process"
    #file_root = "hospital_inductive"
    #file_root = "repair_start_end_inductive"
    
    file_type = "inductive"
    #file_type = "real_logs"
    
    #MINED WITH ALPHA MINER
    #file_root = "ex6_claim_alpha"
    #file_type = "alpha"
    
    file_name = "C://BPMNexamples/"+file_type+"/"+file_root+".pnml"
    
    # ===================================================================================================
    
    # START: read the pnml file....
    tree = ET.parse(file_name)
    pnet = tree.getroot()
    
    hg = DirectedHypergraph()
    
    # STEP 1: convert pnet into hypergraph + tau post processing
    hg = convert_pnet_to_hypergraph(pnet)
    hg = tau_post_processing(hg)
    
    #STEP 2: randomly initialise hypergraph's nodes utility values
    hg = random_init_attributes(hg)
    #print_hg(hg,'hyp.txt')
    
    #find start node (MAKE A FUNCTION FOR IT!!!!)
    """ INITIALISATION FOR RECURSIVE VERSION
    nodes = hg.get_node_set()
    start_nodes = []
    for node in nodes:
        if hg.get_node_attribute(node, 'source') == True:
            logger.debug("  ")
            logger.debug("$$$$$ Begin optimisation....$$$$$$$$$$$$$$$$$$$$$$$$")
            logger.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            logger.debug("Found start node: {0}".format(print_node(node, hg)))
            logger.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            start_nodes.append(node)
    END """
    
    
    # ==================== INITIALISATION NON RECURSIVE VERSION ===========================================
    logger.debug("*"*50)
    logger.info("*"*50)
    logger.info("*** BEGIN ACO OPTIMISATION.... ***")
    logger.info("*"*50)
    logger.debug("*"*50)

    # Set ACO parameters
    tau = 0.6
    ANT_NUM = 10
    COL_NUM = 3
    W_UTILITY = {'cost' : 1.0, 'avail' : 0.0, 'qual' : 0.0, 'time' : 0.0}
    
    # =====================  call ACO algorithm (NON RECURSIVE)
    #p_opt = aco_algorithm(start_nodes, hg, ANT_NUM, COL_NUM, tau, W_UTILITY)
    p_opt = aco_algorithm_norec(hg, ANT_NUM, COL_NUM, tau, W_UTILITY)
    
    # =================  highlight optimal path on pnet
    show_opt_path_pnet(p_opt, tree, file_root)
    
    # ================= reduce pnet to show only the optimal path
    reduce_opt_path_pnet(tree, file_root)
    
    


if __name__ == "__main__":
    main()