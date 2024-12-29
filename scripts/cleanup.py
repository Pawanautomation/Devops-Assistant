import subprocess
import time
import os

def run_command(cmd, description=None):
    """Execute a shell command and print its output"""
    if description:
        print(f"\n=== {description} ===")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            text=True,
            capture_output=True
        )
        
        if result.stdout.strip():
            print(result.stdout)
        
        if result.stderr.strip():
            print(f"Warning/Error: {result.stderr}")
            
        return result.returncode == 0
    except Exception as e:
        print(f"Error executing command: {e}")
        return False

def cleanup_docker():
    """Clean up Docker resources"""
    commands = [
        "docker-compose down -v",
        "docker system prune -f --volumes",
        "docker volume prune -f",
        "docker network prune -f"
    ]
    
    for cmd in commands:
        run_command(cmd, f"Running: {cmd}")
        time.sleep(2)

def start_services():
    """Start all services and verify their status"""
    if not run_command("docker-compose up -d", "Starting services"):
        print("Failed to start services")
        return False
    
    print("\nWaiting for services to initialize...")
    time.sleep(30)  # Give services time to start
    
    return run_command("docker-compose ps", "Checking service status")

def verify_services():
    """Verify that all services are running correctly"""
    checks = [
        ("docker-compose ps", "Container Status"),
        ("curl -s localhost:54322", "PostgreSQL Connection"),
        ("curl -s localhost:19530", "Milvus Connection"),
        ("curl -s localhost:54323", "Studio Connection")
    ]
    
    for cmd, desc in checks:
        if not run_command(cmd, desc):
            print(f"Warning: {desc} check failed")

def main():
    print("Starting DevOps Assistant setup...")
    
    # 1. Clean up existing resources
    print("\nStep 1: Cleaning up existing resources")
    cleanup_docker()
    
    # 2. Start services
    print("\nStep 2: Starting services")
    if not start_services():
        print("Failed to start services properly")
        run_command("docker-compose logs", "Service Logs")
        return
    
    # 3. Verify services
    print("\nStep 3: Verifying services")
    verify_services()
    
    print("\nSetup complete! Use 'docker-compose logs' to check for any issues.")

if __name__ == "__main__":
    main()