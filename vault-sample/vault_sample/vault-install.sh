poetry install

sudo apt update && sudo apt install -y gpg
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt update && sudo apt install -y vault

sudo apt update && sudo apt install -y postgresql postgresql-contrib
sudo pg_ctlcluster $(pg_lsclusters | awk 'NR==2 {print $1}') main start
sudo -u postgres createuser --interactive --pwprompt
sudo -u postgres createdb postgres
