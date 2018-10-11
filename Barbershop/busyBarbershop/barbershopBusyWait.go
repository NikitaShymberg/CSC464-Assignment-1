package main

import (
	"fmt"
	"sync"
	"time"
)

const maxQueueLen = 10
const initialCustomerLimit = 20

var numCustomer = initialCustomerLimit
var curQueueLength = 0
var lengthMutex = sync.Mutex{}
var fullMutex = sync.Mutex{}
var completedHaircuts [initialCustomerLimit]bool

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
	var index int
	for i := 0; i < numCustomer-1; i++ {
		fmt.Printf("Waiting for %d\n", i)
		index = <-queuedCustomers
		lengthMutex.Lock()
		curQueueLength--
		lengthMutex.Unlock()
		giveHairCut(i)
	}
	completedHaircuts[index] = true
	done <- true
}

func customer(i int) {
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

	queuedCustomers <- i
	// Busy wait
	var q int
	for !completedHaircuts[i] {
		q++
		if q%1000000000 == 0 {
			// Started off as a sanity check because I thought everything broke
			// But it seems to schedule these routines less often if they're performing I/O
			fmt.Printf("%d\n", i)
		}
	}
}

func main() {
	startTime := time.Now()
	go barber()
	for i := 0; i < numCustomer; i++ {
		time.Sleep(50 * time.Millisecond)
		go customer(i)
	}
	<-done
	fmt.Printf("Total runtime: %s\n", time.Since(startTime))
}
