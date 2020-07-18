set -eu

COMMAND=${1}

if [ ${COMMAND} = "build" ]; then
docker container run -w /work -v $(pwd):/work --rm -it python:3.8.2-buster sh -c ' \
    pip install mkdocs && \
    pip install -r docs/requirements.txt && \
    cd docs && \
    mkdocs build && \
    cd .. \
'
elif [ ${COMMAND} = "publish" ]; then
    # Set git user name and email as a format of "Your Name <email@example.com>"
    GIT_USER=${GIT_USER}
    # gh-pages first clone the repository and then create gh-pages branch there.
    # The cloned repository is saved in CACHE_DIR .
    # Read https://www.npmjs.com/package/gh-pages#tips more details
    CACHE_DIR=gh-pages

    docker container run -w /work -v $(pwd):/work --rm -it -e CACHE_DIR=${CACHE_DIR} node:8.10.0 sh -c " \
        npm install -g --silent gh-pages@2.0.1 && \
        gh-pages --user \"${GIT_USER}\" --dist docs/site
    "
else
    echo "COMMAND should be one of {build,publish}."
fi