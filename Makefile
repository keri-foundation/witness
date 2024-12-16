
.PHONY: build-witness

VERSION=1.2.0

define DOCKER_WARNING
In order to use the multi-platform build enable the containerd image store
The containerd image store is not enabled by default.
To enable the feature for Docker Desktop:
	Navigate to Settings in Docker Desktop.
	In the General tab, check Use containerd for pulling and storing images.
	Select Apply and Restart."
endef

build-witness: .warn
	@docker build --platform=linux/amd64,linux/arm64 -f images/keripy.dockerfile -t weboftrust/keri:$(VERSION) .

publish-witness:
	@docker push weboftrust/keri:$(VERSION)

.warn:
	@echo -e ${RED}"$$DOCKER_WARNING"${NO_COLOUR}

RED="\033[0;31m"
NO_COLOUR="\033[0m"
export DOCKER_WARNING
