.PHONY: run run-reloader reset-db server

# Run default configuration (see ./webserver.cfg)
# Use make run config=config/otherconfig.cfg to run a different config file.
config?=./webserver.cfg
run:
	bash -c "source ./venv/bin/activate; python main.py $(config)"

run-reloader:
	bash -c "source ./venv/bin/activate; python main.py config/local.reloader.cfg"


reset-db:
	cd sql; ./reset.bash; ./init.bash


server:
	rsync -a --cvs-exclude --exclude='venv' --exclude='backup' --exclude='docs' --exclude='data' --exclude='tests' --exclude='webserver.cfg' ../`basename $(PWD)`/* ubuntu@54.163.255.230:~/genderit
