#! /bin/bash
cd chatserver/ && killall python && git pull https://github.com/gnivciv/Chat_Programm/ > log.txt && ./start_server.sh 
