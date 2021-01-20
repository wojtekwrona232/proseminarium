package main

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"net/http"
	"strconv"
)

func getBooksAvailability(w http.ResponseWriter, _ *http.Request) {
	var err2 error
	err2 = initDB()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	var books []Book
	db.Preload("Book").Find(&books)

	var err error
	err = json.NewEncoder(w).Encode(books)
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

func getBookAvailability(w http.ResponseWriter, r *http.Request)  {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	bookId := -1

	var err error
	if val, ok := params["bookId"]; ok {
		bookId, err = strconv.Atoi(val)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
	}

	var book []Book
	db.Preload("Book").First(&book, bookId)

	var err1 error
	err1 = json.NewEncoder(w).Encode(book)
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

func updateBookAvailability(w http.ResponseWriter, r *http.Request) {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var book Book
	var err error
	err = json.NewDecoder(r.Body).Decode(&book)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	db.Save(&book)
	w.Header().Set("Content-Type", "application/json")

	var err1 error
	err1 = json.NewEncoder(w).Encode(book)
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

func addBookAvailability(w http.ResponseWriter, r *http.Request) {
	var erro error
	erro = initDB()
	if erro != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var book Book
	var err error
	err = json.NewDecoder(r.Body).Decode(&book)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	db.Save(&book)
	w.Header().Set("Content-Type", "application/json")

	var err1 error
	err1 = json.NewEncoder(w).Encode(book)
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

func deleteBooksAvailabilityId(w http.ResponseWriter, r *http.Request) {
	var err error
	err = initDB()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	params := mux.Vars(r)
	bookId := params["bookId"]
	id64, _ := strconv.ParseUint(bookId, 10, 64)
	idToDel := uint(id64)

	db.Where("id = ?", idToDel).Delete(&Book{})

	w.WriteHeader(http.StatusNoContent)

	var err2 error
	err2 = db.Close()
	if err2 != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}
