.PHONY: run

# Run default configuration (see ./webserver.cfg)
# Use make run config=config/otherconfig.cfg to run a different config file.
config?=./webserver.cfg
run:
	bash -c "source ./venv/bin/activate; python main.py $(config)"
