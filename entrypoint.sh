#!/bin/sh

# Avvia Flask in background
python application.py &

# Avvia il Bot in background
python bot.py &

# Attende che i processi finiscano (se uno dei due muore, il container si ferma)
wait -n
