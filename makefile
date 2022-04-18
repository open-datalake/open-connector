# Global variables
$(eval S3_BUCKET="docs.joffreybvn.be")
$(eval LIBRARY_NAME="mailxtract")

.SILENT: build
.PHONY: build

dev-env:
	echo "Install dev dependencies"
	pip install -r requirements.dev.txt

doc:
	echo "Build documentation"
	cd ./docs; \
	rm -rf build; \
	make html

doc-push:
	echo "Upload documentation to S3"
	aws s3 sync ./docs/build/html s3://$(S3_BUCKET)/$(LIBRARY_NAME)

test:
	echo "Running Pytest with coverage"
	pytest --cov=typer tests/

monkey-type:
	echo "Run the code and generates types"
	monkeytype run scripts/monkey_type.py

monkey-apply:
	echo "Edit code files with the types"
	monkeytype apply typer.type.athena
	monkeytype apply typer.typer.big_query
	monkeytype apply typer.typer.pandas
	monkeytype apply typer.type

pure:
	echo "Update requirements versions"
	pur -r requirements.txt
	pur -r requirements-dev.txt

safe:
	echo "Check dependencies vulnerabilities"
	safety check

layer:
	# Source: https://github.com/aws-samples/aws-lambda-layer-builder
	# May require chmod +x ./aws-layers/make-layer.sh
	sh ./aws-layers/make-layer.sh open_connector_s3_s3 python3.8 ./aws-layers/s3_s3.txt

build:
	@echo "Building open-connector"
	python setup.py -q sdist bdist_wheel

	@echo "Building source-s3"
	cd ./connectors/source_s3/; \
	python setup.py -q sdist bdist_wheel
	@mv -v ./connectors/source_s3/dist/* ./dist/

	@echo "Building destination-s3"
	cd ./connectors/destination_s3/; \
	python setup.py -q sdist bdist_wheel
	@mv -v ./connectors/destination_s3/dist/* ./dist/

	@echo "Uploading and indexing to: pypi.joffreybvn.be"
	s3pypi dist/* --bucket pypi.joffreybvn.be --put-root-index --force --verbose --profile private

dev-dependencies:
	pip install -r requirements.dev.txt