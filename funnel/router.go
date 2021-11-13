package main

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
)

func (a *application) newRouter() http.Handler {
	r := chi.NewRouter()

	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.SetHeader("Content-Type", "application/json"))
	r.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"https://*", "http://*"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: false,
		MaxAge:           300, // Maximum value not ignored by any of major browsers
	}))

	r.Get("/funnel/series", a.funnelSeriesHandler)
	r.Get("/funnel/total", a.funnelTotalHandler)
	r.Get("/items", a.items)

	return r
}

func (a *application) sendResponse(w http.ResponseWriter, responseCode int, v interface{}) {
	var (
		data []byte
		err  error
	)
	if responseCode/100 < 4 {
		data, err = json.Marshal(v)
	} else {
		data, err = json.Marshal(map[string]interface{}{"error": v})
	}

	if err != nil {
		a.log.Errorf("send response: marshal data: %w", err)
		return
	}

	w.WriteHeader(responseCode)
	if _, err := w.Write(data); err != nil {
		a.log.Errorf("send response: send response: %w", err)
		return
	}
}
