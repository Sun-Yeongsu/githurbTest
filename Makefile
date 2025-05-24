# DON'T ERASE THIS

PYTHON_VERSION := $(shell which python3)

DOCKER_REGISTRY := localhost:5000

DOCKER_IMAGE := python-multithreaded-calculator

DOCKER_VERSION := v$(shell date +%y.%m%d.%H%M)

docker-pull:
	docker pull ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:$(DOCKER_VERSION)

docker-build:
	DOCKER_BUILDKIT=1 docker build --rm -f ./Dockerfile \
	-t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:$(DOCKER_VERSION) \
	-t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest \
	.

docker-push:
	docker push -a ${DOCKER_REGISTRY}/${DOCKER_IMAGE}

run:
	docker run -it --rm ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest

.PHONY: docker-pull docker-build docker-push run

git-release:
	cd ~/docker_directory && \
	git checkout -B Branch_${DOCKER_VERSION} && \
	git add docker_file && \
	git commit -m "Release ${DOCKER_VERSION} for Python ${PYTHON_VERSION}" && \
	git push origin Branch_${DOCKER_VERSION}

setup:
	python3 -m pip install -r requirements.txt
