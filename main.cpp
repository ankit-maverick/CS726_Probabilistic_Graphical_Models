#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>

using namespace std;


class Node
{
int index;
int card; 
};


class Graph
{
/*
protected:
    int num_nodes;
    int num_edges;
*/
public:
    int num_nodes;
    int num_edges;
    
    void parse(string fileName)
    {
        ifstream inf(fileName.c_str());
        int line_no = 0;

        if (!inf)
        {
            cerr << "Could not open the file " << fileName << endl;
            exit(1);
        }

        while(inf)
        {
            std::string strInput;
            getline(inf, strInput);
            if (line_no == 0)
            {
                num_nodes = atoi(strInput.c_str());
            }

            else if (line_no == 1)
            {
                num_edges = atoi(strInput.c_str());
            }
            cout << strInput << endl;
            line_no++;
        }
    }
};

int main()
{
    Graph myGraph;
    myGraph.parse("samplegraph.txt");
    cout << "Num of nodes : " << myGraph.num_nodes << endl;
    cout << "Num of edges : " << myGraph.num_edges << endl;

    return 0;
}
