package main

import (
	"fmt"
	"os"

	_ "github.com/go-sql-driver/mysql"
	"github.com/jinzhu/gorm"
)

type Reservation struct {
	Id              uint   `json:"id" gorm:"primary_key,AUTO_INCREMENT"`
	ReservationDate string `json:"reservation_date"`
	PickUpDate      string `json:"pick_up_date"`
	Status          string `json:"status"`
}

type Book struct {
	Id        uint   `json:"id" gorm:"primary_key,AUTO_INCREMENT"`
	Isbn      string `json:"isbn"`
	Available bool   `json:"available"`
}

type CheckOut struct {
	Id                uint        `json:"id" gorm:"primary_key,AUTO_INCREMENT"`
	ReservationId     uint        `json:"reservation_id"`
	Reservation       Reservation `json:"reservation" gorm:"ForeignKey:reservation_id"`
	BookId            uint        `json:"book_id"`
	Book              Book        `json:"book" gorm:"ForeignKey:book_id"`
	ReaderId          string      `json:"reader_id"`
	EmployeeId        string      `json:"employee_id"`
	CheckOutDate      string      `json:"check_out_date"`
	ReturnDate        string      `json:"return_date"`
	ReturnTerm        string      `json:"return_term"`
	LateReturnPenalty float32     `json:"late_return_penalty"`
}

var db *gorm.DB

func initDB() (err error) {
	dataSourceName := "root:Ic3P3dZUvid9YdKAb-@P3JaDOp4B@tcp(" + os.Getenv("DB_HOST") + ":3306)/libraryB"
	db, err = gorm.Open("mysql", dataSourceName)

	if err != nil {
		fmt.Println(err)
		return
	}

	db.AutoMigrate(&Reservation{}, &Book{}, &CheckOut{})
	return
}
