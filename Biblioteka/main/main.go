package main

import (
	"github.com/gorilla/mux"
	"log"
	"net/http"
)

func main() {
	router := mux.NewRouter()

	api := router.PathPrefix("/api/v1").Subrouter()
	api.HandleFunc("/get-reservations/all", getReservations).Methods(http.MethodGet)
	api.HandleFunc("/get-reservations/id/{reservationId}", getReservation).Methods(http.MethodGet)
	api.HandleFunc("/get-reservations/reader/{readerId}", getReservation).Methods(http.MethodGet)
	api.HandleFunc("/update-reservation", updateReservation).Methods(http.MethodPost)
	api.HandleFunc("/add-reservation", addReservation).Methods(http.MethodPost)
	api.HandleFunc("/delete-reservation/id/{reservationId}", deleteReservationId).Methods(http.MethodGet)

	api.HandleFunc("/get-books-availability/all", getBooksAvailability).Methods(http.MethodGet)
	api.HandleFunc("/get-book-availability/id/{bookId}", getBookAvailability).Methods(http.MethodGet)
	api.HandleFunc("/update-book-availability", updateBookAvailability).Methods(http.MethodPost)
	api.HandleFunc("/add-book-availability", addBookAvailability).Methods(http.MethodPost)
	api.HandleFunc("/delete-book-availability/id/{bookId}", deleteBooksAvailabilityId).Methods(http.MethodGet)

	api.HandleFunc("/get-check-outs/all", getCheckOuts).Methods(http.MethodGet)
	api.HandleFunc("/get-check-out/id/{checkOutId}", getCheckOut).Methods(http.MethodGet)
	api.HandleFunc("/get-check-out/reader/{readerId}", getCheckOutReader).Methods(http.MethodGet)
	api.HandleFunc("/get-check-out/employee/{employeeId}", getCheckOutEmployee).Methods(http.MethodGet)
	api.HandleFunc("/update-check-out", updateCheckOut).Methods(http.MethodPost)
	api.HandleFunc("/add-check-out", addCheckOut).Methods(http.MethodPost)
	api.HandleFunc("/delete-check-out/id/{checkOutId}", deleteCheckOutId).Methods(http.MethodGet)

	log.Fatal(http.ListenAndServe(":7010", router))
}
