#include <stdlib.h>
#include <iostream>

using namespace std;

int main(int argc, char** argv){
	int n; // number of bits
	int num_nodes;

        if (argc == 2){
	        n = atoi(argv[1]);
		num_nodes = 1 << n;
	} else {
		cout << "Enter number of nodes (as power of 2) in hypergraph\n";
		exit(1);
	}

	for(int i = 0; i < num_nodes; i++){
   		// we check with which vertices is it connected
	   	for(int j = 0; j < i; j++){
   			// we stop when j >= i, because we want to output each unordered pair once
     			int u = i ^ j;

			// we check if U is a power of 2, by rounding it up to next power of two and
			// checking if it changed
			int k = u - 1;
			k |= k >> 1;
			k |= k >> 2;
			k |= k >> 4;
			k |= k >> 8;
			k |= k >> 16;
	
			if(k + 1 == u){
				if (i < j){
		     			cout << i << ";" << j << endl;
				} else {
		     			cout << j << ";" << i << endl;
				}
			}
		} 
	}
	return 0;
}
