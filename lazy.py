import numpy as np
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import sleep, time
import sys


def timeformat(t, second_precision=0):
    """Given a total number of seconds, returns a dictionary
    with the corresponding hours, minutes and remaining seconds,
    and a formatted string.
    
    Parameters
    ----------
    t : float
        total number of seconds
    second_precision : int, optional
        decimals of seconds (the default is 0, which renders 1.27 s  to 1 s)
    
    Returns
    -------
    dictionary
        s: formatted string
        hours: hours
        minutes: minutes
        seconds: remaining seconds
    """

    hours   = t // (60 * 60)

    if hours:
        t -= hours * (60 * 60)

    minutes = t // 60

    seconds = t % 60

    s = ""

    if hours:
        s += "{:.0f} h ".format(hours)

    if minutes:
        s += "{:.0f} min ".format(minutes)

    s += ("{:."+str(second_precision)+"f} s ").format(seconds)

    return {'s': s,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds}


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

    def run(self, func=None, iterable=None, verbose=True):
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

        t = np.array([0]*(num_tasks+1))
        t[0] = time()

        for i, r in enumerate(p.map(func, iterable), 1):
            # If one would like to see progress
            if verbose:
                # Set current time
                t[i] = time()
                # Average time per cycle
                av = np.mean(np.diff(t[:i+1]))
                # Average time for remaining cycles:
                eta = av * (num_tasks - i)
                eta_formatted = timeformat(eta)['s']

                # Progress in percent
                progress = i/num_tasks*100

                # Show progress
                s = '\r[{:03.0f}%]   eta {} '.format(progress,
                                                    eta_formatted)

                print(s.ljust(100), end="\r")
                # sys.stderr.flush()
                # sys.stderr.write(s.ljust(100))

            rl.append(r)

        if verbose:
            print()
            print("Time elapsed: {}".format(timeformat(t[-1]-t[0])['s']))

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
        r = l.run(verbose=True)
        print(r)
        # [0, 1, 2, 3, ...]

        print()

        print("Using threads...")
        l = LazyParallel(f, range(16), threads=8, use_threads=True)
        r = l.run(verbose=True)
        print(r)
        # [0, 1, 2, 3, ...]

        print()
        print()
