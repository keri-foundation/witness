# witness

Witnesses are a fundamental part of the "I" in KERI (Key Event Receipt Infrastructure - https://trustoverip.github.io/tswg-keri-specification/).  
They are the entities that are responsible for "receipting" events that are generated by the KERI.

Witness can be considered ephemeral keys used as part of the inception event to establish an Autonomic IDentifiers (AIDs).

## Acknowledgments

This project includes code originally authored by @pfeairheller and @SmithSamuelM, previously located in KERIpy.

- Original repository: https://github.com/weboftrust/keripy
- License: https://github.com/WebOfTrust/keripy/blob/main/LICENSE

We greatly appreciate their work, which laid the foundation for this project.

## Roadmap

- [] Promiscuous, single tenant witness with docker container
- [] Non-promiscuous witnesses.
- [] Witnesses with multifactor authentication
- [] Witnesses with alternate KEL endpoint for secure event publishing of controller
- [] Multi-tenant witness infrastructure.

## Prerequisites

This project uses [uv](https://docs.astral.sh/uv/).
Directions for installation can be found [here](https://docs.astral.sh/uv/getting-started/installation/).

## Getting Started

Witnesses require a keystore in order to be able to "receipt" events.
Using the command:

```shell
uv run witness init
```

Will create a keystore.

A local witness can be started with:

```shell
uv run witness start
```

## Deployment
