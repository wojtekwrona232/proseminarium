package main

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"net/http"
	"strconv"
)

func getReservations(w http.ResponseWriter, _ *http.Request) {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	var reservation []Reservation
	db.Preload("Reservation").Find(&reservation)

	var err error
	err = json.NewEncoder(w).Encode(reservation)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var err1 error
	err1 = db.Close()
	if err1 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func getReservation(w http.ResponseWriter, r *http.Request)  {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	reservationId := -1

	var err error
	if val, ok := params["reservationId"]; ok {
		reservationId, err = strconv.Atoi(val)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
	}

	var reservation []Reservation
	db.Preload("Reservation").First(&reservation, reservationId)

	var err1 error
	err1 = json.NewEncoder(w).Encode(reservation)
	if err1 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	var err2 error
	err2 = db.Close()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func getReservationReader(w http.ResponseWriter, r *http.Request)  {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	readerId := params["readerId"]

	var reservation []Reservation
	db.Where("reader_id = ?", readerId).Find(&reservation)

	var err1 error
	err1 = json.NewEncoder(w).Encode(reservation)
	if err1 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	var err2 error
	err2 = db.Close()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func updateReservation(w http.ResponseWriter, r *http.Request) {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var reservation Reservation
	var err error
	err = json.NewDecoder(r.Body).Decode(&reservation)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	db.Save(&reservation)
	w.Header().Set("Content-Type", "application/json")

	var err1 error
	err1 = json.NewEncoder(w).Encode(reservation)
	if err1 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var err2 error
	err2 = db.Close()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func addReservation(w http.ResponseWriter, r *http.Request) {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var reservation Reservation
	var err error
	err = json.NewDecoder(r.Body).Decode(&reservation)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	db.Save(&reservation)
	w.Header().Set("Content-Type", "application/json")

	var err1 error
	err1 = json.NewEncoder(w).Encode(reservation)
	if err1 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var err2 error
	err2 = db.Close()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func deleteReservationId(w http.ResponseWriter, r *http.Request) {
	var err error
	err = initDB()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	params := mux.Vars(r)
	reservationId := params["reservationId"]
	id64, _ := strconv.ParseUint(reservationId, 10, 64)
	idToDel := uint(id64)

	db.Where("id = ?", idToDel).Delete(&Reservation{})

	w.WriteHeader(http.StatusNoContent)

	var err2 error
	err2 = db.Close()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}
