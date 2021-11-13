package main

import (
	"time"

	"github.com/kelseyhightower/envconfig"
)

type config struct {
	Port            string        `envconfig:"FUNNEL_API_PORT" default:":1337"`
	DbDataSource    string        `envconfig:"DB_DATA_SOURCE" default:"host=82.148.28.184 port=5432 dbname=test user=wb password=password sslmode=disable"`
	ShutdownTimeout time.Duration `envconfig:"APPLICATION_SHUTDOWN_TIMEOUT" default:"5s"`
}

func (a *application) initConfig() error {
	if err := envconfig.Process("", &a.cfg); err != nil {
		return err
	}
	return nil
}
