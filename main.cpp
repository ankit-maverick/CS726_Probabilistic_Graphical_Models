#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <sstream>
#include <boost/algorithm/string.hpp>
#include <vector>


using namespace std;


class Node
{
public:
	int index;
	int cardinality; 
	bool * neighbours;
};


class Graph
{


private:
    int num_nodes ;
    int num_edges ;
    Node * NodeArray;

public:

    void parse(string fileName)
    {
        ifstream inf(fileName.c_str());
        int line_no = 1;
        vector<string> strs;

        if (!inf)
        {
            cerr << "Could not open the file " << fileName << endl;
            exit(1);
        }

        while(inf)
        {
            std::string strInput;
            getline(inf, strInput);
            if (line_no == 1)	
            {
            	num_nodes = atoi(strInput.c_str());
            	NodeArray = new Node[num_nodes];
            	for (int i=0;i<num_nodes;i++){
            		NodeArray[i].neighbours = new bool[num_nodes] {false};
            	}
            }
            else if (line_no == 2)	
            {
            	num_edges = atoi(strInput.c_str());
           	}
            else if (line_no <= num_nodes+2)
            {
            	boost::split(strs, strInput, boost::is_any_of(" "));
            	NodeArray[atoi(strs.at(0).c_str())].cardinality = atoi(strs.at(1).c_str());
            }
            else if (line_no <= num_nodes + num_edges + 2)
            {
            	boost::split(strs, strInput, boost::is_any_of(" "));
            	NodeArray[atoi(strs.at(0).c_str())].neighbours[atoi(strs.at(1).c_str())] = 1;
            	NodeArray[atoi(strs.at(1).c_str())].neighbours[atoi(strs.at(0).c_str())] = 1;
            }

            cout << strInput << endl;
            line_no++;
        }
    }

    void printParameters()
    {
    	cout << "Num of nodes : " << num_nodes << endl;
    	cout << "Num of edges : " << num_edges << endl;
    	for (int i = 0; i < num_nodes; i++)
    	{
    		cout<< "Node : "<<i<<" " << NodeArray[i].cardinality<<"   -> ";
    		for (int j = 0; j < num_nodes; j++)
    		{
    			cout<< NodeArray[i].neighbours[j] << " ";
    		}
    		cout<<endl;
    	}
    }
};

int main()
{
    Graph myGraph;
    myGraph.parse("samplegraph.txt");
	myGraph.printParameters();

    return 0;
}
