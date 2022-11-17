build:
	DOCKER_BUILDKIT=1 docker build -t simlab-sample:latest .

.PHONY: build