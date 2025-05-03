
BINARY_NAME := uploo
BINARY_PATH := /usr/bin/$(BINARY_NAME)
BINARY_TEST_PATH := ./binary/$(BINARY_NAME)


.PHONY: build
build:
	@go build -o $(BINARY_TEST_PATH) -v

.PHONY: build-di
build-di:
	@docker build -t spidrx/uploo .

#todo
.PHONY: deploy-image
deploy-image:
	@docker login 

.PHONY: install-deps
install-deps:
	@go mod tidy
