package main

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"net/http"
	"strconv"
)

func getCouriers(w http.ResponseWriter, _ *http.Request)  {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	var couriers []Courier
	db.Preload("Courier").Find(&couriers)

	var err error
	err = json.NewEncoder(w).Encode(couriers)
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

func getCourier(w http.ResponseWriter, r *http.Request)  {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	courierId := -1

	var err error
	if val, ok := params["courierId"]; ok {
		courierId, err = strconv.Atoi(val)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
	}

	var couriers []Courier
	db.Preload("Courier").First(&couriers, courierId)

	var err1 error
	err1 = json.NewEncoder(w).Encode(couriers)
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

func updateCourier(w http.ResponseWriter, r *http.Request) {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var courier Courier
	var err error
	err = json.NewDecoder(r.Body).Decode(&courier)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	db.Save(&courier)
	w.Header().Set("Content-Type", "application/json")

	var err1 error
	err1 = json.NewEncoder(w).Encode(courier)
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

func addCourier(w http.ResponseWriter, r *http.Request) {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var courier Courier
	var err error
	err = json.NewDecoder(r.Body).Decode(&courier)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	db.Save(&courier)
	w.Header().Set("Content-Type", "application/json")

	var err1 error
	err1 = json.NewEncoder(w).Encode(courier)
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

func deleteCourierId(w http.ResponseWriter, r *http.Request) {
	var err error
	err = initDB()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	params := mux.Vars(r)
	courierId := params["courierId"]
	id64, _ := strconv.ParseUint(courierId, 10, 64)
	idToDel := uint(id64)

	db.Where("id = ?", idToDel).Delete(&Courier{})

	w.WriteHeader(http.StatusNoContent)

	var err2 error
	err2 = db.Close()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func deleteCourierName(w http.ResponseWriter, r *http.Request) {
	var err error
	err = initDB()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	params := mux.Vars(r)
	nameToDel := params["courierName"]

	db.Where("name = ?", nameToDel).Delete(&Courier{})

	w.WriteHeader(http.StatusNoContent)

	var err2 error
	err2 = db.Close()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}
