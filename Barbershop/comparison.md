# Problem 6: Concurrent list comparisson of implementations

## Description and relevance to code bases
This problem simulates multiple threads accessing a shared list data structure. There are two kinds of threads - readers and writers. Writers write a number to a random index of the shared list, and readers read from a random index of the list. One implementation has two mutexes and allows multiple readers to look at the list at once. The other implementation has only one mutex and will only let one thread look at the list at a time. In hindsight, this is essentially the readers writers problem solved in a data structure.

An example of a real world software problem where such a solution is applied to would be a collaborative text editor. // TODO

## Results

Regular barbershop
```
Total runtime: 3.288873354s
```

Busy wait barbershop
```
Total runtime: 4m49.48313935s
```

## Analysis