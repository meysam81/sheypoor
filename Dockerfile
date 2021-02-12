# STAGE 0: base image
FROM python:3.9-alpine AS base

LABEL author="Meysam Azad <MeysamAzad81@yahoo.com>"

ARG WHEELDIR=/wheelhouse
ARG BUILDDIR=/build

ENV BUILDDIR=${BUILDDIR} \
    WHEELDIR=${WHEELDIR}

RUN pip install -U pip


# STAGE 1: fetch dependencies
FROM base AS build

RUN \
    apk update && \
    apk add gcc musl-dev libffi-dev

COPY requirements.txt ${BUILDDIR}/
RUN pip wheel -r ${BUILDDIR}/requirements.txt -w ${WHEELDIR}


# STAGE 2: run the server
FROM base AS run

ARG ENV=development
ARG USER=sheypoor
ARG WORKDIR=/service
ARG SERVICE_PORT=8000
ARG DUMB_INIT="https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64"
ARG DUMB_INIT_BIN="/usr/local/bin/dumb-init"
ARG GUSO="https://github.com/tianon/gosu/releases/download/1.12/gosu-amd64"
ARG GUSO_BIN="/usr/local/bin/guso"
ARG ENV_FILE=./.env

RUN apk add curl && \
    curl -sLo ${DUMB_INIT_BIN} ${DUMB_INIT} && \
    curl -sLo ${GUSO_BIN} ${GUSO} && \
    chmod +x ${DUMB_INIT_BIN} ${GUSO_BIN}

RUN adduser -DH ${USER}

ENV USER=${USER} \
    SERVICE_PORT=${SERVICE_PORT} \
    ENV=${ENV} \
    PYTHONWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

WORKDIR ${WORKDIR}
EXPOSE ${SERVICE_PORT}

COPY --from=build ${BUILDDIR} ${BUILDDIR}
COPY --from=build ${WHEELDIR} ${WHEELDIR}

RUN pip install -U \
    --no-cache-dir \
    -f ${WHEELDIR} \
    -r ${BUILDDIR}/requirements.txt && \
    chown ${USER}:${USER} ${WORKDIR} && \
    rm -rf ${BUILDDIR} ${WHEELDIR}

COPY --chown=${USER} ./app ./app/
COPY --chown=${USER} ./entrypoint.sh .
COPY --chown=${USER} ${ENV_FILE} ./.env

ENTRYPOINT [ "/usr/local/bin/dumb-init", "--" ]

CMD [ "sh", "./entrypoint.sh" ]
