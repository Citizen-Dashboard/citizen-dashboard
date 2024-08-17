# Use the official PostgreSQL image
FROM postgres:16

# Environment variables for PostgreSQL
ENV POSTGRES_DB=agenda_items
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD_FILE=/run/secrets/citizen_dashboard_sql_password

# Run the database
CMD ["postgres"]