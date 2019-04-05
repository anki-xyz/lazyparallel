# lazyparallel
A class to easily run a function in parallel with runtime estimation

## Minimal example

    from lazy import LazyParallel, f
    # f only sleeps for 1 s and returns the iterator
    # specify function (f) and the iterable (here, range(12))
    # it uses internally imap (so only one (!) argument per function)
    # the output is ordered.
    l = LazyParallel(f, range(12))
    l.run(verbose=True)
    
creates the following (final) output on my computer with four cores (2 real, 2 hyper-threading):

    Running f in parallel on 4 cores.
    Number of tasks: 12
    [100%]   eta 0 s       
    
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

## Settings

    LazyParallel(function, iterable, cores='auto')
   
   
By default, all available cores are used ('auto'). 
Otherwise, just specify the number of cores.
Very easy usage: Create class (1) and run (2).

## Notes for juptyer notebook

- The function **must not** be defined in the notebook! Please provide it in a separate file and import it (see above example)
- Sometimes, it is maybe neccessary to run it in the following way:


        if __name__ ==  '__main__':
              l = LazyParallel(f, range(12))
              l.run()
        
        
However, I never encountered that.
