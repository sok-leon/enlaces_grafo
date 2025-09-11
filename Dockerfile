FROM python:3.11-slim

# Instala dependencias
RUN pip install --no-cache-dir ping3 fastapi uvicorn

# Copia los archivos
WORKDIR /app
COPY . .


# Ejecuta el script
CMD ["uvicorn", "main:app","--host", "0.0.0.0","--port" ,"80" "--reload"]
