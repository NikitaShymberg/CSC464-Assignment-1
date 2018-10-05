package main

import (
	"fmt"
	"time"
)

var M = 10

var pot = make(chan int, M)
var pokeCook = make(chan bool)
var done = make(chan bool)

func cook() {
	for;;{
		for i := 0; i < M; i++ {
			pot <- i
		}
		<- pokeCook
	}
}

func savage(){
	for;;{
		var food int 
		food = <- pot
		fmt.Printf("Eating: %d\n", food)
		time.Sleep(1 * time.Second)
		if food == M-1{
			pokeCook <- true
		}
	}
}

func main(){
	go cook()
	go savage()
	go savage()
	go savage()
	<- done
}