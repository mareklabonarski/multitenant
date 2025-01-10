#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <file_to_watch> <process_command>"
    exit 1
fi

FILE_TO_WATCH="$1"

PROCESS_COMMAND="$2"

start_process() {
    $PROCESS_COMMAND &
    echo $!
}

restart_process() {
    if [[ -n "$PROCESS_PID" ]]; then
        kill "$PROCESS_PID" 2>/dev/null
        echo "Process with PID $PROCESS_PID has been terminated."
    fi

    PROCESS_PID=$(start_process)
    echo "Process restarted with PID $PROCESS_PID."
}

if ! command -v inotifywait &> /dev/null; then
    echo "inotifywait could not be found. Please install inotify-tools."
    exit 1
fi

PROCESS_PID=$(start_process)
echo "Watching for changes on $FILE_TO_WATCH..."

while inotifywait -e modify "$FILE_TO_WATCH"; do
    echo "Changes detected on $FILE_TO_WATCH."
    restart_process
done
