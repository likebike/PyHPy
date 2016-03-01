# This is the PyHPy Project Makefile.
# Adjust this Makefile to suit your project requirements.

# Find the location of this Makefile (this method works with 'make -C', but maybe not with 'make -f'.):
THIS_MAKEFILE=$(CURDIR)/$(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
MAKEFILE_DIR=$(patsubst %/,%,$(dir $(THIS_MAKEFILE)))

# We use the Makefile location to guess our project root and PyHPy location:
PROJ_ROOT=${MAKEFILE_DIR}
PYHPY_DIR=${MAKEFILE_DIR}

# Directory locations:
SCRIPTS_DIR=${PROJ_ROOT}/1_scripts
IN_DIR=${PROJ_ROOT}/2_input
BUILD_DIR=${PROJ_ROOT}/3_build
OUT_DIR=${PROJ_ROOT}/4_output
OUT_DEV_DIR=${OUT_DIR}/dev
OUT_PROD_DIR_NAME=prod-$(shell date '+%Y%m%d%H%M%S')
OUT_PROD_DIR=${OUT_DIR}/${OUT_PROD_DIR_NAME}
OUT_PROD_SYMLINK=${OUT_DIR}/prod

# The port and docroot of the development HTTP server:
WWW_PORT=8000
WWW_DIR=${OUT_DEV_DIR}

# Long commands that I use multiple times:
COPY=rsync -aHAX

# Build the development site:
# We use 'find' instead of 'rm -rf' to preserve existing directory structure.
# This is less confusing for users who rebuild a project while viewing
# outputs -- they don't end up in a detached filesystem node.
dev:
	find "${BUILD_DIR}" -not -type d -delete
	find "${OUT_DEV_DIR}" -not -type d -delete
	${COPY} "${IN_DIR}/" "${BUILD_DIR}"
	"${PYHPY_DIR}/bin/build" "${SCRIPTS_DIR}" "${BUILD_DIR}" "${OUT_DEV_DIR}"
	@echo
	@echo "DEV Built Successfully!  Output is at: ${OUT_DEV_DIR}"
	@echo

# Copy 'dev' to 'prod':
prod: dev
	${COPY} "${OUT_DEV_DIR}/" "${OUT_PROD_DIR}"
	ln -sfn "${OUT_PROD_DIR_NAME}" "${OUT_PROD_SYMLINK}"
	@echo
	@echo "PROD Built Successfully!  Output is at: ${OUT_PROD_SYMLINK}"
	@echo

# Useful for local development and testing:
server:
	"${PYHPY_DIR}/bin/server" "${WWW_PORT}" "${WWW_DIR}"


