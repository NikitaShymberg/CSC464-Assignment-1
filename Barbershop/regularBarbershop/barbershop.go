package main

import (
	"fmt"
	"sync"
	"time"
)

const maxQueueLen = 10

var numCustomer = 20
var curQueueLength = 0
var lengthMutex = sync.Mutex{}
var fullMutex = sync.Mutex{}

var queuedCustomers = make(chan int, maxQueueLen)
var pokeCook = make(chan bool)
var done = make(chan bool)

func giveHairCut(i int) {
	var t = 200 * time.Millisecond
	fmt.Printf("Cutting hair %d!\n", i)
	go getHairCut(t)
	time.Sleep(t)
}

func getHairCut(t time.Duration) {
	fmt.Printf("Getting my hair cut!\n")
	time.Sleep(t)
}

func barber() {
	for i := 0; i < numCustomer-1; i++ {
		fmt.Printf("Waiting for %d\n", i)
		<-queuedCustomers
		lengthMutex.Lock()
		curQueueLength--
		lengthMutex.Unlock()
		giveHairCut(i)
	}
	done <- true
}

func customer() {
	lengthMutex.Lock()

	if curQueueLength <= maxQueueLen {
		curQueueLength++
		fmt.Println("I'm in the waiting room")
		lengthMutex.Unlock()
	} else {
		lengthMutex.Unlock()
		fullMutex.Lock()
		numCustomer--
		fullMutex.Unlock()
		fmt.Println("It's full :(")
		return
	}

	queuedCustomers <- 1
}

func main() {
	startTime := time.Now()
	go barber()
	for i := 0; i < numCustomer; i++ {
		time.Sleep(50 * time.Millisecond)
		go customer()
	}
	<-done
	fmt.Printf("Total runtime: %s\n", time.Since(startTime))
}
