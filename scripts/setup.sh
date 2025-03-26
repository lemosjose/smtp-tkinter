#!/bin/bash

# Script para instalar pacotes no Debian 11

echo "Iniciando o script de instalação..."

# Garante que o script seja executado como root
if [ "$(id -u)" -ne 0 ]; then
   echo "Este script deve ser executado como root" 1>&2
   exit 1
fi

# Função para aguardar o desbloqueio do apt
wait_for_apt() {
    while fuser /var/lib/dpkg/lock >/dev/null 2>&1 || \
          fuser /var/lib/apt/lists/lock >/dev/null 2>&1 || \
          fuser /var/cache/apt/archives/lock >/dev/null 2>&1; do
        echo "Aguardando desbloqueio do apt..."
        sleep 1
    done
}

# Atualiza a lista de pacotes
echo "Atualizando a lista de pacotes..."
wait_for_apt
apt update

# Instala o Nano
echo "Instalando o Nano..."
wait_for_apt
apt install -y nano

# Atualiza a lista de pacotes novamente
echo "Atualizando a lista de pacotes novamente..."
wait_for_apt
apt-get update

# Instala o software-properties-common
echo "Instalando software-properties-common..."
wait_for_apt
apt-get install -y software-properties-common

# Adiciona o repositório Universe (correção)
echo "Adicionando o repositório Universe..."
wait_for_apt
add-apt-repository "deb http://deb.debian.org/debian bullseye main contrib non-free"

# Instala o Certbot e o plugin Python diretamente dos repositórios
echo "Instalando Certbot e o plugin Python..."
wait_for_apt
apt install -y certbot python3-certbot

echo "Instalação concluída com sucesso!"

# Configurar Postfix automaticamente
echo "Configurando Postfix..."
debconf-set-selections <<< "postfix postfix/mailname string $DOMAIN"
debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
dpkg-reconfigure -f noninteractive postfix
