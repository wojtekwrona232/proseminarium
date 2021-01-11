package main

import (
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"github.com/jinzhu/gorm"
)

type Courier struct {
	Id uint `json:"id" gorm:"primary_key"`
	Name string `json:"name"`
}

type Package struct {
	Id                uint    `json:"id" gorm:"primary_key"`
	IdLibrarySender   string  `json:"id_library_sender"`
	IdLibraryReceiver string  `json:"id_library_receiver"`
	IdBook            uint    `json:"id_book"`
	IdCourier         uint    `json:"id_courier"`
	Courier           Courier `json:"courier" gorm:"ForeignKey:id_courier"`
	PackageNumber	  string  `json:"package_number"`
	DeliveryStage	  string  `json:"delivery_stage"`
}

var db *gorm.DB

func initDB() (err error) {
	dataSourceName := "root:@tcp(localhost:3306)/transportmicroservice"
	db, err = gorm.Open("mysql", dataSourceName)

	if err != nil {
		fmt.Println(err)
		return
	}

	db.AutoMigrate(&Package{}, &Courier{})
	return
}
