#!/usr/bin/sh

wait_for_tcp()
{
  while true
  do
    echo $2
    curl -s -o /dev/null $1
    ret=$?
    [ $ret -eq 52 ] && break
    sleep 1
  done
}

wait_for_tcp $POSTGRES_HOST:5432 "Wait for $POSTGRES_HOST:5432..."

alembic upgrade head
uvicorn --host 0.0.0.0 main:app

