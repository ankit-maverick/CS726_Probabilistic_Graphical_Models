#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <sstream>
#include <boost/algorithm/string.hpp>
#include <vector>
#include <unordered_map>
#include <cstdarg>

using namespace std;


// TODO : Implement variadic functions for set_potential and get_potential


class Graph
{


private:

    class Node
    {
    public:
        int index;
        int cardinality; 
        bool * neighbours;
    };

    
    class CPT
    {
    public:
        int * node_seq;
        int * cardinality_seq;
        int * cardinality_prod_seq; // used in setting potential while parsing
        float * potentials;

        /*void set_potential()

        */
        // float get_potential
        // CPT multiply(CPT other)
        // CPT eliminate(int node)
        // 
    };
    


    int num_nodes ;
    int num_edges ;
    Node * NodeArray;
    unordered_map <string, CPT> factors;


public:

    void parseGraph(string fileName)
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

    void parseCPT(string fileName)
    {
        ifstream inf(fileName.c_str());
        int line_no = 1;
        vector<string> strs;

        if (!inf)
        {
            cerr << "Could not open the file " << fileName << endl;
            exit(1);
        }
        string key = "";
        while(inf)
        {
            std::string strInput;
            getline(inf, strInput);

            boost::split(strs, strInput, boost::is_any_of(" "));
            
            if (strs.at(0) == "#")
            {
                key = "";
                for (int i=1; i<strs.size(); i++){
                    key = key + strs[i];
                }
                cout << key << endl;
                factors[key] = CPT();
                factors[key].node_seq = new int[strs.size() - 1];
                factors[key].cardinality_seq = new int[strs.size() - 1];
                factors[key].cardinality_prod_seq = new int[strs.size() - 1];
                int len_potentials = 1;
                for (int i=1; i<strs.size(); i++){
                    factors[key].node_seq[i - 1] = atoi(strs.at(i).c_str());
                    factors[key].cardinality_seq[i - 1] = NodeArray[factors[key].node_seq[i - 1]].cardinality;
                    factors[key].cardinality_prod_seq[i - 1] = len_potentials;
                    len_potentials = len_potentials * NodeArray[factors[key].node_seq[i - 1]].cardinality;
                }
                factors[key].potentials = new float[len_potentials];
            }

            else
            {
                int index = 0;
                for (int i=0; i<strs.size()-1; i++)
                {
                    index = index + factors[key].cardinality_prod_seq[i]*atoi(strs.at(i).c_str());
                }
                factors[key].potentials[index] = atof(strs.at(strs.size()-1).c_str());

            }

        }

    }

    void printParameters()
    {
    	cout << "Num of nodes : " << num_nodes << endl;
    	cout << "Num of edges : " << num_edges << endl;
    	for (int i = 0; i < num_nodes; i++)
    	{
    		cout<< "Node : "<<i<<" " << NodeArray[i].cardinality<<"   -=> ";
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
    myGraph.parseGraph("samplegraph.txt");
    myGraph.parseCPT("potentials.txt");
/*    cout << "Enter a clique between 01 and 12 by typing the string : ";
    string clique;
    cin >> clique;
    cout << "Enter the value in 0-2 1st variable takes : ";
    int val1;
    cin >> val1;
    cout << "Enter the value in 0-2 2nd variable takes : ";
    int val2;
    cin >> val2;
    cout << "The corresponding potential Psi_" + clique + "(" + val1 + "," + val2 + ") = " + myGraph.factors[clique].potentials
*/
	myGraph.printParameters();

    return 0;
}
