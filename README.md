# RaspbotV2_dev
Tests des fonctionnalités Yahboom Raspbot V2 


## Picamera2
[Repository picamera2 pour Raspberry Pi](https://github.com/raspberrypi/picamera2/tree/main)

- Contient le code source de Picamera2
- Un tas d'exemples
- Des tests

# Backup vers laptop
scp -rp pi@192.168.1.50:/home/pi/raspbotV2_dev C:\Users\guigu\OneDrive\Dev\GitRepositories

# Environnement WSL

Mettre à jour python au même niveau que RaspbotV2 

Mettre en place Python 3.11.2 sur Linux sans casser le Python système, avec une méthode recommandée (pyenv) puis lier ça à votre projet/VS Code.

Méthode recommandée (pyenv) — propre et réversible
Avantages:
- Installe exactement 3.11.2  
- N’altère pas le Python système (apt)  
- Facile à activer par projet  

0- Dans WSL, se placer dans le répertoire ./root

1- Installer les dépendances de compilation (Debian/Ubuntu/Raspberry Pi OS)
```
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev curl llvm libncursesw5-dev xz-utils tk-dev \
  libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev libgdbm-dev libnss3-dev libedit-dev
```
2- Installer pyenv
```
# via git (recommandé)
git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# activer pyenv dans votre shell
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# recharger le shell
exec "$SHELL"
```

3- Installer Python 3.11.2
```
pyenv install 3.11.2
```
4- Fixer la version localement au dépôt (recommandé)
Dans votre dossier de projet (ex: raspbotV2_dev):

```
cd /root/raspbotV2_dev
pyenv local 3.11.2
```
Cela crée un fichier .python-version et active 3.11.2 dès que vous êtes dans ce dossier.