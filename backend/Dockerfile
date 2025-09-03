# See build steps below
FROM codyswanner/memecataloger-nextjs:backend-25.09.1

# Make migrations to the database
RUN python manage.py makemigrations

# Run the application
CMD ["bash", "-c", "python manage.py migrate & python manage.py runserver 0.0.0.0:8000"]


###############################################################################
# Image layers/build process can be found in backend/Dockerfile-baseline
###############################################################################
