
FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  && apt-get -y install -qq --force-yes cron \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
  && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
  && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

# Copy cron file to the cron.d directory
COPY crontab/send_subscriber_email /etc/cron.d/send_subscriber_email
RUN sed -i 's/\r$//g' /etc/cron.d/send_subscriber_email

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/send_subscriber_email

# Apply cron job
RUN crontab /etc/cron.d/send_subscriber_email

COPY --chown=django:django . /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
