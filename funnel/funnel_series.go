package main

import (
	"net/http"
	"time"
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
	stackName = "stack1"
)

type responseSeriesV2 struct {
	Labels  []string   `json:"labels"`
	Dataset [6]dataset `json:"datasets"`
}

type dataset struct {
	Stack           string `json:"stack"`
	Label           string `json:"label"`
	BackgroundColor string `json:"backgroundColor"`
	Data            []int  `json:"data"`
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

	var out responseSeriesV2

	for i := from; to.After(i.AddDate(0, 0, -1)); i = i.AddDate(0, 0, 1) {
		out.Labels = append(out.Labels, i.Format(dateLayout))
	}

	out.Dataset = [6]dataset{
		{
			Stack:           stackName,
			Label:           "Просмотр в поисковой выдаче",
			BackgroundColor: "rgb(255, 0, 0)",
		},
		{
			Stack:           stackName,
			Label:           "Просмотр карточки товара",
			BackgroundColor: "rgb(0, 255, 0)",
		},
		{
			Stack:           stackName,
			Label:           "Добавление в корзину",
			BackgroundColor: "rgb(0, 0, 255)",
		},
		{
			Stack:           stackName,
			Label:           "Удаление из корзины",
			BackgroundColor: "rgb(255, 255, 0)",
		},
		{
			Stack:           stackName,
			Label:           "Оформление заказа",
			BackgroundColor: "rgb(255, 0, 255)",
		},
		{
			Stack:           stackName,
			Label:           "Выкуп",
			BackgroundColor: "rgb(0, 255, 255)",
		},
	}

	rows, err := a.db.QueryContext(r.Context(), seriesSQL, id, from.Format(dateLayout), to.Format(dateLayout))
	if err != nil {
		a.log.Errorf("can't get rows for funnel series: %v", err)
		a.sendResponse(w, http.StatusInternalServerError, "can't get funnel series")
		return
	}
	defer rows.Close()

	statMap := make(map[string]responseCombo)

	for rows.Next() {
		var tmp responseCombo
		var date time.Time
		if err := rows.Scan(
			&date,
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

		statMap[date.Format(dateLayout)] = tmp
	}

	// if len(statMap) == 0 {
	// 	a.sendResponse(w, http.StatusNotFound, "no data")
	// 	return
	// }

	for _, label := range out.Labels {
		stat := statMap[label]
		if stat.ViewItemList == nil || *stat.ViewItemList == 0 {
			out.Dataset[0].Data = append(out.Dataset[0].Data, 0)
		} else {
			out.Dataset[0].Data = append(out.Dataset[0].Data, *stat.ViewItemList)
		}
		if stat.ViewItem == nil || *stat.ViewItem == 0 {
			out.Dataset[1].Data = append(out.Dataset[1].Data, 0)
		} else {
			out.Dataset[1].Data = append(out.Dataset[1].Data, *stat.ViewItem)
		}
		if stat.AddToCart == nil || *stat.AddToCart == 0 {
			out.Dataset[2].Data = append(out.Dataset[2].Data, 0)
		} else {
			out.Dataset[2].Data = append(out.Dataset[2].Data, *stat.AddToCart)
		}
		if stat.RemoveFromCart == nil || *stat.RemoveFromCart == 0 {
			out.Dataset[3].Data = append(out.Dataset[3].Data, 0)
		} else {
			out.Dataset[3].Data = append(out.Dataset[3].Data, *stat.RemoveFromCart)
		}
		if stat.BeginCheckout == nil || *stat.BeginCheckout == 0 {
			out.Dataset[4].Data = append(out.Dataset[4].Data, 0)
		} else {
			out.Dataset[4].Data = append(out.Dataset[4].Data, *stat.BeginCheckout)
		}
		if stat.Purchase == nil || *stat.Purchase == 0 {
			out.Dataset[5].Data = append(out.Dataset[5].Data, 0)
		} else {
			out.Dataset[5].Data = append(out.Dataset[5].Data, *stat.Purchase)
		}
	}

	a.sendResponse(w, http.StatusOK, out)
}
