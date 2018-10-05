package main

import (
	"fmt"
	"time"
)

var forkChannels = [5]chan bool{
	make(chan bool, 1),
	make(chan bool, 1),
	make(chan bool, 1),
	make(chan bool, 1),
	make(chan bool, 1),
}
var philosopherState = [5]string{
	"thinking",
	"thinking",
	"thinking",
	"thinking",
	"thinking",
}

func right(i int) int {
	return ((i + 1) % 5)
}

func left(i int) int {
	return i
}

// IF left and right not eating, I can eat and I block them BOTH
// ELSE wait for them to finish eating

// Idea: after eating, if anyone beside me is hungry give them the fork
// Only pick both forks up at the same time

// Idea 27: just grab any free forks
func getForks(i int) {
	// if both my neighbours aren't eating pick up forks then grab them
	// TODO: clean up - set eating correctly but it works?????????
	if philosopherState[i] == "hungry" && philosopherState[left(i)] != "eating" && philosopherState[right(i)] != "eating" {
		philosopherState[i] = "eating"
		<-forkChannels[left(i)]
		<-forkChannels[right(i)]
	} else if philosopherState[i] == "hungry" && philosopherState[left(i)] != "eating" {
		<-forkChannels[right(i)]
		<-forkChannels[left(i)]
	} else if philosopherState[i] == "hungry" && philosopherState[right(i)] != "eating" {
		<-forkChannels[left(i)]
		<-forkChannels[right(i)]
	}
	fmt.Printf("Philosopher %d is eating\n", i)
	time.Sleep(time.Second)
}

func putForksDown(i int) {
	forkChannels[left(i)] <- true
	forkChannels[right(i)] <- true
	philosopherState[i] = "thinking"
	fmt.Printf("Philosopher %d is thinking\n", i)
}

func philosopher(i int) {
	for {
		if philosopherState[i] == "thinking" {
			philosopherState[i] = "hungry"
			fmt.Printf("Philosopher %d is hungry\n", i)
			getForks(i)
			putForksDown(i)
		}
	}
}

func main() {
	// Place all the forks on the table
	c := 0
	for c < 5 {
		forkChannels[c] <- true
		c++
	}

	done := make(chan bool)

	go philosopher(0)
	go philosopher(1)
	go philosopher(2)
	go philosopher(3)
	go philosopher(4)

	<-done
}
