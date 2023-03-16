REG_URL=chica.fisica.ufmg.br:5000
IMG_TAG?=$(REG_URL)/simlab

containers/%.sif: defs/%.def
	mkdir -p ./containers
	apptainer build $@ $<

upload:
	#docker save $(IMG_TAG):latest | bzip2 | pv | ssh -p 22 root@10.0.1.2 docker load
	docker push $(IMG_TAG) 

bash:
	docker run --rm -ti --entrypoint /bin/bash $(IMG_TAG)

build:
	DOCKER_BUILDKIT=1 docker build . --tag $(IMG_TAG)
.PHONY: build
