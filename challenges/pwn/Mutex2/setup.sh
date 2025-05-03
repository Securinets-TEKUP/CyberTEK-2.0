#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Banner
echo -e "${GREEN}"
echo "===================================="
echo "    Mutex CTF Challenge Setup     "
echo "===================================="
echo -e "${NC}"

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed.${NC}"
        echo "Please install Docker first:"
        echo "  https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Error: Docker Compose is not installed.${NC}"
        echo "Please install Docker Compose first:"
        echo "  https://docs.docker.com/compose/install/"
        exit 1
    fi
}

# Function to start the challenge
start_challenge() {
    echo -e "${YELLOW}Starting Mutex CTF Challenge...${NC}"
    docker-compose up -d
    
    # Check if container is running
    if [ "$(docker ps -q -f name=mutex-challenge)" ]; then
        echo -e "${GREEN}Challenge is now running!${NC}"
        IP=$(hostname -I | awk '{print $1}')
        echo -e "Challenge is available at: ${GREEN}$IP:6002${NC}"
    else
        echo -e "${RED}Failed to start the challenge container.${NC}"
        echo "Check logs with: docker-compose logs"
    fi
}

# Function to stop the challenge
stop_challenge() {
    echo -e "${YELLOW}Stopping Mutex CTF Challenge...${NC}"
    docker-compose down
    echo -e "${GREEN}Challenge stopped successfully.${NC}"
}

# Function to show status
status_challenge() {
    if [ "$(docker ps -q -f name=mutex-challenge)" ]; then
        echo -e "${GREEN}Challenge is running!${NC}"
        IP=$(hostname -I | awk '{print $1}')
        echo -e "Challenge is available at: ${GREEN}$IP:6002${NC}"
        
        # Show container stats
        echo -e "\n${YELLOW}Container Stats:${NC}"
        docker stats mutex-challenge --no-stream
    else
        echo -e "${RED}Challenge is not running.${NC}"
    fi
}

# Function to show logs
logs_challenge() {
    echo -e "${YELLOW}Challenge Logs:${NC}"
    docker-compose logs --tail=100
}

# Check if Docker is installed
check_docker

# Parse command line arguments
case "$1" in
    start)
        start_challenge
        ;;
    stop)
        stop_challenge
        ;;
    restart)
        stop_challenge
        start_challenge
        ;;
    status)
        status_challenge
        ;;
    logs)
        logs_challenge
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo "  start   - Start the challenge container"
        echo "  stop    - Stop the challenge container"
        echo "  restart - Restart the challenge container"
        echo "  status  - Check if the challenge is running"
        echo "  logs    - Show challenge container logs"
        exit 1
esac

exit 0
