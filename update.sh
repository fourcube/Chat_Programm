#! /bin/bash
cd chatserver/ && killall python && git pull https://github.com/gnivciv/Chat_Programm/ && ./start_server.sh > log.txt 
