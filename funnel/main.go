package main

import (
	"context"
	"net/http"

	"github.com/jackc/pgx/v4"
	"github.com/sirupsen/logrus"
)

type application struct {
	cfg config
	log *logrus.Logger
	db  *pgx.Conn
}

func main() {
	a := application{}
	a.initLogger()

	if err := a.initConfig(); err != nil {
		a.log.Fatalf("init config: %v", err)
	}

	if err := a.initDB(); err != nil {
		a.log.Fatalf("init db: %v", err)
	}
	defer a.db.Close(context.Background())

	a.log.Infof("api started on %s", a.cfg.Port)

	if err := http.ListenAndServe(a.cfg.Port, a.newRouter()); err != nil {
		a.log.Fatal(err)
	}
}

func (a *application) initLogger() {
	a.log = logrus.New()
	a.log.SetLevel(logrus.InfoLevel)
	a.log.SetFormatter(&logrus.TextFormatter{})
	a.log.SetReportCaller(true)
}
