package main

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"net/http"
	"strconv"
)

func getCheckOuts(w http.ResponseWriter, _ *http.Request) {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	var checkOut []CheckOut
	db.Preload("Reservation").Preload("Book").Preload("Checkout").Find(&checkOut)

	var err error
	err = json.NewEncoder(w).Encode(checkOut)
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

func getCheckOut(w http.ResponseWriter, r *http.Request)  {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	checkOutId := -1

	var err error
	if val, ok := params["checkOutId"]; ok {
		checkOutId, err = strconv.Atoi(val)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
	}

	var checkOut []CheckOut
	db.Preload("Reservation").Preload("Book").Preload("Checkout").First(&checkOut, checkOutId)

	var err1 error
	err1 = json.NewEncoder(w).Encode(checkOut)
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

func getCheckOutReader(w http.ResponseWriter, r *http.Request)  {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	readerId := params["readerId"]


	var checkOut []CheckOut
	db.Preload("Reservation").Preload("Book").Preload("Checkout").Where("reader_id = ?", readerId).Find(&checkOut)

	var err1 error
	err1 = json.NewEncoder(w).Encode(checkOut)
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

func getCheckOutEmployee(w http.ResponseWriter, r *http.Request)  {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	employeeId := params["employeeId"]


	var checkOut []CheckOut
	db.Preload("Reservation").Preload("Book").Preload("Checkout").Where("employee_id = ?", employeeId).Find(&checkOut)

	var err1 error
	err1 = json.NewEncoder(w).Encode(checkOut)
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

func updateCheckOut(w http.ResponseWriter, r *http.Request) {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var checkOut CheckOut
	var err error
	err = json.NewDecoder(r.Body).Decode(&checkOut)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	db.Save(&checkOut)
	w.Header().Set("Content-Type", "application/json")

	var err1 error
	err1 = json.NewEncoder(w).Encode(checkOut)
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

func addCheckOut(w http.ResponseWriter, r *http.Request) {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var checkOut CheckOut
	var err error
	err = json.NewDecoder(r.Body).Decode(&checkOut)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	db.Save(&checkOut)
	w.Header().Set("Content-Type", "application/json")

	var err1 error
	err1 = json.NewEncoder(w).Encode(checkOut)
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

func deleteCheckOutId(w http.ResponseWriter, r *http.Request) {
	var err error
	err = initDB()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	params := mux.Vars(r)
	checkOutId := params["checkOutId"]
	id64, _ := strconv.ParseUint(checkOutId, 10, 64)
	idToDel := uint(id64)

	db.Where("id = ?", idToDel).Delete(&CheckOut{})

	w.WriteHeader(http.StatusNoContent)

	var err2 error
	err2 = db.Close()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}
