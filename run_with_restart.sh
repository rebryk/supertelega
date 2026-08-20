#!/bin/bash

MAX_WAIT=3600  # Maximum wait time in seconds (1 hour)
INITIAL_WAIT=120  # Initial wait time in seconds (2 minutes)
BACKOFF_FACTOR=2  # Multiplier for wait time after each crash

wait_time=$INITIAL_WAIT

while true; do
    python main.py --auto-archive
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "Script completed successfully. Exiting."
        break
    else
        echo "Script crashed. Restarting in $wait_time seconds..."
        sleep $wait_time

        # Increase wait time for next iteration, but cap at MAX_WAIT
        wait_time=$((wait_time * BACKOFF_FACTOR))
        if [ $wait_time -gt $MAX_WAIT ]; then
            wait_time=$MAX_WAIT
        fi
    fi
done

