#! /bin/bash
ch chatserver/ && killall python && git pull https://github.com/gnivciv/Chat_Programm/ > update_log.txt && ./start_server.sh 
