package main

import (
	"fmt"
	"time"
)

var buffer = make(chan int, 10000)
var done = make(chan bool)

func producer(tokens int) {
	for i := 0; i < tokens; i++ {
		buffer <- i
	}
	done <- true
}

func consumer(tokens int) {
	for i := 0; i < tokens; i++ {
		fmt.Println(<-buffer)
	}
	done <- true
}

func main() {
	start := time.Now()
	go producer(10000)
	go producer(10000)
	go consumer(5000)
	go consumer(5000)
	go consumer(5000)
	go consumer(5000)
	<-done
	<-done
	<-done
	<-done
	<-done
	<-done
	fmt.Printf("Total runtime: %s\n", time.Since(start))
}
