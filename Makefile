# This is a PyHPy Project Makefile.

########  BASIC SETTINGS  (Adjust these.)  ########

# For example, if you are creating a site located at http://example.com/blog/... ,
# then URL_ROOT would be "/blog" or "http://example.com/blog".
# The default assumes that your site is located at http://example.com/...
export URL_ROOT=



########  ADVANCED STUFF  (You usually don't need to change these.)  ########

# Find the location of this Makefile (this method works with 'make -C', but maybe not with 'make -f'.):
THIS_MAKEFILE=$(CURDIR)/$(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
MAKEFILE_DIR=$(patsubst %/,%,$(dir $(THIS_MAKEFILE)))

# We use the Makefile location to guess our project root and PyHPy location:
PROJ_ROOT=${MAKEFILE_DIR}
PYHPY_DIR=${MAKEFILE_DIR}
MUCK_DIR=${PYHPY_DIR}/muck

# I assume that PATH is always set, so I prepend to it the easy way.
# But PYTHONPATH might not be set.  Don't use a ':' unless we need to:
export PATH:=${MUCK_DIR}/bin:${PATH}
export PYTHONPATH:=${PYHPY_DIR}/lib$(shell echo $${PYTHONPATH:+:$${PYTHONPATH:-}})

# Directory locations:
IN_NAME=1-input
IN_DIR=${PROJ_ROOT}/${IN_NAME}
BUILD_NAME=2-buildarea
BUILD_DIR=${PROJ_ROOT}/${BUILD_NAME}
OUT_DIR_NAME=3-output
DEV_NAME=dev
OUT_DEV_NAME=${OUT_DIR_NAME}/${DEV_NAME}
OUT_DEV_DIR=${PROJ_ROOT}/${OUT_DEV_NAME}
PROD_NAME=prod-$(shell date '+%Y%m%d%H%M%S')
OUT_PROD_NAME=${OUT_DIR_NAME}/${PROD_NAME}
OUT_PROD_DIR=${PROJ_ROOT}/${OUT_PROD_NAME}
OUT_PROD_SYMLINK_NAME=${OUT_DIR_NAME}/prod
OUT_PROD_SYMLINK=${PROJ_ROOT}/${OUT_PROD_SYMLINK_NAME}

# The port and docroot of the development HTTP server:
WWW_PORT=8000
WWW_DIR=${OUT_DEV_DIR}

# Tell 'make' that our targets aren't really files:
.PHONY: dev prod clean server

# Build the development site:
# We use 'find' instead of 'rm -rf' to preserve existing directory structure.
# This is less confusing for users who rebuild a project while viewing
# outputs -- they don't end up in a detached filesystem node.
dev:
	@echo Copying ${IN_NAME} '-->' ${BUILD_NAME}
	@rsync -aHAX "${IN_DIR}/" "${BUILD_DIR}"
	@echo Building ${BUILD_NAME} '-->' ${OUT_DEV_NAME}
	@muck "${BUILD_DIR}" "${OUT_DEV_DIR}"
	@echo
	@echo "DEV Built Successfully!  Output is at: ${OUT_DEV_DIR}"
	@echo

# Copy 'dev' to 'prod':
prod: dev
	@echo Copying ${OUT_DEV_NAME} '-->' ${OUT_PROD_NAME}
	@rsync -aHAX "${OUT_DEV_DIR}/" "${OUT_PROD_DIR}"
	@echo Updating ${OUT_PROD_SYMLINK_NAME} symlink
	@ln -sfn "${PROD_NAME}" "${OUT_PROD_SYMLINK}"
	@echo
	@echo "PROD Built Successfully!  Output is at: ${OUT_PROD_SYMLINK}"
	@echo

# Remove everything from the Build and Dev directories:
clean:
	@echo Cleaning ${BUILD_NAME} and ${OUT_DEV_NAME}
	-@find "${BUILD_DIR}" -not -type d -delete
	-@find "${OUT_DEV_DIR}" -not -type d -delete

# Useful for local development and testing:
server:
	"${PYHPY_DIR}/bin/server" "${WWW_PORT}" "${WWW_DIR}"


