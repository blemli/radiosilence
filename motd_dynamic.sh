#!/bin/bash
last_login="$(last -F | grep -m 1 "$USER" | awk '{print $5, $6, $7, $8}' | xargs -I {} date -d {} +'%Y-%m-%d %H:%M:%S')"
if [ ! -z "$last_login" ]; then
    log_entries=$(journalctl --since "$last_login" --priority=err..emerg --unit=radiosilence.service --lines=3 --reverse --output=short | grep -v "No entries")
    if [ ! -z "$log_entries" ]; then
        echo "Errors since last login:"
        echo "$log_entries"
    fi
fi
