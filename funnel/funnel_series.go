package main

import (
	"net/http"
	"time"

	"github.com/jackc/pgtype"
)

const (
	dateLayout = "2006-01-02"

	seriesSQL = `
select
	utc_event_date as "date",
    sum(case when ecom_event_action = 'begin_checkout' then 1 else 0 end) as begin_checkout_summ,
    sum(case when ecom_event_action = 'add_to_cart' then 1 else 0 end) as add_to_cart_summ,
    sum(case when ecom_event_action = 'purchase' then 1 else 0 end) as purchase_summ,
    sum(case when ecom_event_action = 'view_item_list' then 1 else 0 end) as view_item_list_summ,
    sum(case when ecom_event_action = 'remove_from_cart' then 1 else 0 end) as remove_from_cart_summ,
    sum(case when ecom_event_action = 'view_item' then 1 else 0 end) as view_item_summ
from 
    public.wb_hack_parsed
where 
    ecom_id = $1::text
	and utc_event_date is not null
    and (utc_event_date) between $2::date and $3::date
group by 
    utc_event_date
order by 
    utc_event_date
`
)

type responseSeries struct {
	responseCombo
	Date pgtype.Date `json:"date"`
}

func (a *application) funnelSeriesHandler(w http.ResponseWriter, r *http.Request) {
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

	rows, err := a.db.QueryContext(r.Context(), seriesSQL, id, from.Format(dateLayout), to.Format(dateLayout))
	if err != nil {
		a.log.Errorf("can't get rows for funnel series: %v", err)
		a.sendResponse(w, http.StatusInternalServerError, "can't get funnel series")
		return
	}
	defer rows.Close()

	var out []responseSeries

	for rows.Next() {
		var tmp responseSeries
		if err := rows.Scan(
			&tmp.Date,
			&tmp.BeginCheckout,
			&tmp.AddToCart,
			&tmp.Purchase,
			&tmp.ViewItemList,
			&tmp.RemoveFromCart,
			&tmp.ViewItem,
		); err != nil {
			a.log.Errorf("can't scan rows for funnel series: %v", err)
			a.sendResponse(w, http.StatusBadRequest, "can't get funnel series")
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
