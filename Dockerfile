# Usando uma imagem oficial do PostgreSQL
FROM postgres:13

# Configurar variáveis de ambiente do PostgreSQL
ENV POSTGRES_DB=PatientSystem
ENV POSTGRES_USER=postgre
ENV POSTGRES_PASSWORD=853211

# Copiar o script SQL para o container
COPY init_db.sql /docker-entrypoint-initdb.d/

