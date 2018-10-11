# Producer and consumer problem

## Description and relevance to code bases
This problem is similar to the classic producer consumer concurrency problem. There is one cook that puts resources into the pot for the savages to consume. When the pot is empty a savage must wake the cook up and ask him to put more resources into the pot.

TODO:!!! An example of a real world software problem where such a solution is applied to would be in TODO:!!!

## TODO: Results (???)

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

### TODO: Performance (???)

In the above tables, it is impossible to know whether the male or the female threads will need to wait longer, so without loss of generality, the slow wait time refers to the type of thread that needed to wait longer. There appears to be clear winner in terms of performance. In the no starve solution both types of threads have to wait _longer_ to use the bathroom on average. In the regular solution when a thread gets into a line with other threads of the opposite gender to use the bathroom, there is a 50% chance that the other threads in the bathroom have the same gender and the current thread would be able to enter straight away (or at most wait for one thread to exit if the bathroom is full). In the no starve solution however, if there are other threads of the opposite gender in line already, the current thread would need to wait for them to finish before being able to enter the bathroom.

It is worth noting that the results in this experiment are a little skewed as all threads are being spawned at once. If the spawn times of threads were more staggered, then the average wait times in the no starve solution would be lower - likely in between the fast and slow wait times of the regular solution. Nevertheless, the slow and fast wait times of the no starve solution would be very similar, and in the regular solution much more different.

### Comprehensibility
The comprehensibility of these two solutions is quite subjective and depends on the users familiarity with mutexes and Go channels. The lengths of the two types of functions are similar enough to not be relevant to the readability of the code. The python solution uses three separate synchronization objects whereas the Go one uses only two so it has the edge in that respect. The Go solution also uses one of its channels as the pot itself whereas the python solution needs a separate list for the pot. This can be considered more intuitive as the pot becomes the way for the two types of threads to communicate with each other without the necessity any other communication mechanisms. Personally I would consider the Go solution to be easier to understand, however this is not a concrete statement and might vary from person to person.

### Correctness
In this problem a correct solution is one that doesn't deadlock and allows savages to eat from the pot whenever it is empty, or to be able to wake up the cook to fill it up. The python solution does not deadlock because when the shared `mutex` is held there is only one `wait` for the cook process. During that `wait` the cook fills up the pot which is an operation that is guaranteed to be finite, this means that neither thread can wait forever. In the Go solution the pot is refilled as soon as the last piece of food is removed, this means that savages cannot wait for the pot to be filled up forever. Since the cook is woken up as soon as the last bit of food is removed, it also cannot wait forever and so the solution is deadlock free.

In both solutions all of the savage code is the same and therefore any savage is able to wake the cook up as well as be able to eat from it if there is food in it.