#include<iostream>
#include<bits/stdc++.h>
using namespace std;

#define WHITE 0
#define GRAY 1
#define BLACK 2
#define SIZE 100

int adj[SIZE][SIZE];
int colour[SIZE];
int parent[SIZE];
int dis[SIZE];
char T,t;
int vertex, l, m, s, r;
int node1,node2;

void TakeVertices();
void TakeEdges();
void StartAndEndPoint();
void BFS(int adj[][SIZE] , int vertex , int startingNode, int endNode);
void PrintPath(int startingNode , int endNode);
void MatrixInitialize();
void ShortestPath();

void TakeVertices()
{
        MatrixInitialize();
        cin>>vertex;
}

void TakeEdges()
{
            cin>>t;
            while(t!= '}')
            {
                cin>>t>>node1>>t>>node2>>t>>t;
                    if (node1<vertex && node2<vertex)
                    {
                    adj[node1][node2]=adj[node2][node1]=1;
                    }
                    else
                    {
                    cout<<"Error: Vertex does not exist. "<<endl;
                    continue;
                    }
            }
}

void StartAndEndPoint()
{
    cin >> s >> r;
}

void MatrixInitialize()
{
    for(l=0;l<100;l++)
            {
                for(m=0;m<100;m++)
                {
                    adj[l][m] = 0;
                }
            }
}

void BFS(int adj[][SIZE] , int vertex , int startingNode, int endNode)
{
    for(int i = 0 ; i < vertex ; i++)
    {
        if(i!= startingNode)
        {
            colour[i] = WHITE;
            dis[i] = INT_MIN;
            parent[i] = -1;
        }
    }

    colour[startingNode] = GRAY;
    dis[startingNode] = 0;
    parent[startingNode] = -1;
    queue <int> BFSQueue;
    BFSQueue.push(startingNode);
    while(!BFSQueue.empty())
    {
        int u = BFSQueue.front();
        BFSQueue.pop();
        for(int i = 0 ; i < vertex ; i++)
        {
            if(adj[u][i]!=0)
            {
                int v = i;
                if(colour[v] == WHITE)
                {
                    colour[v] = GRAY;
                    dis[v] = dis[u]+1;
                    parent[v] = u;
                    BFSQueue.push(v);
                    if(v==endNode)
                    {
                        return;
                    }
                }
            }
        }
        colour[u] = BLACK;
    }
}

void ShortestPath()
{
    StartAndEndPoint();

    if (s<vertex && r<vertex)
        {
        BFS(adj , vertex , s, r);
        PrintPath(s,r);
        }
    else
        {
        cout<<"Error: Invalid value of start or end point detected."<<endl;
        }
 }

void PrintPath(int startingNode , int endNode)
{
    int path[SIZE];
    int  par = parent[endNode];
    int i = 0;
    par = endNode;
    if(parent[endNode]==-1)
        {
        cout << "Error: No path exits" << endl;
        return;
        }

    while(par != -1)
        {
        path[i++] = par;
        par = parent[par];
        }

    while(i>0)
        {
        cout << path[i-1];
        if(i==1)
            {
            cout << endl;
            }
        else
            {
            cout << "-";
            }
        i--;
        }
}

int main()
{
    char T;
    while (cin>>T)
    {
        if(T=='V' || T=='v')
            TakeVertices();
        else if (T=='E' || T=='e')
            TakeEdges();
        else if (T=='S'||T=='s')
            ShortestPath();
        else
            cout<<"Error: Invalid Input."<<endl;
    }
}
