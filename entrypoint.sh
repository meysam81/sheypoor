test -f .env && . .env || ( exit 1 && echo .env not found )


guso ${USER} uvicorn --host ${HOST:-0.0.0.0} --port ${PORT:-8000} ${RELOAD} ${MODULE_NAME}:app
