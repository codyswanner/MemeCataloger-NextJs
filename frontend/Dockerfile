# See build steps below
FROM codyswanner/memecataloger-nextjs:frontend-25.08.1

# USER front-runner
CMD ["bash", "-c", "npm run dev; tail -f /dev/null"]


###############################################################################
# The following were the steps used to create the image
# that is pulled from codyswanner/memecataloger-nextjs
###############################################################################

# FROM node:lts-slim
#
# RUN apt-get update \
# 	&& apt-get upgrade -y \
# 	&& apt-get install -y sudo gcc pkg-config
#
# # Create a non-privileged user to run processes
# ARG UID=1001
# RUN useradd -m --uid "${UID}" front-runner
# RUN usermod -aG sudo front-runner
#
# # Create a sudoers configuration file in /etc/sudoers.d/
# RUN echo 'front-runner localhost=(root) NOPASSWD: /usr/local/bin/npm' > /etc/sudoers.d/front-runner \
# 	&& chmod 440 /etc/sudoers.d/front-runner \
# 	&& chown root:root /etc/sudoers.d/front-runner
#
# COPY . /home/front-runner/
#
# WORKDIR /home/front-runner/memecataloger
#
# RUN npm install
# RUN npx playwright install --with-deps chromium
# RUN npx playwright install --with-deps firefox
#
# # USER front-runner
# CMD ["bash", "-c", "npm run dev; tail -f /dev/null"]
