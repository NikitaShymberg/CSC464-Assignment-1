package main

import (
	"fmt"
)

var buffer = make(chan int)
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
	go producer(100)
	go producer(100)
	go consumer(50)
	go consumer(50)
	go consumer(50)
	go consumer(50)
	<-done
	<-done
	<-done
	<-done
	<-done
	<-done
}
