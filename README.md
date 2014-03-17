CS726_Probabilistic_Graphical_Models

====================================
Message Passing Algorithm (MPA)

Sumeet Fefar  (10D070001)
Ankit Agrawal (10D070027)

====================================
Assignment : 

http://www.cse.iitb.ac.in/~sunita/cs726/protected/hw3.html


Installation :

You will require python 2.7, python-numpy library.

	numpy  : Type 'sudo apt-get install python-numpy' in terminal
	python : Built-in for Ubuntu users	/ Windows users install python 2.7

Python tutorials :

http://www.tutorialspoint.com/python/python_command_line_arguments.htm

Usage :

Open python in terminal

1) To create a Graph:

		>run Graph.py
	
	A Graph 'G' will get generated.

2)To create a triangulate the Graph 'G':

		>H = G.triangulate()
		
	'H' will be a triangulated version of 'G'
	
2) To create a junction-tree of 'H':

		>H.junctionTree()
		
	A junction-tree object will be created as 'H._Jtree'
	
3) For marginal probability query:
	
		>H.sum_query(['1','8'])
		>H.sum_query(['7'])
		>H.sum_query([<query parameters>])
		
	it will output marginal probabilities according to query
	
4) To see the nodes of the junction tree:
	
		>H._JTree._nodeList
		
		Outputs a list of sets each representing a maximal clique
		
4) To see the edgeList of the junction tree:

		>H._JTree._edgeList
		
		Outputs a list of list where ith element of the inner list representing a tuple '( index of destination clique in H._JTree._nodeList , no of variable common between cliques)' represents edges going out from ith clique of H._JTree._nodeList.
		Each edge is unidirectional therefore there are two unidirectional edges of opposite direction between two cliques if at all.
		
5) To see messages of sum_query:

		>H._JTree._msg

6) To change files path for graph, potentials change filepaths at line 489,490 in Graph.py

		