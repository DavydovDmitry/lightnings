#!/usr/bin/expect

spawn pg_dump \
--dbname=$env(DB_NAME) \
--host=$env(DB_IP) \
--port=$env(DB_PORT) \
--username=$env(DB_USER) 

expect "Password: "
send "$env(DB_PASSWORD)\n"
interact
