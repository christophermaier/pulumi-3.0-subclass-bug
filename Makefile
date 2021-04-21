setup: export PULUMI_CONFIG_PASSPHRASE=test
setup:
	pulumi stack init test --non-interactive
	pulumi stack select test
.PHONY: setup-two
setup-two: clean
	rm -Rf venv
	cp requirements-2.0.txt requirements.txt

.PHONY: setup-three
setup-three: clean
	rm -Rf venv
	cp requirements-3.0.txt requirements.txt

.PHONY: run-two
run-two: export PULUMI_CONFIG_PASSPHRASE=test
run-two: setup-two
	pulumi up --yes
	pulumi stack

.PHONY: run-three
run-three: export PULUMI_CONFIG_PASSPHRASE=test
run-three: setup-three
	pulumi up --yes
	pulumi stack

.PHONY: clean
run-three: export PULUMI_CONFIG_PASSPHRASE=test
clean:
	pulumi destroy --yes

.PHONY: destroy
destroy: export PULUMI_CONFIG_PASSPHRASE=test
destroy: clean
	pulumi stack rm test --preserve-config --yes
