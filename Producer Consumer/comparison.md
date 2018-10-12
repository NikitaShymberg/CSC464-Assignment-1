# Producer and consumer problem

## Description and relevance to code bases
This is a classical concurrency problem that simulated a division of labour between threads. Producers are threads that push elements onto a channel or a queue, and consumers are threads that take these elements off (and in a real application would process them somehow).

An example of a real world software problem where such a solution is applied to would be in event driven systems. The producer would "produce" and event such as a mouse click on an element on a webpage that a consumer would consume, process appropriately, and return a useful result.

## Results

### Python solution

| Run number | Runtime (sec) |
|------------|---------------|
| 1          | 0.908         |
| 2          | 0.815         |
| 3          | 0.957         |
| 4          | 0.898         |
| 5          | 0.967         |
| MEAN       | 0.909         |

### Golang solution

| Run number | Runtime (sec) |
|------------|---------------|
| 1          | 0.0741        |
| 2          | 0.0652        |
| 3          | 0.0607        |
| 4          | 0.0699        |
| 5          | 0.0647        |
| MEAN       | 0.0669        |

## Analysis

### Performance

Looking at the above tables there is a clear winner in terms of performance. The Golang solution was almost fourteen times faster than the python one. The likely main reason for this is that the Go program uses a channel to pass tokens from the produces to the consumer threads, whereas the python program uses a queue data structure. Channels are much more lightweight than a queue which results in faster execution times. Another contributing factor is that in order to be correct, the python program had to use mutexes which take a relatively long time to lock and unlock.

### Comprehensibility
The Golang solution is very concise taking only 4 lines each for the producer and consumer functions (+ 2 lines with closing brackets). The python solution takes 6 and 7 lines for the two functions, so the difference in line length isn't very significant. The biggest difference lies in the intuitiveness of the passing of the tokens between the threads. The Go solution takes one line to do this `buffer <- i` and `<- buffer` for the producer and consumer solutions respectively. The python code needs to acquire the `bufferLock` mutex before looking at the buffer and then release it after doing so. Furthermore it requires a second mutex `items` that prevents the producer from trying to read from an empty queue.

Therefore, the Go code is far more easy to understand than the python code.

### Correctness
In this problem a correct solution is one that doesn't deadlock and doesn't have consumers reading from empty buffers. The Go solution can essentially be boiled down to the two lines `buffer <- i` and `<- buffer`, everything else is just the function declaration and the loop. The only interleaving of these lines that could cause deadlock would be if the producer simply was producing fewer items than the consumer was expecting - this would be a misuse of the designed functions. It is worth noting that it is possible to design the functions such that this is not possible (for example by removing the loops), but since this is just an exercise this is not important. 

The python solution uses the `items` mutex to prevent the consumer from accessing an empty buffer. It's initial value is 0 which would block a consumer thread from looking at the buffer, and it is only ever released after a producer puts a token into the queue. Therefore in the state that the current solutions are they are both correct, however the python solution is a little more robust and requires less knowledge of the code to be used correctly.