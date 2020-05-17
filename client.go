package main
import (
	"fmt"
	"time"
	"net/http"
	"os"
	"io/ioutil"
	"flag"
	"log"
)

func main(){
	var country string
	flag.StringVar(&country, "opt", "", "Usage")
	flag.Parse()
	ts:=time.Now()
	response,err:= http.Get("http://localhost:5000/json/" + country)
	if err!=nil{
		fmt.Println(err.Error())
		os.Exit(1)
	}
	responseData,err := ioutil.ReadAll(response.Body)
	if err!=nil {
		log.Fatal(err)
	}
	fmt.Println(string(responseData))
	tf:=time.Now()
	fmt.Println(tf.Sub(ts))
}
