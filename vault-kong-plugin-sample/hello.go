package hello

import (
	"fmt"

	"rsc.io/quote"
)

func Hello() string {
	return quote.Hello()
}

func main() {
	fmt.Println("hello")
}
