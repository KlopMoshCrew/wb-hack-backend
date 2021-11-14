package main

import (
	"net/http"
)

const (
	itemsSQL = `SELECT ec.id, bn.name, ec.variant
	FROM public.ecom ec
	LEFT JOIN public.brand_names bn ON ec.brand = bn.brand where ec.id in (
		'8360E6D158AEBD26BBBE835C38F88748',
'97F9B1135CF24F4CFFF4664435AEC2B9',
'B0270133170E1B886F4FA77B7E1F0EB9',
'A6FC1D41C2A36CD6ED1428BC40991F3A',
'BDBD23C5359EF7B3F85763C032892B85',
'C0C9F2DC21904776545FFBB2FC3D646C',
'6050B6B1F05ABDB4B33DA4BCEB46DE9B',
'61F3488FEF9234C5B0E9B68CAF0AB51F',
'0F49D92CEA8C80166B0605ED3D1A8E5D',
'ECD8847A3E389369BA25918DFF9B5B83',
'7D9A98C6E8BF033613B74252D9D24B33',
'AF51FBD3B09A5BE324C76C524118BFD3',
'5C8925190BE8C493517153B561BA21E7',
'B3A955CA48D147C9C9D7795DC736464D',
'67FC8BB094EC6205479255C1F8028E20',
'BF4304D1BE666DB38DF823DE35823D4D',
'AC688D3B8E8D812E2B49496BE59286E3',
'9EC302050B63C90533F9FFBCAC489DD8',
'6D88AAEEAB611F290D931ACCC12045CB',
'6BDA30FE61747A5C2FA82F13843104A8'
	)`
)

type responseItem struct {
	ID      string `json:"id"`
	Brand   string `json:"name"`
	Variant string `json:"variant"`
}

func (a *application) items(w http.ResponseWriter, r *http.Request) {
	// limit := 20
	// offset := 0

	// if l, err := strconv.Atoi(r.URL.Query().Get("limit")); err == nil {
	// 	limit = l
	// }

	// if o, err := strconv.Atoi(r.URL.Query().Get("page")); err == nil {
	// 	offset = (o - 1) * limit
	// }

	rows, err := a.db.QueryContext(r.Context(), itemsSQL)
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
