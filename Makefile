# This is the PyHPy Project Makefile.

########  BASIC SETTINGS  (Adjust these.)  ########

# If you are creating a blog, located at http://example.com/blog/... , then URL_ROOT would be "/blog" or "http://example.com/blog".
# The default assumes that your site is located at http://example.com/...
export URL_ROOT=



########  ADVANCED STUFF  (You usually don't need to change these.)  ########

# Find the location of this Makefile (this method works with 'make -C', but maybe not with 'make -f'.):
THIS_MAKEFILE=$(CURDIR)/$(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
MAKEFILE_DIR=$(patsubst %/,%,$(dir $(THIS_MAKEFILE)))

# We use the Makefile location to guess our project root and PyHPy location:
PROJ_ROOT=${MAKEFILE_DIR}
PYHPY_DIR=${MAKEFILE_DIR}

# Directory locations:
SCRIPTS_DIR=${PROJ_ROOT}/1-scripts
IN_NAME=2-input
IN_DIR=${PROJ_ROOT}/${IN_NAME}
BUILD_NAME=3-build
BUILD_DIR=${PROJ_ROOT}/${BUILD_NAME}
OUT_DIR_NAME=4-output
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

# Build the development site:
# We use 'find' instead of 'rm -rf' to preserve existing directory structure.
# This is less confusing for users who rebuild a project while viewing
# outputs -- they don't end up in a detached filesystem node.
dev: clean
	@echo Copying ${IN_NAME} '-->' ${BUILD_NAME}
	@rsync -aHAX "${IN_DIR}/" "${BUILD_DIR}"
	@echo Building ${BUILD_NAME} '-->' ${OUT_DEV_NAME}
	@"${PYHPY_DIR}/bin/build" "${SCRIPTS_DIR}" "${BUILD_DIR}" "${OUT_DEV_DIR}"
	@echo
	@echo "DEV Built Successfully!  Output is at: ${OUT_DEV_DIR}"
	@echo

# Copy 'dev' to 'prod':
prod: dev
	rsync -aHAX "${OUT_DEV_DIR}/" "${OUT_PROD_DIR}"
	ln -sfn "${OUT_PROD_DIR_NAME}" "${OUT_PROD_SYMLINK}"
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


