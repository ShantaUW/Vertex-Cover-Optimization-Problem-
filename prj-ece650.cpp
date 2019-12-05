#include <iostream>
#include <sstream>
#include <algorithm>
#include <pthread.h>
#include <vector>
#include <fstream>
#include <memory>
#include <time.h>
#include <algorithm>
#include <stdlib.h>
#include "minisat/core/Solver.h"
#include "minisat/core/SolverTypes.h"

using namespace std;
using namespace Minisat;

void *threadInOut(void *arg);
void *cnfSat(void *arg);
void *approxVC1(void *arg);
void *approxVC2(void *arg);

struct Graph {
    unsigned V;
    vector<vector<unsigned>> E;
    vector<unsigned> cnfsat;
    vector<unsigned> approxvc1;
    vector<unsigned> approxvc2;
};

void *threadInOut(void *arg) {
    auto *G = (Graph *) arg;

    while (!cin.eof()) {
        string Input;
        getline(cin, Input);
        stringstream input(Input);

        char cmd_in = '0';
        input >> cmd_in;
        if (cmd_in == 'V') {
            input >> G->V;
        } else if (cmd_in == 'E') {
            while (!input.eof()) {
                char symb;
                input >> symb;
                if (symb == '<') {
                    unsigned node1, node2;
                    char comma;
                    input >> node1 >> comma >> node2;
                    G->E.push_back({node1, node2});
                }
            }

            pthread_t t_algorithm1, t_algorithm2, t_algorithm3;

            pthread_create(&t_algorithm1, nullptr, &cnfSat, G);
            pthread_create(&t_algorithm2, nullptr, &approxVC1, G);
            pthread_create(&t_algorithm3, nullptr, &approxVC2, G);

            pthread_join(t_algorithm1, nullptr);
            pthread_join(t_algorithm2, nullptr);
            pthread_join(t_algorithm3, nullptr);

            cout << "CNF-SAT-VC: ";
            for (unsigned i = 0; i < G->cnfsat.size(); ++i) {
                if (i == 0) cout << G->cnfsat[i];
                else cout << "," << G->cnfsat[i];
            }
            cout << endl;
            G->cnfsat.clear();

            cout << "APPROX-VC-1: ";
            for (unsigned i = 0; i < G->approxvc1.size(); ++i) {
                if (i == 0) cout << G->approxvc1[i];
                else cout << "," << G->approxvc1[i];
            }
            cout << endl;
            G->approxvc1.clear();

            cout << "APPROX-VC-2: ";
            for (unsigned i = 0; i < G->approxvc2.size(); ++i) {
                if (i == 0) cout << G->approxvc2[i];
                else cout << "," << G->approxvc2[i];
            }
            cout << endl;
            G->approxvc2.clear();
            G->E.clear();
        }
    }
    return nullptr;
}

void *cnfSat(void *arg) {
    auto *G = (Graph *) arg;

    if (G->E.empty())
        return nullptr;

    for (unsigned m = 1; m < G->V; ++m) {
        unique_ptr<Solver> solver(new Solver());
        vector<vector<Lit>> lit(G->V);

        //initialize
        for (unsigned i = 0; i < G->V; ++i)
            for (unsigned j = 0; j < m; ++j) {
                Lit l = mkLit(solver->newVar());
                lit[i].push_back(l);
            }

        //At least one vertex is the ith vertex in the vertex cover.
        for (unsigned i = 0; i < m; ++i) {
            vec<Lit> ps;
            for (unsigned j = 0; j < G->V; ++j) {
                ps.push(lit[j][i]);
            }
            solver->addClause(ps);
        }

        //No one vertex can appear twice in a vertex cover.
        for (unsigned i = 0; i < G->V; ++i)
            for (unsigned j = 0; j < m - 1; ++j)
                for (unsigned k = j + 1; k < m; ++k)
                    solver->addClause(~lit[i][j], ~lit[i][k]);

        //No more than one vertex appears in the mth position of the vertex cover.
        for (unsigned i = 0; i < m; ++i)
            for (unsigned j = 0; j < G->V - 1; ++j)
                for (unsigned k = j + 1; k < G->V; ++k)
                    solver->addClause(~lit[j][i], ~lit[k][i]);

        //Every edge is incident to at least one vertex in the vertex cover.
        for (unsigned i = 0; i < G->E.size(); ++i) {
            vec<Lit> ps;
            for (unsigned j = 0; j < m; ++j) {
                ps.push(lit[G->E[i][0]][j]);
                ps.push(lit[G->E[i][1]][j]);
            }
            solver->addClause(ps);
        }

        if (solver->solve()) {
            for (unsigned i = 0; i < G->V; ++i)
                for (unsigned j = 0; j < m; ++j)
                    if (solver->modelValue(lit[i][j]) == l_True)
                        G->cnfsat.push_back(i);

            solver.reset(new Solver());
            return nullptr;
        }
        solver.reset(new Solver());
    }
    return nullptr;
}

void *approxVC1(void *arg) {
    auto *G = (Graph *) arg;

    if (G->E.empty())
        return nullptr;

    vector<bool> visit(G->E.size(), false);

    while (true) {
        vector<unsigned> count(G->V, 0);
        for (unsigned i = 0; i < G->E.size(); ++i)
            if (visit[i] == false) {
                count[G->E[i][0]]++;
                count[G->E[i][1]]++;
            }

        unsigned vMax = distance(count.begin(), max_element(count.begin(), count.end()));
        G->approxvc1.push_back(vMax);

        for (unsigned i = 0; i < G->E.size(); ++i)
            if (G->E[i][0] == vMax || G->E[i][1] == vMax)
                visit[i] = true;

        if (find(visit.begin(), visit.end(), false) == visit.end()) {
            sort(G->approxvc1.begin(), G->approxvc1.end());
            return nullptr;
        }
    }
}

void *approxVC2(void *arg) {
    auto *G = (Graph *) arg;

    vector<vector<unsigned>> tmpE = G->E;
    ifstream urandom("/dev/urandom");
    while (!tmpE.empty()) {
        int num = 23;
        urandom.read((char *) &num, sizeof(int));
        unsigned index = abs(num) % (tmpE.size());
        unsigned a = tmpE[index][0], b = tmpE[index][1];
        G->approxvc2.push_back(a);
        G->approxvc2.push_back(b);
        for (unsigned i = 0; i < tmpE.size();)
            if (tmpE[i][0] == a || tmpE[i][0] == b || tmpE[i][1] == a || tmpE[i][1] == b)
                tmpE.erase(tmpE.begin() + i);
            else ++i;
    }
    sort(G->approxvc2.begin(), G->approxvc2.end());
    return nullptr;
}

int main() {
    Graph G;
    pthread_t t_in_out;
    pthread_create(&t_in_out, nullptr, &threadInOut, &G);
    pthread_join(t_in_out, nullptr);
    return 0;
}
