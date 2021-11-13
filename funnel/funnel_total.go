package main

import (
	"database/sql"
	"errors"
	"net/http"
	"time"
)

const (
	totalSQL = `
select
    sum(case when ecom_event_action = 'begin_checkout' then 1 else 0 end) as begin_checkout_summ,
    sum(case when ecom_event_action = 'add_to_cart' then 1 else 0 end) as add_to_cart_summ,
    sum(case when ecom_event_action = 'purchase' then 1 else 0 end) as purchase_summ,
    sum(case when ecom_event_action = 'view_item_list' then 1 else 0 end) as view_item_list_summ,
    sum(case when ecom_event_action = 'remove_from_cart' then 1 else 0 end) as remove_from_cart_summ,
    sum(case when ecom_event_action = 'view_item' then 1 else 0 end) as view_item_summ
FROM 
    public.wb_hack_parsed
WHERE 
    ecom_id = $1::text
    and 
    (utc_event_date) 
        between  
        $2::date 
        and  
        $3::date
`
	fieldsCount = 6
)

var null = 0

type responseCombo struct {
	BeginCheckout  *int `json:"begin_checkout"`
	AddToCart      *int `json:"add_to_cart"`
	Purchase       *int `json:"purchase"`
	ViewItemList   *int `json:"view_item_list"`
	RemoveFromCart *int `json:"remove_from_cart"`
	ViewItem       *int `json:"view_item"`
}

func (a *application) funnelTotalHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")

	if len(id) == 0 {
		a.sendResponse(w, http.StatusBadRequest, "id requiered")
		return
	}

	fromDt := r.URL.Query().Get("from")
	from, err := time.Parse(dateLayout, fromDt)
	if err != nil {
		a.sendResponse(w, http.StatusBadRequest, "invalid from")
		return
	}

	toDt := r.URL.Query().Get("to")
	to, err := time.Parse(dateLayout, toDt)
	if err != nil {
		a.sendResponse(w, http.StatusBadRequest, "invalid to")
		return
	}

	if from.After(to) {
		a.sendResponse(w, http.StatusBadRequest, "from after to")
		return
	}

	var out responseCombo

	if err := a.db.QueryRow(r.Context(), totalSQL, id, from.Format(dateLayout), to.Format(dateLayout)).Scan(
		&out.BeginCheckout,
		&out.AddToCart,
		&out.Purchase,
		&out.ViewItemList,
		&out.RemoveFromCart,
		&out.ViewItem,
	); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			a.sendResponse(w, http.StatusNotFound, "no data")
		} else {
			a.log.Errorf("can't get row for funnel total: %v", err)
			a.sendResponse(w, http.StatusInternalServerError, "can't get funnel total")
		}
		return
	}

	nullCount := 0
	if out.BeginCheckout == nil {
		out.BeginCheckout = &null
		nullCount++
	}
	if out.AddToCart == nil {
		out.AddToCart = &null
		nullCount++
	}
	if out.Purchase == nil {
		out.Purchase = &null
		nullCount++
	}
	if out.ViewItemList == nil {
		out.ViewItemList = &null
		nullCount++
	}
	if out.RemoveFromCart == nil {
		out.RemoveFromCart = &null
		nullCount++
	}
	if out.ViewItem == nil {
		out.ViewItem = &null
		nullCount++
	}

	if nullCount == 6 {
		a.sendResponse(w, http.StatusNotFound, "no data")
		return
	}

	a.sendResponse(w, http.StatusOK, out)
}
