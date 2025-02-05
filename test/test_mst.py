import pytest
import numpy as np
from mst import Graph
from sklearn.metrics import pairwise_distances


def check_mst(adj_mat: np.ndarray, 
              mst: np.ndarray, 
              expected_weight: int, 
              allowed_error: float = 0.0001):
    """
    
    Helper function to check the correctness of the adjacency matrix encoding an MST.
    Note that because the MST of a graph is not guaranteed to be unique, we cannot 
    simply check for equality against a known MST of a graph. 

    Arguments:
        adj_mat: adjacency matrix of full graph
        mst: adjacency matrix of proposed minimum spanning tree
        expected_weight: weight of the minimum spanning tree of the full graph
        allowed_error: allowed difference between proposed MST weight and `expected_weight`

    TODO: Add additional assertions to ensure the correctness of your MST implementation. For
    example, how many edges should a minimum spanning tree have? Are minimum spanning trees
    always connected? What else can you think of?

    """

    def approx_equal(a, b):
        return abs(a - b) < allowed_error

    total = 0
    for i in range(mst.shape[0]):
        for j in range(i+1):
            total += mst[i, j]
    assert approx_equal(total, expected_weight), 'Proposed MST has incorrect expected weight'

    # assert that your number of nodes between your MST and adjacency matrix remains the same.
    # you should not have less nodes in your MST 

    # Check that you have all nodes here 
    assert ( len(mst) == len(adj_mat) ) 

    # Check for disconnected graphs here - take length of all connected nodes
    assert ( len(mst[~np.all(adj_mat == 0, axis=0)]) == len(adj_mat[~np.all(adj_mat == 0, axis=0)]) ) 

    # assert that your MST has n - 1 edges, where n=number of nodes. 
    # We multiply by two because our adjacency matrix is symmetric. 
    assert ( np.count_nonzero(mst) == (len(adj_mat[~np.all(adj_mat == 0, axis=0)]) - 1) * 2)


def test_mst_small():
    """
    
    Unit test for the construction of a minimum spanning tree on a small graph.
    
    """
    file_path = './data/small.csv'
    g = Graph(file_path)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 8)


def test_mst_single_cell_data():
    """
    
    Unit test for the construction of a minimum spanning tree using single cell
    data, taken from the Slingshot R package.

    https://bioconductor.org/packages/release/bioc/html/slingshot.html

    """
    file_path = './data/slingshot_example.txt'
    coords = np.loadtxt(file_path) # load coordinates of single cells in low-dimensional subspace
    dist_mat = pairwise_distances(coords) # compute pairwise distances to form graph
    g = Graph(dist_mat)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 57.263561605571695)


def test_mst_student():
    """
    
    TODO: Write at least one unit test for MST construction.
    
    """
    # this unit test checks for a disconnected graph where the last node is not connected to the rest of the graph.
    
    file_path = './data/disconnected_graph.csv'
    g = Graph(file_path)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 4)

def test_mst_one_node():
    # this unit test ensures that a MST containing only 1 node will return 0 for adjacency matrix (representing just the same node). 

    file_path = './data/one_node.csv'
    g = Graph(file_path)
    g.construct_mst()
    assert (g.mst == 0)
