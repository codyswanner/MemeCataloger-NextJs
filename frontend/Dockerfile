# See build steps below
FROM codyswanner/memecataloger-nextjs:frontend-25.10.1

# Run server and ensure container stays open
CMD ["bash", "-c", "npm ci; npm run dev; tail -f /dev/null"]


###############################################################################
# Image layers/build process can be found in frontend/Dockerfile-baseline
###############################################################################
