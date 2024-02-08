import numpy as np
import heapq
from typing import Union
import math

class Graph:

    def __init__(self, adjacency_mat: Union[np.ndarray, str]):
        """
    
        Unlike the BFS assignment, this Graph class takes an adjacency matrix as input. `adjacency_mat` 
        can either be a 2D numpy array of floats or a path to a CSV file containing a 2D numpy array of floats.

        In this project, we will assume `adjacency_mat` corresponds to the adjacency matrix of an undirected graph.
    
        """
        if type(adjacency_mat) == str:
            self.adj_mat = self._load_adjacency_matrix_from_csv(adjacency_mat)
        elif type(adjacency_mat) == np.ndarray:
            self.adj_mat = adjacency_mat
        else: 
            raise TypeError('Input must be a valid path or an adjacency matrix')
        self.mst = None

    def _load_adjacency_matrix_from_csv(self, path: str) -> np.ndarray:
        with open(path) as f:
            return np.loadtxt(f, delimiter=',')

    def construct_mst(self):
        """
    
        TODO: Given `self.adj_mat`, the adjacency matrix of a connected undirected graph, implement Prim's 
        algorithm to construct an adjacency matrix encoding the minimum spanning tree of `self.adj_mat`. 
            
        `self.adj_mat` is a 2D numpy array of floats. Note that because we assume our input graph is
        undirected, `self.adj_mat` is symmetric. Row i and column j represents the edge weight between
        vertex i and vertex j. An edge weight of zero indicates that no edge exists. 
        
        This function does not return anything. Instead, store the adjacency matrix representation
        of the minimum spanning tree of `self.adj_mat` in `self.mst`. We highly encourage the
        use of priority queues in your implementation. Refer to the heapq module, particularly the 
        `heapify`, `heappop`, and `heappush` functions.

        """
        priority_queue = []      
        # edge case for checking for 1 node
        if self.adj_mat.size == 1:
            self.mst = 0
            return
        # create list of nodes here 
        nodes = [i for i in range(len(self.adj_mat))]
        # create adjacency matrix for MST here - filling in all weights with zero to start 
        self.mst = np.zeros([len(nodes), len(nodes)])
        visited = set()
        j = 0
        visited.add(nodes[0])
        # Loop through the first node - this code assumes that you always start from the first node in your adjacency matrix.
        for edge in self.adj_mat[0]:
            if edge > 0:
                heapq.heappush(priority_queue, (edge, 0, j))
            j += 1
        # your minimum spanning tree will have same number of nodes as well as (n - 1) edges. 
        
        # Checks for only returning minimum spanning tree for all connected nodes
        while (len(visited) < len(self.adj_mat[~np.all(self.adj_mat == 0, axis=0)]) ):
            # edge case for if there is only 1 node within the graph - MST should return itself 
            # pop smallest edge weight, start node, and end node 
            edge, start, end = heapq.heappop(priority_queue)
            # check whether the end node is already in visited 
            if end not in visited:
                # append end node here 
                visited.add(end)
                self.mst[start, end] = edge
                self.mst[end, start] = edge
                j = 0
                # loop through neighbors of end node to see if any of the neighbors are in visited nodes or not 
                for edge in self.adj_mat[end]:
                    if edge > 0: 
                        if j not in visited:
                            heapq.heappush(priority_queue, (edge, end, j))
                    j += 1