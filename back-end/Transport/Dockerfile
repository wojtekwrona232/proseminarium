FROM golang:1.15.8 as builder
WORKDIR /go/src/app/main
COPY ./main .
RUN go get github.com/go-sql-driver/mysql
RUN go get github.com/gorilla/mux
RUN go get github.com/jinzhu/gorm
RUN go install
RUN GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -v
RUN cp main /
COPY transportmicroservice.sql docker-entrypoint-initdb.d/transportmicroservice.sql
ENTRYPOINT [ "/go/src/app/main/main" ]
