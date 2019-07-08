# Task 4 - Evaluating DB Performance

This task consists of comparing the performances of the hash and btree structures. We used the Kyoto Cabinet library that already has the necessary implementations of the two structures. The Kyoto Cabinet library is available at https://fallabs.com/kyotocabinet/.

For the experiment, we selected 100,000 valid NIS from the bolsa.csv file used in task 3. The selected NIS were inserted into the two structures to be evaluated. As the objective of the experiment is to evaluate the search performance in the structures in terms of time, the real keys (pointers) were not used. 100 evaluations were performed where at each iteration the data were scrambled and a batch of {1000, 2000, 3000, ..., 100000} was used to obtain the search time in each of the structures.

The experiment was implemented in a jupyter notebook and its html version is also available. The graph with the result is in the notebook jupyter and also in the "evaluating.png" file.

As a conclusion, the hash structure exhibits higher performance as the amount of fetch data increases.
