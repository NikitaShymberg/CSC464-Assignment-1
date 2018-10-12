package main

import (
	"fmt"
	"time"
)

// M Max food
var M = 10

var pot = make(chan int, M)
var pokeCook = make(chan bool)
var done = make(chan bool)

var runTimes [3]time.Duration

func cook() {
	for {
		for i := 0; i < M; i++ {
			pot <- i
		}
		<-pokeCook
	}
}

func savage(index int) {
	startTime := time.Now()
	for i := 0; i < 10; i++ {
		var food int
		food = <-pot
		fmt.Printf("Eating: %d\n", food)
		time.Sleep(200 * time.Millisecond)
		if food == M-1 {
			pokeCook <- true
		}
	}
	runTimes[index] = time.Since(startTime)
	done <- true
}

func main() {
	go cook()

	startTime := time.Now()
	go savage(0)
	go savage(1)
	go savage(2)
	<-done
	<-done
	<-done
	fmt.Printf("Total runtime: %s\n", time.Since(startTime))
	fmt.Printf("%v\n", runTimes)
}
