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

var runTimes [5]time.Duration

func getLeftHandedForks(i int) {
	if philosopherState[i] == "hungry" {
		philosopherState[i] = "eating"
		<-forkChannels[left(i)]
		<-forkChannels[right(i)]
	}
	fmt.Printf("Philosopher %d is eating\n", i)
	time.Sleep(200 * time.Millisecond)
}

func getRightHandedForks(i int) {
	if philosopherState[i] == "hungry" {
		philosopherState[i] = "eating"
		<-forkChannels[right(i)]
		<-forkChannels[left(i)]
	}
	fmt.Printf("Philosopher %d is eating\n", i)
	time.Sleep(200 * time.Millisecond)
}

func putForksDown(i int) {
	forkChannels[left(i)] <- true
	forkChannels[right(i)] <- true
	philosopherState[i] = "thinking"
	fmt.Printf("Philosopher %d is thinking\n", i)
}

func leftHandedPhilosopher(i int, done chan bool) {
	startTime := time.Now()
	for j := 0; j < 2; j++ {
		if philosopherState[i] == "thinking" {
			philosopherState[i] = "hungry"
			fmt.Printf("Philosopher %d is hungry\n", i)
			getLeftHandedForks(i)
			putForksDown(i)
		}
	}
	runTimes[i] = time.Since(startTime)
	done <- true
}

func rightHandedPhilosopher(i int, done chan bool) {
	startTime := time.Now()
	for j := 0; j < 2; j++ {
		if philosopherState[i] == "thinking" {
			philosopherState[i] = "hungry"
			fmt.Printf("Philosopher %d is hungry\n", i)
			getRightHandedForks(i)
			putForksDown(i)
		}
	}
	runTimes[i] = time.Since(startTime)
	done <- true
}

func main() {
	// Place all the forks on the table
	c := 0
	for c < 5 {
		forkChannels[c] <- true
		c++
	}

	done := make(chan bool)

	start := time.Now()

	go leftHandedPhilosopher(0, done)
	go leftHandedPhilosopher(1, done)
	go leftHandedPhilosopher(2, done)
	go leftHandedPhilosopher(3, done)
	go rightHandedPhilosopher(4, done)

	<-done
	<-done
	<-done
	<-done
	<-done

	fmt.Printf("Total runtime: %s\n", time.Since(start))
	fmt.Printf("%v\n", runTimes)
}
