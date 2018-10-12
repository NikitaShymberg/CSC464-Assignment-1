# Dining savages problem

## Description and relevance to code bases
This problem is similar to the classic producer consumer concurrency problem. There is one cook that puts resources into the pot for the savages to consume. When the pot is empty a savage must wake the cook up and ask him to put more resources into the pot.

An example of a real world software problem where such a solution is applied to could be in a distributed system used for data processing. This could allow the cook to dynamically allocate processing work to the different savage computers. Instead of having to initially split up all of the work between all possible computers, the cook assigns a certain number to each, and when each computer finishes the assigned task it lets the cook know that it is done and can get assigned more processing.

## Results

In the section below the total runtime is shown followed by the total runtime of each thread.

### Go solution output

```
Total runtime: 2.436221188s
[2.436187605s 2.436152088s 2.032253087s]
```

### Python solution output (in seconds)

```
Total runtime: 2.0234687328338623
[2.022498846054077, 2.0226809978485107, 2.0221598148345947]
```

## Analysis

### Performance

Each thread had to wait 10 times for 0.2 seconds representing the consumption of the resource, so the python solution can be seen as very fast with all the boilerplate code taking up 0.02 seconds to run. The Go solution is quite a bit slower taking 0.4 seconds for all the boilerplate code to run. A likely cause for this is the disparity of the speeds of accessing a shared list vs copying data over channels. However this will only slow down the total runtime, not the average time that a thread has to wait for the resource to fill up. The Go solution fills up the pot upon taking away the last token, this means that threads do not have to wait for the pot to fill up while they are still consuming their tokens. Furthermore they are able to retrieve tokens from the pot as soon as one exists in it. In the python solution on the other hand, the pot is filled up only when a thread notices that it is empty. If the pot filling process is very slow in a real world application, this will have consequences on the performance. Additionally, the python threads need to wait until the pot is completely full before being able to access it. Nevertheless in this example the cost of Go channels outweighed those other considerations.

### Comprehensibility
The comprehensibility of these two solutions is quite subjective and depends on the users familiarity with mutexes and Go channels. The lengths of the two types of functions are similar enough to not be relevant to the readability of the code. The python solution uses three separate synchronization objects whereas the Go one uses only two so it has the edge in that respect. The Go solution also uses one of its channels as the pot itself whereas the python solution needs a separate list for the pot. This can be considered more intuitive as the pot becomes the way for the two types of threads to communicate with each other without the necessity any other communication mechanisms. Personally I would consider the Go solution to be easier to understand, however this is not a concrete statement and might vary from person to person.

### Correctness
In this problem a correct solution is one that doesn't deadlock and allows savages to eat from the pot whenever it is empty, or to be able to wake up the cook to fill it up. The python solution does not deadlock because when the shared `mutex` is held there is only one `wait` for the cook process. During that `wait` the cook fills up the pot which is an operation that is guaranteed to be finite, this means that neither thread can wait forever. In the Go solution the pot is refilled as soon as the last piece of food is removed, this means that savages cannot wait for the pot to be filled up forever. Since the cook is woken up as soon as the last bit of food is removed, it also cannot wait forever and so the solution is deadlock free.

In both solutions all of the savage code is the same and therefore any savage is able to wake the cook up as well as be able to eat from it if there is food in it.