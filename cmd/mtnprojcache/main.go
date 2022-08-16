package main

import "github.com/lcrownover/mtnprojcache/internal/cdn"

func main() {
	h := cdn.NewCDNLinkHandler("smith-rock", "https://cdn2.apstatic.com/photos/climb/106229550_large_1494089954.jpg")
	h.SaveImage()
}
