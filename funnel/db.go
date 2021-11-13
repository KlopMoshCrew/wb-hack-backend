package main

import (
	"database/sql"
	"fmt"

	_ "github.com/lib/pq"
)

func (a *application) initDB() error {
	db, err := sql.Open("postgres", a.cfg.DbDataSource)
	if err != nil {
		return fmt.Errorf("open db conn: %w", err)
	}

	if err := db.Ping(); err != nil {
		return fmt.Errorf("ping db: %v", err)
	}

	a.db = db

	return nil
}
