#!/bin/sh

# POSIX-compliant setup script for mypt Python development environment
# Based on setup_spec.md requirements

set -e  # Exit on any error

# Color constants for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_success() {
    printf "${GREEN}✅ %s${NC}\n" "$1"
}

log_error() {
    printf "${RED}❌ %s${NC}\n" "$1"
}

log_warning() {
    printf "${YELLOW}⚠️  %s${NC}\n" "$1"
}

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Step functions
check_dev_tools() {
    echo "📋 Checking development tools..."

    # Check Claude Code CLI
    if check_command "claude"; then
        CLAUDE_VERSION=$(claude --version 2>/dev/null || echo "unknown")
        log_success "Claude CLI installed: $CLAUDE_VERSION"
    else
        log_error "Claude CLI not found. Please install it using: npm install -g @anthropic-ai/claude-code"
    fi

    # Check Gemini CLI
    if check_command "gemini"; then
        log_success "Gemini CLI installed"
    else
        log_error "Gemini CLI not found. Please install it from: https://github.com/google/generative-ai-cli"
    fi

    # Check GitHub CLI
    if check_command "gh"; then
        GH_VERSION=$(gh --version 2>/dev/null | head -n1 || echo "unknown")
        log_success "GitHub CLI installed: $GH_VERSION"
    else
        log_error "GitHub CLI not found. Please install it using: brew install gh (macOS) or your package manager"
    fi

    # Check uv
    if check_command "uv"; then
        UV_VERSION=$(uv --version 2>/dev/null || echo "unknown")
        log_success "uv installed: $UV_VERSION"
    else
        log_error "uv not found. Please install it using: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
}

update_project_name() {
    echo "🔄 Updating project name..."
    
    # Derive project name from directory name
    DEFAULT_PROJECT_NAME=$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr '-' '_')
    
    # Check if update script exists
    if [ ! -f "scripts/update_project_name.py" ]; then
        log_warning "Project name update script not found, skipping project name update"
        return 0
    fi
    
    # Execute the Python script with error handling
    if uv run python scripts/update_project_name.py --new-name "$DEFAULT_PROJECT_NAME" >/dev/null 2>&1; then
        log_success "Project name updated to: $DEFAULT_PROJECT_NAME"
    else
        log_warning "Failed to update project name (continuing anyway)"
    fi
}

setup_python_env() {
    echo "🐍 Setting up Python environment..."

    # Read Python version from .python-version file
    if [ -f ".python-version" ]; then
        PYTHON_VERSION=$(cat .python-version | tr -d '[:space:]')
        log_success "Python version specified: $PYTHON_VERSION"
    else
        log_error ".python-version file not found"
        exit 1
    fi

    # Check if Python version is available
    if command -v "python$PYTHON_VERSION" >/dev/null 2>&1; then
        ACTUAL_VERSION=$(python$PYTHON_VERSION --version 2>&1 | cut -d' ' -f2)
        log_success "Python $ACTUAL_VERSION available"
    elif command -v python3 >/dev/null 2>&1; then
        ACTUAL_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        log_success "Python $ACTUAL_VERSION available"
    else
        log_error "Python $PYTHON_VERSION not found. Please install Python $PYTHON_VERSION"
        exit 1
    fi

    # Create virtual environment using uv
    echo "📦 Creating virtual environment..."
    if uv venv --python="$PYTHON_VERSION" >/dev/null 2>&1; then
        log_success "Virtual environment created"
    else
        log_warning "Failed to create venv with specific version, trying with default Python"
        if uv venv >/dev/null 2>&1; then
            log_success "Virtual environment created with default Python"
        else
            log_error "Failed to create virtual environment"
            exit 1
        fi
    fi
}

install_dependencies() {
    echo "📚 Installing dependencies..."

    if uv sync >/dev/null 2>&1; then
        log_success "Dependencies installed via uv sync"
    else
        log_error "Failed to install dependencies with uv sync"
        exit 1
    fi
}

setup_pre_commit() {
    echo "🪝 Setting up pre-commit hooks..."

    # Check if .pre-commit-config.yaml exists
    if [ ! -f ".pre-commit-config.yaml" ]; then
        log_warning ".pre-commit-config.yaml not found, skipping pre-commit setup"
    else
        # Install pre-commit hooks
        if uv run pre-commit install >/dev/null 2>&1; then
            log_success "Pre-commit hooks installed"
        else
            log_error "Failed to install pre-commit hooks"
            exit 1
        fi
        
        # Update pre-commit hooks
        if uv run pre-commit autoupdate >/dev/null 2>&1; then
            log_success "Pre-commit hooks updated"
        else
            log_warning "Failed to update pre-commit hooks (continuing anyway)"
        fi
    fi
}

init_git_repo() {
    echo "📁 Setting up Git repository..."

    # Check if already a git repository
    if [ -d ".git" ]; then
        log_success "Git repository already initialized"
    else
        # Initialize git repository
        if git init >/dev/null 2>&1; then
            log_success "Git repository initialized"
            
            # Optional: Create initial commit if base files exist
            if [ -f ".gitignore" ] && [ -f "pyproject.toml" ]; then
                git add .gitignore pyproject.toml CLAUDE.md setup.sh >/dev/null 2>&1 || true
                if git commit -m "Initial commit: project setup" >/dev/null 2>&1; then
                    log_success "Initial commit created"
                else
                    log_warning "Failed to create initial commit (continuing anyway)"
                fi
            fi
        else
            log_error "Failed to initialize git repository"
            exit 1
        fi
    fi
}

# Main function
main() {
    echo "🚀 Setting up Python development environment..."
    echo
    
    check_dev_tools
    update_project_name
    setup_python_env
    install_dependencies
    setup_pre_commit
    init_git_repo
    
    echo
    echo "🎉 Setup completed successfully!"
    echo
    echo "Next steps:"
    echo "  • Run 'make test' to verify everything works"
    echo "  • Run 'make format && make lint' to check code quality"
    echo "  • Start developing your Python project!"
    echo
}

# Execute main function
main