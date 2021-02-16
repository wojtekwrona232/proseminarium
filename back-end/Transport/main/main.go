package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	router := mux.NewRouter()

	api := router.PathPrefix("/api/v1").Subrouter()
	api.HandleFunc("/get-couriers/all", getCouriers).Methods(http.MethodGet)
	api.HandleFunc("/get-courier/id/{courierId}", getCourier).Methods(http.MethodGet)
	api.HandleFunc("/update-courier", updateCourier).Methods(http.MethodPost)
	api.HandleFunc("/add-courier", addCourier).Methods(http.MethodPost)
	api.HandleFunc("/delete-courier/id/{courierId}", deleteCourierId).Methods(http.MethodGet)
	api.HandleFunc("/delete-courier/name/{courierName}", deleteCourierName).Methods(http.MethodGet)

	api.HandleFunc("/get-packages/all", getPackages).Methods(http.MethodGet)
	api.HandleFunc("/get-packages/id/{packageId}", getPackageId).Methods(http.MethodGet)
	api.HandleFunc("/get-packages/courier/{courierId}", getPackageCourier).Methods(http.MethodGet)
	api.HandleFunc("/get-packages/number/{packageNumber}", getPackageNumber).Methods(http.MethodGet)
	api.HandleFunc("/get-packages/sender/{senderId}", getPackageSender).Methods(http.MethodGet)
	api.HandleFunc("/get-packages/receiver/{receiverId}", getPackageReceiver).Methods(http.MethodGet)
	api.HandleFunc("/get-packages/delivery-state/{deliveryState}", getPackageDeliveryState).Methods(http.MethodGet)
	api.HandleFunc("/update-packages", updatePackage).Methods(http.MethodPost)
	api.HandleFunc("/add-packages", addPackage).Methods(http.MethodPost)
	api.HandleFunc("/delete-packages/package-number/{packageNumber}", deletePackageNumber).Methods(http.MethodGet)
	api.HandleFunc("/delete-packages/package-id/{packageId}", deletePackageId).Methods(http.MethodGet)

	log.Fatal(http.ListenAndServe(":8000", router))
}
