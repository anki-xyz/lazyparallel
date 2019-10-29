import numpy as np
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import sleep
import sys
from tqdm import tqdm


class LazyParallel:
    """Creates a process pool using the imap function
    of multiprocessing and reports progress"""

    def __init__(self, func, iterable=None, cores='auto', use_threads=False, threads=1):
        """Creates a process pool using the imap function
        of multiprocessing and reports progress
        
        Parameters
        ----------
        func : function
            the function to be processed
        iterable : list, optional
            the function arguments as list (the default is None)
        cores : str, optional
            the number of cores used in parallel
            (the default is 'auto', which takes all available cores)
        use_threads : bool, optional
            uses threads instead of processes
        threads : int, optional
            number of threads/workers to be used in multithreading
        
        """

        self.cores = mp.cpu_count() if cores == 'auto' else cores

        if threads < 1:
            raise Exception("Threads should be higher or equal to 1.")

        self.threads = threads
        self.use_threads = bool(use_threads)

        self.f = func
        self.f_name = func.__name__
        self.i = iterable

    def run(self, func=None, iterable=None):
        """Runs function with items from iterable in parallel
        
        Parameters
        ----------
        func : function, optional
            the function to be processed 
            (the default is None, 
            which looks for the init function)

        iterable : [type], optional
            iterable with function arguments 
            (the default is None, 
            which looks for the init iterable)

        verbose : bool, optional
            states information and progress (the default is True)
        
        Raises
        ------
        Exception
            when no iterable is found
        
        Returns
        -------
        list
            A list of returns of the function
        """

        # Uses a function that is different to __init__
        if func is None:
            func = self.f 
            
        else:
            self.f_name = func.__name__

        # Use a new iterable
        if iterable is None:
            iterable = self.i

        if iterable is None:
            raise Exception("no iterable found, please provide one")

        # Create all processes with number of cores
        #  or threads with number of threads
        if self.use_threads:
            p = ThreadPoolExecutor(self.threads)
        else:
            p = ProcessPoolExecutor(self.cores)

        num_tasks = len(iterable)

        if verbose:
            if self.use_threads:
                print('Running {} concurrently on {:d} thread(s).'.format(self.f_name, self.threads))

            else:
                print('Running {} in parallel on {:d} core(s).'.format(self.f_name, self.cores))

            print('Number of tasks: {:d}'.format(num_tasks))

        rl = []

        for r in tqdm(p.map(func, iterable), total=num_tasks):
            rl.append(r)

        return rl

def f_sleep(i):
    """Function that does nothing than sleeping for 1 second
    
    Parameters
    ----------
    i : int
        a variable that does nothing
    
    Returns
    -------
    int
        the input variable
    """

    sleep(1)
    return i

def f_cpu_heavy(i):
    """Function that does some long computations
    
    Parameters
    ----------
    i : int
        a variable that does nothing
    
    Returns
    -------
    int
        the input variable
    """
    q = 0

    for k in range(10**7):
        q += k ** 2

    return i


if __name__ == '__main__':
    # Showcase the difference between threads and processes.

    for f in [f_cpu_heavy, f_sleep]:
        print("Testing {} function: ".format(f.__name__))

        # Test if everything works
        print("Using processes...")
        cores = mp.cpu_count()
        l = LazyParallel(f, range(16), cores=4)
        r = l.run()
        print(r)
        # [0, 1, 2, 3, ...]

        print()

        print("Using threads...")
        l = LazyParallel(f, range(16), threads=8, use_threads=True)
        r = l.run()
        print(r)
        # [0, 1, 2, 3, ...]

        print()
        print()
