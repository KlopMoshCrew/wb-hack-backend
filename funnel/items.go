package main

import (
	"net/http"
	"strconv"
)

const (
	itemsSQL = `select id, brand, variant from ecom limit $1 offset $2`
)

type responseItem struct {
	ID      string `json:"id"`
	Brand   string `json:"name"`
	Variant string `json:"variant"`
}

func (a *application) items(w http.ResponseWriter, r *http.Request) {
	limit := 20
	offset := 0

	if l, err := strconv.Atoi(r.URL.Query().Get("limit")); err == nil {
		limit = l
	}

	if o, err := strconv.Atoi(r.URL.Query().Get("page")); err == nil {
		offset = (o - 1) * limit
	}

	rows, err := a.db.QueryContext(r.Context(), itemsSQL, limit, offset)
	if err != nil {
		a.log.Errorf("can't get rows for items: %v", err)
		a.sendResponse(w, http.StatusInternalServerError, "can't get items")
		return
	}
	defer rows.Close()

	var out []responseItem

	for rows.Next() {
		var tmp responseItem
		if err := rows.Scan(
			&tmp.ID,
			&tmp.Brand,
			&tmp.Variant,
		); err != nil {
			a.log.Errorf("can't scan rows for items: %v", err)
			a.sendResponse(w, http.StatusBadRequest, "can't get items")
			return
		}

		out = append(out, tmp)
	}

	if len(out) == 0 {
		a.sendResponse(w, http.StatusNotFound, "no data")
		return
	}

	a.sendResponse(w, http.StatusOK, out)
}
