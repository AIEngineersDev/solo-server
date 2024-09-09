APP := llamacpp_python
PORT ?= 8001
CHAT_FORMAT ?=

include ../common/Makefile.common

IMAGE_NAME ?= $(REGISTRY_ORG)/$(COMPONENT)/$(APP):latest
IMAGE := $(REGISTRY)/$(IMAGE_NAME)
CUDA_IMAGE := $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/$(APP)_cuda:latest
VULKAN_IMAGE := $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/$(APP)_vulkan:latest

MODELS_PATH := /locallm/models
MODEL_NAME ?= granite-7b-lab-Q4_K_M.gguf

.Phony: all
all: build download-model-granite run

.PHONY: build-cuda
build-cuda:
	"${CONTAINER_TOOL}"  build --squash-all -t $(CUDA_IMAGE) . -f cuda/Containerfile

.PHONY: build-vulkan-amd64 build-vulkan-arm64
build-vulkan-amd64:
	"${CONTAINER_TOOL}"  build --squash-all -t $(VULKAN_IMAGE) . -f vulkan/amd64/Containerfile
build-vulkan-arm64:
	"${CONTAINER_TOOL}"  build --squash-all -t $(VULKAN_IMAGE) . -f vulkan/arm64/Containerfile

.PHONY: download-model-granite # default model
download-model-granite:
	cd ../../models/ && \
	make download-model-granite
