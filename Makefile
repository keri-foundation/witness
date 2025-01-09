
.PHONY: build-witness

VERSION=1.0.0-dev0

define DOCKER_WARNING
In order to use the multi-platform build enable the containerd image store
The containerd image store is not enabled by default.
To enable the feature for Docker Desktop:
	Navigate to Settings in Docker Desktop.
	In the General tab, check Use containerd for pulling and storing images.
	Select Apply and Restart."
endef

build-witness: .warn
	@docker build --platform=linux/amd64,linux/arm64 -t ghcr.io/keri-foundation/witness:$(VERSION) .

publish-witness:
	@docker push ghcr.io/keri-foundation/witness:$(VERSION)

.warn:
	@echo -e ${RED}"$$DOCKER_WARNING"${NO_COLOUR}

RED="\033[0;31m"
NO_COLOUR="\033[0m"
export DOCKER_WARNING

check:
	uv run ruff check

fmt:
	uv run ruff format