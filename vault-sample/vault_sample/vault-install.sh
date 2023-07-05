poetry install

sudo apt update && sudo apt install -y gpg

# GPG is required for the package signing key
sudo apt install gpg

# Download the signing key to a new keyring
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Verify the key's fingerprint
gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint

# The fingerprint must match 798A EC65 4E5C 1542 8C8E 42EE AA16 FCBC A621 E701, which can also be verified at https://www.hashicorp.com/security under "Linux Package Checksum Verification".

# Add the HashiCorp repo
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

# apt update successfully
sudo apt update

curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt update && sudo apt install -y vault

sudo apt update && sudo apt install -y postgresql postgresql-contrib
sudo pg_ctlcluster $(pg_lsclusters | awk 'NR==2 {print $1}') main start
sudo -u postgres createuser --interactive --pwprompt
sudo -u postgres createdb postgres
