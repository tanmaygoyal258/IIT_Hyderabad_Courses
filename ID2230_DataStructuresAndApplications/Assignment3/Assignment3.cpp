/*
ID2230

AUTHOR: TANMAY GOYAL, AI20BTECH10021

ASSIGNMENT 3: SOCIAL DISTANCE CALCULATOR: find the distance and shortest path between two nodes

NOTE: Code is working fine on MACOSX and replit.com, anything that uses clang compiler
*/

# include <iostream>
# include <cstring>
# include <fstream>
# include <cstdlib>
# include <algorithm> //for dynamically allocating memory

using namespace std;

// creating struct graph with 4 columns 
// column 2 -> degree
// column 3 -> pointer to list of neighbours
// column 4 -> distance
// column 5 -> predecessor
struct graph
{
    int degree;
    int* neighbor;
    int distance;
    int pred;
};

void insert_into_queue(int* Q, int* tail, int value)
{
    /*
    adds an element to a queue, which follows the First In first Out principle
    */

    (*tail) += 1;
    Q[*tail] = value;
}

int remove_from_queue(int* Q , int * head , int* tail)
{
    /*
    adds an element to a queue, which follows the First In first Out principle
    returns the value removed
    */
    if((*head)== (*tail) + 1)
    {
        cout<<"Empty Queue"<<endl;
        return -1;
    }
    
    else
    {
        int x = Q[*head];
        (*head) += 1;
        return x;
    }
    }

int main()
{
    string file;

    // taking the name of the file
    cout<<"Enter name of file for testing"<<endl;
    cin>>file;
    ifstream fin,fin_1;
    string line;

    // reading the file
    fin.open(file);
    

    int deg = 1; // to keep track of current degree
    int mnode = -1; // to keep track of maximum index of node
    int mdeg = 1 ; // to keep track of maximum degree
    
    while(getline(fin,line))
    // while we are still able to read data from fin into line
    {
    
    string edge1 = "";
    string edge2 = "";
    

    // splitting the pair of edges about the comma
    int i = 0 ;
    for (; line[i]!=',';i++)
    {
        edge1 += line[i];
    }
    
    i += 1;

    for(;i < line.length()-1 ; i++)
    // length-1 to avoid the extra space at the end of password
    {
        edge2 += line[i];
    }
    
    int edge1_int = stoi(edge1);
    int edge2_int = stoi(edge2);

    

    // checking for maximum node and maxmum degree
    
    if (edge1_int > mnode)
    {
        mdeg = max(mdeg,deg);
        mnode = edge1_int;
        deg = 1;  

    }
    if (edge1_int == mnode)
    {
        deg += 1;    
    }
    }
    mdeg = max(mdeg,deg);
    // since for mnode, there is no mnode+1, we are unable to do so in the last loop, so we check seperately
       

// declaring an array of type struct graph
struct graph adj[mnode];

// initialising all distances and predecessors to -1 to differentiate between visited and unvisited
for (int i = 0 ; i < mnode+1 ; i++)
{
    adj[i].distance = adj[i].pred = -1;
}


// filling in the adjacency list 
int node_current = -1;
int degree = 0;

fin_1.open(file);

while(getline(fin_1,line))
{
    
    string edge1 = "";
    string edge2 = "";
    

    // splitting the pair of edges about the comma
    int i =0 ;
    for (; line[i]!=',';i++)
    {
        edge1 += line[i];
    }
    
    i += 1;

    for(;i < line.length()-1 ; i++)
    // length-1 to avoid the extra space at the end of password
    {
        edge2 += line[i];
    }
    
    int edge1_int = stoi(edge1);
    int edge2_int = stoi(edge2);
    
    
    if(node_current == edge1_int) // we are still continuing with the same node
    {
        degree += 1;
        void * p = realloc(adj[node_current].neighbor , sizeof(int)*degree);
        adj[node_current].neighbor = (int*)p;
        // reallocating memory by increasing the space by one

        *(adj[node_current].neighbor + (degree-1))= edge2_int; //putting the neighbor node in
        
    }
    if(node_current < edge1_int) // we are moving onto new node
    {
        adj[edge1_int].neighbor = (int*) malloc(sizeof(int)); // assigning the memory
        adj[edge1_int].neighbor[0] = edge2_int;
        adj[node_current].degree = degree;
        degree = 1;
        node_current = edge1_int;
    }
    
}
adj[mnode].degree = degree; 
// since for mnode, there is no mnode+1, we are unable to update degree inside loop

//adjacency lists are now ready


// creating variables head and tail to keep track in Queue
int head = 0;
int tail = -1;

// taking input of two nodes from user
int node1, node2;

cout<<"Enter first node: ";
cin>>node1;
cout<<"Enter second node: ";
cin>>node2;

// making sure node 1 is smaller than node2, else we swap
if(node1>node2)
{
    int temp = node2;
    node2 = node1;
    node1 = temp;
}
else if(node1 == node2)
{
    cout<<"Distance is 0"<<endl;
    cout<<"Shortest path is "<<node1<<","<<node1<<endl;
}

if(node1 < node2)
{

int queue[mdeg*100];
int vertex = node1;
adj[vertex].distance = 0;
int result = 0;

insert_into_queue(queue, &tail , vertex); // putting the vertex into queue so we can enter while loop

for(;vertex >= 0 && result==0;) // when dequeue returns -1, it means queue is empty
{
vertex = remove_from_queue(queue,&head,&tail); // dequeue vertex

for (int i = 0 ; result ==0 && i<adj[vertex].degree ; i++) // examine adjacency list
{
// iterating over all neighbours of vertex
if(adj[adj[vertex].neighbor[i]].distance < 0) // unvisisted node
{
    insert_into_queue(queue, &tail , adj[vertex].neighbor[i]); //enqueued into the Queue
    adj[adj[vertex].neighbor[i]].pred = vertex; //setting the predecessor
    adj[adj[vertex].neighbor[i]].distance = adj[vertex].distance + 1; // updating the distance
}

if(adj[vertex].neighbor[i]  == node2) // if we have found our end vertex
{
    cout<<"Distance is "<<adj[adj[vertex].neighbor[i]].distance<<endl;
    result = 1; // to break out of while loop
    break; // to break out of for loop
}
}
}

// storing the path in an array, we donot directly print because we need to reverse the order
int path[adj[node2].distance + 1];
int nodes_in_path = node2;
int i =1;
path[0] = nodes_in_path;

while(adj[nodes_in_path].pred>=0) // if pred is -1, we have reached our starting node
{
    path[i] = nodes_in_path = adj[nodes_in_path].pred; // recursively storing predecessors
    i += 1;
}


// reversing the path array to print shortest path
cout<<"The Shortest path between the nodes is: "<<endl;
cout<<node1<<endl; // our start vertex was not stored in the path array
for(int i = adj[node2].distance-1 ; i >=0 ; i--)
{
    cout<<path[i]<<endl;
}

}

}