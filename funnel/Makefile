build:
	go build -mod vendor -o .bin/api

run:build
	FUNNEL_API_PORT=:1337 .bin/api

clean:
	rm -rf .bin