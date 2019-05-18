#!/usr/bin/expect

log_user 0

spawn psql \
--dbname=$env(DB_NAME) \
--host=$env(DB_IP) \
--port=$env(DB_PORT) \
--username=$env(DB_USER) < database/dumps/2019-05-17.dump

expect "Password: "
send "$env(DB_PASSWORD)\n"
interact
