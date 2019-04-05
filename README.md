# lazyparallel
A class to easily run a function in parallel with runtime estimation

## Minimal example

    from lazy import LazyParallel, f
    # f only sleeps for 1 s and returns the iterator
    l = LazyParallel(f, range(12))
    l.run(verbose=True)
    
creates the following (final) output on my computer with four cores (2 real, 2 hyper-threading):

    Running f in parallel on 4 cores.
    Number of tasks: 12
    [100%]   eta 0 s       
    
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
