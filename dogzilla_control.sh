#!/bin/bash
# Dogzilla S2 Quick Start Script

echo "🐕🦖 STARTING DOGZILLA S2 SERVICES"
echo "================================="

# Check if repository exists
if [ ! -d "/home/spencer/DogzillaRobot" ]; then
    echo "❌ DogzillaRobot repository not found!"
    echo "Please clone the repository first:"
    echo "git clone https://github.com/Dexterscat/DogzillaRobot.git"
    exit 1
fi

# Function to start Flask API
start_flask() {
    echo "🐍 Starting Dogzilla Flask API (port 5011)..."
    cd /home/spencer/DogzillaRobot/dogzilla_core
    
    # Check if virtual environment exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Start Flask server
    python3 mobile_api_server.py &
    FLASK_PID=$!
    echo "✅ Flask API started (PID: $FLASK_PID)"
    echo "📡 API available at: http://192.168.1.4:5011/"
}

# Function to start React interface
start_react() {
    echo "⚛️ Starting Dogzilla React Interface (port 5010)..."
    cd /home/spencer/DogzillaRobot/DogzillaVoiceControl
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing Node dependencies..."
        npm install
    fi
    
    # Start React dev server
    npm run dev &
    REACT_PID=$!
    echo "✅ React interface started (PID: $REACT_PID)"
    echo "🌐 Interface available at: http://192.168.1.4:5010/"
}

# Function to check if ports are available
check_ports() {
    echo "🔍 Checking port availability..."
    
    if netstat -tlnp 2>/dev/null | grep -q ":5010 "; then
        echo "⚠️ Port 5010 already in use"
        return 1
    fi
    
    if netstat -tlnp 2>/dev/null | grep -q ":5011 "; then
        echo "⚠️ Port 5011 already in use"
        return 1
    fi
    
    echo "✅ Ports 5010 and 5011 available"
    return 0
}

# Function to show status
show_status() {
    echo ""
    echo "🐕🦖 DOGZILLA STATUS DASHBOARD"
    echo "============================="
    
    # Check Flask API
    if curl -s http://192.168.1.4:5011/ > /dev/null 2>&1; then
        echo "✅ Flask API: ONLINE (http://192.168.1.4:5011/)"
    else
        echo "❌ Flask API: OFFLINE"
    fi
    
    # Check React interface
    if curl -s http://192.168.1.4:5010/ > /dev/null 2>&1; then
        echo "✅ React Interface: ONLINE (http://192.168.1.4:5010/)"
    else
        echo "❌ React Interface: OFFLINE"
    fi
    
    # Show Astra status for comparison
    echo ""
    echo "🤖 ASTRA STATUS (for comparison)"
    echo "==============================="
    
    if curl -s http://192.168.1.4:5001/ > /dev/null 2>&1; then
        echo "✅ Astra Flask API: ONLINE (http://192.168.1.4:5001/)"
    else
        echo "❌ Astra Flask API: OFFLINE"
    fi
    
    if curl -s http://192.168.1.4:5000/ > /dev/null 2>&1; then
        echo "✅ Astra React Interface: ONLINE (http://192.168.1.4:5000/)"
    else
        echo "❌ Astra React Interface: OFFLINE"
    fi
}

# Main execution
case "$1" in
    "start")
        check_ports
        if [ $? -eq 0 ]; then
            start_flask
            sleep 3
            start_react
            sleep 5
            show_status
        else
            echo "❌ Cannot start - ports in use"
            exit 1
        fi
        ;;
    "status")
        show_status
        ;;
    "stop")
        echo "🛑 Stopping Dogzilla services..."
        pkill -f "python.*mobile_api_server.py"
        pkill -f "npm.*dev"
        pkill -f "tsx.*server"
        echo "✅ Dogzilla services stopped"
        ;;
    "restart")
        $0 stop
        sleep 2
        $0 start
        ;;
    *)
        echo "🐕🦖 Dogzilla S2 Service Manager"
        echo ""
        echo "Usage: $0 {start|stop|restart|status}"
        echo ""
        echo "Commands:"
        echo "  start   - Start both Flask API and React interface"
        echo "  stop    - Stop all Dogzilla services"
        echo "  restart - Stop and start services"
        echo "  status  - Show current status of all services"
        echo ""
        echo "Dogzilla runs on ports 5010 (React) and 5011 (Flask)"
        echo "Astra runs on ports 5000 (React) and 5001 (Flask)"
        exit 1
        ;;
esac