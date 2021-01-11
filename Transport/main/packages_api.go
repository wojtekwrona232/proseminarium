package main

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"net/http"
	"strconv"
)

func getPackages(w http.ResponseWriter, _ *http.Request)  {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	var packages []Package
	db.Preload("Courier").Find(&packages)

	var err error
	err = json.NewEncoder(w).Encode(packages)
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

func getPackageId(w http.ResponseWriter, r *http.Request)  {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	packageId := -1

	var err error
	if val, ok := params["packageId"]; ok {
		packageId, err = strconv.Atoi(val)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
	}

	var packages []Package
	db.Preload("Courier").First(&packages, packageId)

	var err3 error
	err3 = json.NewEncoder(w).Encode(packages)
	if err3 != nil {
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

func getPackageNumber(w http.ResponseWriter, r *http.Request)  {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	packageNumber := params["packageNumber"]

	var packages []Package
	db.Preload("Courier").Where("package_number = ?", packageNumber).First(&packages)

	var err3 error
	err3 = json.NewEncoder(w).Encode(packages)
	if err3 != nil {
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

func getPackageSender(w http.ResponseWriter, r *http.Request)  {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	senderId := params["senderId"]

	var packages []Package
	db.Preload("Courier").Where("id_library_sender = ?", senderId).Find(&packages)

	var err3 error
	err3 = json.NewEncoder(w).Encode(packages)
	if err3 != nil {
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

func getPackageReceiver(w http.ResponseWriter, r *http.Request)  {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	receiverId := params["receiverId"]

	var packages []Package
	db.Preload("Courier").Where("id_library_receiver = ?", receiverId).Find(&packages)

	var err3 error
	err3 = json.NewEncoder(w).Encode(packages)
	if err3 != nil {
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

func getPackageDeliveryState(w http.ResponseWriter, r *http.Request)  {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	deliveryState := params["deliveryState"]

	var packages []Package
	db.Preload("Courier").Where("delivery_stage = ?", deliveryState).Find(&packages)

	var err3 error
	err3 = json.NewEncoder(w).Encode(packages)
	if err3 != nil {
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

func updatePackage(w http.ResponseWriter, r *http.Request) {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var packages Package
	var err error
	err = json.NewDecoder(r.Body).Decode(&packages)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	db.Save(&packages)
	w.Header().Set("Content-Type", "application/json")

	var err3 error
	err3 = json.NewEncoder(w).Encode(packages)
	if err3 != nil {
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

func addPackage(w http.ResponseWriter, r *http.Request) {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var packages Package
	var err error
	err = json.NewDecoder(r.Body).Decode(&packages)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	db.Save(&packages)
	w.Header().Set("Content-Type", "application/json")

	var err3 error
	err3 = json.NewEncoder(w).Encode(packages)
	if err3 != nil {
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

func deletePackageNumber(w http.ResponseWriter, r *http.Request) {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	params := mux.Vars(r)
	packageNumber := params["packageNumber"]
	db.Where("package_number = ?", packageNumber).Delete(&Package{})
	w.WriteHeader(http.StatusOK)

	var err error
	err = db.Close()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func deletePackageId(w http.ResponseWriter, r *http.Request) {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	params := mux.Vars(r)
	packageId := params["packageId"]
	id64, _ := strconv.ParseUint(packageId, 10, 64)
	idToDel := uint(id64)
	db.Where("id = ?", idToDel).Delete(&Package{})
	w.WriteHeader(http.StatusOK)

	var err error
	err = db.Close()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}
