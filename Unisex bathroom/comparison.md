# Unisex bathroom problem

## Description and relevance to code bases
This is a concurrency problem that simulates restricted access to a resource to a limited number of certain types of threads. Only either male or female threads are allowed to run at a time, and only at most 3 can run at once. The rest are barred by the "bathroom lock".

The applications of this problem are very similar to the reader writer problem. The no starve solution will offer equal priority to the two types of threads. Mutual exclusion is still guaranteed between the two types of threads as is necessary for the reader writer problem. 

## Results

### Regular solution

| Run number | Total Runtime (sec) | Fast thread wait time (sec) | Long thread wait time (sec)|
|------------|---------------------|-----------------------------|----------------------------|
| 1          | 8.560               | 2.440                       | 6.794                      |
| 2          | 8.548               | 2.509                       | 6.708                      |
| 3          | 8.567               | 1.764                       | 5.968                      |
| 4          | 8.567               | 2.511                       | 6.720                      |
| 5          | 8.543               | 2.755                       | 6.950                      |
| MEAN       | 8.557               | 2.396                       | 6.628                      |

### No starve solution

| Run number | Total Runtime (sec) | Fast thread wait time (sec) | Long thread wait time (sec)|
|------------|---------------------|-----------------------------|----------------------------|
| 1          | 14.11               | 7.367                       | 7.245                      |
| 2          | 15.08               | 8.315                       | 8.004                      |
| 3          | 14.08               | 7.065                       | 7.029                      |
| 4          | 15.63               | 8.780                       | 6.911                      |
| 5          | 15.13               | 8.990                       | 7.581                      |
| MEAN       | 14.81               | 8.103                       | 7.354                      |

## Analysis

### Performance

In the above tables, it is impossible to know whether the male or the female threads will need to wait longer, so without loss of generality, the slow wait time refers to the type of thread that needed to wait longer. There appears to be clear winner in terms of performance. In the no starve solution both types of threads have to wait _longer_ to use the bathroom on average. In the regular solution when a thread gets into a line with other threads of the opposite gender to use the bathroom, there is a 50% chance that the other threads in the bathroom have the same gender and the current thread would be able to enter straight away (or at most wait for one thread to exit if the bathroom is full). In the no starve solution however, if there are other threads of the opposite gender in line already, the current thread would need to wait for them to finish before being able to enter the bathroom.

It is worth noting that the results in this experiment are a little skewed as all threads are being spawned at once. If the spawn times of threads were more staggered, then the average wait times in the no starve solution would be lower - likely in between the fast and slow wait times of the regular solution. Nevertheless, the slow and fast wait times of the no starve solution would be very similar, and in the regular solution much more different.

### Comprehensibility
These two solutions are very similar to each other so comprehensibility is quite straightforward to evaluate. The no starve solution uses an extra two mutexes that need to each be acquired and released. This is the only difference between the two solutions. Generally the more complex a program is the more difficult is it to understand, having more synchronization mechanisms makes a program more complicated and thus regular is the more easily comprehensible solution.

### Correctness
In this problem a correct solution is one that doesn't deadlock and follows the two constraints of the problem. Deadlock in this problem could be caused by threads in the line to the bathroom waiting for each other. In both solutions threads that are in line do not interact with each other and so they cannot deadlock. It is worth noting that in the current implementation there is no queue data structure in which the threads wait in line and as such there are race conditions as to which thread enters the bathroom when there is room, however this is not crucial to this problem.

In both solutions, whenever a thread enters the bathroom it flips the lightswitch that marks the bathroom as occupied preventing threads from the opposite gender from entering. There is also a multiplex for each gender that blocks too many threads from entering the bathroom at once. This fulfills the constraints of the problem.

It is worth mentioning that in the regular solution all threads from one gender enter the bathroom followed by all threads from the other gender. This could cause very real starvation issues in a real world system if threads enter the queue faster than they are able to exit. While that condition is true, threads from the other gender simply will not be able to enter the bathroom and thus do not have a bounded waiting time. 