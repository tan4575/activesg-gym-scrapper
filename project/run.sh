#!/bin/bash
echo $1
source activate webscrapping
pid=$(pgrep -af "python3 $1/main.py" | awk '{print $1}')
echo $1/main.py
if [ -z "$pid" ]; then
    echo "No running Python processes found."
else
    echo $pid
    kill $pid
fi

cd $1

nohup python3 $1/main.py > run.log &
