# lazyparallel
A class to easily run a function in parallel with runtime estimation

## Minimal example

    from lazy import LazyParallel, f_cpu_heavy
    # f_cpu_heavy performs heavy computations and returns the iterator
    # Specify function (f_cpu_heavy) and the iterable (here, range(12)).
    # It uses internally from concurrent.futures the map function 
    # (similar behavior as multiprocessing.imap, so only one (!) argument per function).
    # The output is ordered.
    l = LazyParallel(f, range(12))
    l.run(verbose=True)
    
creates the following (final) output on my computer with four cores (2 real, 2 hyper-threading):

    Running f in parallel on 4 cores.
    Number of tasks: 12
    [100%]   eta 0 s       
    Time elapsed 14 s
    
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

## Settings

    LazyParallel(function, iterable, cores='auto', use_threads=False, threads=1)
   
   
By default, all available cores are used ('auto'). 
Otherwise, just specify the number of cores.
If your problem is IO-bound, you can use threads instead (```use_threads=True```).
Then, the cores are ignored and the function uses the number of threads provided.
Very easy usage: Create class (1) and run (2).

## Notes for juptyer notebook

- The function **must not** be defined in the notebook! Please provide it in a separate file and import it (see above example)
- Sometimes, it is maybe neccessary to run it in the following way:


        if __name__ ==  '__main__':
              l = LazyParallel(f, range(12))
              l.run()
        
        
However, I never encountered that.
