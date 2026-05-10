BINARY := album2vid
CMD := ./cmd/album2vid

.PHONY: build run

build:
	go build -ldflags="-s -w" -o $(BINARY) $(CMD)

run: build
	./$(BINARY) $(ARGS)
