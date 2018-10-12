# Barbershop problem

## Description and relevance to code bases
This problem simulates multiple threads waiting for a "barber" thread to process their requests. Multiple customer threads are able to enter the barbershop at once until it is full. When the first thread enters the barbershop it wakes the barber up at which point the barber gives it a haircut. If the barbershop is full when a thread enters it is rejected.

An example of a real world software problem where a similar solution is used would be a single threaded server with very limited resources. When a request thread arrives (a customer) the server thread (the barber) serves its request. Due to the server's limited resources it can only accept a finite number of requests at which point it will reject any more until it has more room left. 

## Results

There are two implementations to this problem, the first one is a regular solution using go channels for the customers to communicate with the barber. The second solution is very similar however the customers have a busy wait (i.e. the keep polling an array until they have been services). The intent is to show the difference in performance of a busy wait vs a normal wait.

Regular barbershop runtime
```
Total runtime: 3.288873354s
```

Busy wait barbershop runtime
```
Total runtime: 4m49.48313935s
```

## Analysis

### Performance
The regular barbershop runtime was by far superior to the busy wait runtime as expected. The busy wait runtime was even worse prior to the addition of the print statement on line 72. This print statement forces the go routine to perform I/O which prevents it from being scheduled as often allowing the barber to actually give haircuts. These two solutions demonstrate the very large extent to which a busy wait is slow. Granted, there were around 20 customer threads that managed to fit into the barbershop which were all busy waiting, so with a smaller number of threads this difference might not have been as high. Nonetheless, regular waits will waste much less of the CPU's time on unnecessary processing.

### Comprehensibility
The busy wait solution uses identical code to the regular solution and builds on top of it. The core synchronization tools are the same between the two solutions except that customer threads are explicitly stopped by the barber after they have been serviced in the busy wait solution. This adds an extra (unnecessary) layer to the code that doesn't positively contribute to the comprehensibility of the code and could possibly cause confusion. Therefore the regular solution is certainly easier to understand.

### Correctness
Since the busy wait solution uses the basic structure of the regular solution, showing the correctness of the regular solution will do the same for the busy wait solution. This solution is guaranteed to serve all customers as the barber thread always reads from the `queuedCustomers` channel (in a real world implementation, the for loop in line 35 would be infinite, however to be able to measure performance it had to be capped). Before a customer enters the barbershop it checks if it is full using a mutex to prevent other threads from changing that value, so there cannot be more customers than the capacity at any given time. Furthermore whenever a thread locks a shared mutex, it doesn't acquire any other mutexes which solves any deadlock problems.