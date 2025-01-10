#!/bin/bash


args=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --database)
            # If --database is specified, grab the next argument (the database name)
            if [[ -n "$2" ]]; then
                DB_NAME="$2"
                shift 2
            else
                echo "Error: --database requires a value."
                exit 1
            fi
            ;;
        *)

            args+=("$1")
            shift
            ;;
    esac
done

if [[ -n "$DB_NAME" ]]; then
    args=(--database "$DB_NAME" "${args[@]}")
fi

# Check if Docker is installed
if command -v docker &> /dev/null
then
    # If Docker is installed, run the migrate command inside the web service
    docker-compose exec web python manage.py migrate "${args[@]}"
else
    # If Docker is not installed, run the migrate command directly
    python manage.py migrate "${args[@]}"
fi

#docker compose exec web python manage.py migrate "${args[@]}"
