# Problem 6: Concurrent list comparison of implementations

## Description and relevance to code bases
This problem simulates multiple threads accessing a shared list data structure. There are two kinds of threads - readers and writers. Writers write a number to a random index of the shared list, and readers read from a random index of the list. One implementation has two mutexes and allows multiple readers to look at the list at once. The other implementation has only one mutex and will only let one thread look at the list at a time. In hindsight, this is essentially the readers writers problem solved in a data structure.

An example of a real world software problem where such a solution is applied to would be in a database implementation. If there are multiple users using the same table at once, a similar solution would need to be implemented to prevent data races. Multiple users should be allowed to read data in the database at once, but writers to the table should wait until there are no read operations or other write operations being performed prior to altering the table.

## Results

### Two mutex solution

| Sleep duration (line 24) | Main thread runtime (sec) | Average Writer runtime (sec)| Average Reader runtime (sec)|
|--------------------------|---------------------------|-----------------------------|-----------------------------|
| No pause                 | 0.429                     | 0.000764                    | 0.0000576                   |
| 0.01 second pause        | 0.595                     | 0.000451                    | 0.0132                      |
| 0.05 second pause        | 0.662                     | 0.000406                    | 0.0590                      |

### One mutex solution

| Sleep duration (line 18) | Main thread runtime (sec) | Average Writer runtime (sec)| Average Reader runtime (sec)|
|--------------------------|---------------------------|-----------------------------|-----------------------------|
| No pause                 | 0.433                     | 0.000324                    | 0.0000216                   |
| 0.01 second pause        | 1.585                     | 0.000321                    | 0.761                       |
| 0.05 second pause        | 1.810                     | 0.0000795                   | 0.927                       |

## Analysis

### Performance

In both solutions, the average writer runtimes were quite similar to each other. This makes sense as during the experiment they appeared to be entirely scheduled before any reader threads, since the two writer thread codes were essentially identical they are not the main focus of the performance analysis. The main difference in runtime was in the average reader runtimes. When the read function did not have a pause and simply read the value from the list, the one mutex solution proved to be considerably faster than the more complex two mutex one. This is due to the overhead costs encountered when locking multiple mutexes. However when a read function had a pause in it and took longer to run, the more complex solution performed much quicker. This is because the one mutex solution could only let one thread into the critical section at a time, and as the thread took a long time to read all the other readers needed to wait for it to finish. In the two mutex solution on the other hand, all readers could be let into the critical section at once and would perform the long read together.

Thus for very quick reads one mutex would result in quicker performance, but for longer reads two mutexes would be faster.

### Comprehensibility
These two solutions are very similar to each other so comprehensibility is quite straightforward to evaluate. The solution that allows multiple readers at the same time uses two mutexes, whereas the other uses only one more global one. This is the only difference between the two solutions. Generally the more complex a program is the more difficult is it to understand, having more synchronization mechanisms makes a program more complicated and thus cListOneMutex is the more comprehensible solution.

### Correctness
In this problem a correct solution is a solution that doesn't have any data races. The cListOneMutex program only allows one thread access to the list at a time. This means that data races cannot happen and so the solution is correct. The cListTwoMutex solution will let multiple readers have access to the list at once, however this is not a problem as reading the data does not change it. Whenever a writer is given access to the shared list, it is guaranteed to be the only thread looking at it as the wMutex that it acquires blocks any other readers or writers from accessing the list. Thus both solutions are correct.