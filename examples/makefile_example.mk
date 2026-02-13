# Example: Makefile with Sound Notifications
#
# This Makefile demonstrates how to add audio feedback to build tasks.
# Copy the play_sound function and use it in your targets.
#
# Usage:
#   make build
#   make test
#   make deploy

.PHONY: help build test clean deploy all

SOUND_SERVER := http://localhost:9091

# Helper function to play sounds
define play_sound
	@curl -s -X POST $(SOUND_SERVER)/play \
		-H 'Content-Type: application/json' \
		-d '{"sound":"$(1)", "volume":$(2)}' > /dev/null 2>&1 || true
endef

help:
	@echo "Available targets:"
	@echo "  make build   - Build the project"
	@echo "  make test    - Run tests"
	@echo "  make clean   - Clean build artifacts"
	@echo "  make deploy  - Deploy to production"
	@echo "  make all     - Build and test"

# Build target with notifications
build:
	@echo "🔨 Building project..."
	$(call play_sound,build-start.mp3,0.7)
	@sleep 2  # Simulate build
	@echo "✅ Build complete!"
	$(call play_sound,build-success.mp3,1.0)

# Test target with error handling
test:
	@echo "🧪 Running tests..."
	$(call play_sound,test-start.mp3,0.7)
	@if pytest tests/ ; then \
		echo "✅ All tests passed!" ; \
		$(call play_sound,test-success.mp3,1.0) ; \
	else \
		echo "❌ Tests failed!" ; \
		$(call play_sound,test-failed.mp3,1.0) ; \
		exit 1 ; \
	fi

# Clean target
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info __pycache__
	@echo "✨ Clean complete!"
	$(call play_sound,notification.mp3,0.5)

# Deploy target with multiple notifications
deploy: build test
	@echo "🚀 Deploying to production..."
	$(call play_sound,deploy-start.mp3,0.8)
	@sleep 2  # Simulate deployment
	@if [ $$? -eq 0 ]; then \
		echo "✅ Deployment successful!" ; \
		$(call play_sound,deploy-success.mp3,1.0) ; \
	else \
		echo "❌ Deployment failed!" ; \
		$(call play_sound,deploy-failed.mp3,1.0) ; \
		exit 1 ; \
	fi

# Compound target
all: clean build test
	@echo "✅ All tasks complete!"
	$(call play_sound,all-complete.mp3,1.0)

# Advanced: Progress notifications
long-task:
	@echo "⏳ Starting long task..."
	$(call play_sound,start.mp3,0.7)
	@for i in 1 2 3 4 5; do \
		echo "  Step $$i/5..." ; \
		sleep 1 ; \
		$(call play_sound,tick.mp3,0.3) ; \
	done
	@echo "✅ Long task complete!"
	$(call play_sound,complete.mp3,1.0)

# Example: Different sounds for different outcomes
risky-operation:
	@echo "⚠️  Attempting risky operation..."
	$(call play_sound,warning.mp3,0.8)
	@if ./scripts/risky-script.sh ; then \
		$(call play_sound,success.mp3,1.0) ; \
	else \
		$(call play_sound,error.mp3,1.0) ; \
		exit 1 ; \
	fi
