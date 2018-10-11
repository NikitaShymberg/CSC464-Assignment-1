# Producer and consumer problem

## Description and relevance to code bases
This is **the** classic concurrency problem. There are 5 philosophers sitting around a round table, in between each philosopher is a chopstick or a fork. When philosophers get hungry, they grab the forks next to them and eat, after they're done eating they return the forks to the table and continue to think. This problem simulates the sharing of limited resources between concurrent threads when each thread needs more than one resource. 

An example of a real world software problem where such a solution is applied to would be in event driven systems. The producer would "produce" and event such as a mouse click on an element on a webpage that a consumer would consume, process appropriately, and return a useful result.

## Results

The python solution to this problem uses the famous solution proposed by Tanenbaum. In this solution a philosopher can start eating only if the two beside him aren't eating. Whenever a philosopher finishes eating they will let those beside them know that they are done, so if their neighbours are hungry they can eat. The Go solution is different in that it has four left handed philosophers and one right handed one.

## Analysis

### Performance

The main measurable metric in this problem is the waiting time of hungry threads. In the implemented solution this was done by measuring the total runtime of a philosopher thread, this is the time to eat two meals as well as all of the wait time in between. The first line of the print statement is the total time taken for all philosophers to each, the array printed below is the runtime of each philosopher thread.

A sample output of the Go program:
```
Total runtime: 1.209432777s
[1.209233145s 1.40939405s 604.584049ms 804.867508ms 1.006016194s]
```

A sample output of the python program (all times are in seconds):
```
Total runtime: 0.8188929557800293
[0.616426944732666, 0.8175380229949951, 0.41075778007507324, 0.6163182258605957, 0.8172898292541504]
```

Bearing in mind that Go programs tend to run much faster than python programs, this result implies that the Go solution is much slower. A likely reason behind this is that all philosophers become hungry at nearly the exact same time (or at least while others are still eating). In the Go solution since there is only one right handed philosopher, everyone else has to wait for them. Consider the following likely scenario: all philosophers become hungry at the same time and pick up one fork, and the right handed philosopher wins the race condition with their right neighbour. The right neighbour must now wait for the right handed philosopher to finish eating before they can start, and their right neighbour must wait for them and so on around the table. Thus only one philosopher can eat at a time which is inefficient. This can be seen in the thread run times as each runtime increases by roughly 0.2 seconds.

In Tanenbaum's solution however, when a similar situation happens the philosopher that finishes eating will wake up both of his neighbours so that two philosophers can eat at the same time. This can be clearly seen in the thread run times - first the 0.4 second philosopher finished, then the two 0.6 ones, then the two 0.8 ones.

### Comprehensibility
The Go solution is easier to understand for two main reasons. The first reason is that it models the concept of forks more clearly than the python one. The python solution doesn't have any representation of forks, it simply has a constraint that prevents neighbours from eating at the same time. Given that the forks are such a core constraint of the problem, the solution that has a representation of a fork is easier to understand. The Golang solution also wins in terms of intuitiveness. It is easier to picture why this solution works and why deadlock cannot happen with a right handed philosopher in a pool of left handed philosophers. The python solution is more abstract and mathematical making it less easy to understand.

### Correctness
The dining philosophers problem has the following four constraints:
1. Only one philosopher can hold a fork at a time
2. Deadlock cannot occur
4. Multiple philosophers should be able to eat at the same time
3. A philosopher cannot starve waiting for a fork

The Go solution satifies the first constraint by virtue of forks being channels that can only hold one object, thus only one thread can read from the channel at a time. The python solution satisfies this with the check to see if any of the philosopher's neighbours are eating, if any are then the philosopher cannot eat and so forks cannot be shared.

In the Go solution deadlock cannot occur because for that to happen each philosopher needs to be holding one fork. Since one phisolopher is right handed and the rest are left handed there will be a race condition between the right handed philosopher and the left handed one, the winner of this race will wake up all of the other philosophers step by step. The python solution cannot deadlock because `mutex` is the only shared semaphore, and no threads execute any waits while holding the semaphore.

Condition three is satisfied by the go solution because the fork channels aren't related to each other and thus philosophers sitting across from each other can eat at the same time. Similarly in the python solution only the neighbours can prevent a philosopher from eating so again philosophers sitting across from each other can eat at the same time.

The last condition is satisfied by both programs pretty simply, before a thread can eat it must wait for its neighbour to finish eating. Since eating time is finite, the waiting function is guaranteed to not starve.