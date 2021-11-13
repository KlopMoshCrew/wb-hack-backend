package main

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v4"
)

func (a *application) initDB() error {
	db, err := pgx.Connect(context.Background(), a.cfg.DbDataSource)
	if err != nil {
		return fmt.Errorf("open db conn: %w", err)
	}

	a.db = db

	return nil
}
