#!/bin/sh

# O Railway define a variável de ambiente PORT.
# Se ela não estiver definida, usamos 8080 como padrão.
# O Hypercorn irá ouvir em todas as interfaces (0.0.0.0).
hypercorn main:app --bind "0.0.0.0:${PORT:-8080}"