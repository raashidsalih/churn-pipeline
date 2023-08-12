for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done

sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

cd /home/admin

git clone https://github.com/raashidsalih/churn-pipeline

sudo chmod -R u=rwx,g=rwx,o=rwx churn-pipeline/

cd churn-pipeline/

mv sample.env .env

sudo mkdir -p pg_data pgadmin_data metabase && sudo chmod -R u=rwx,g=rwx,o=rwx pg_data pgadmin_data metabase

sudo docker compose up airflow-init

sudo docker compose up