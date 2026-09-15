# Моя история команд или как я поднимал YTsaurus

> Это copy paste debug часть отчёта, скорее мой личный журнал - что делал, зачем, и почему не вышло за полчаса по инструкции. 

--- 
## Docker  

Стандартная процедура с официального сайта. Ключ, репозиторий, установка.

```bash
# Ключ Docker
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Репозиторий (heredoc, вводить ЦЕЛИКОМ, не забыть EOF в конце)
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER

# Проверка
sudo docker run hello-world
```

##  kubectl, kind, helm
Три утилиты, каждая для своего.

```bash
# kubectl — рулим k8s-кластером
curl -LO https://dl.k8s.io/release/`curl -LS https://dl.k8s.io/release/stable.txt`/bin/linux/amd64/kubectl

# kind — локальный k8s в Docker-контейнере
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.33.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# helm — пакетный менеджер для k8s
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4
chmod 700 get_helm.sh
./get_helm.sh
```

Поднимаем кластер
```bash
kind create cluster --name ytsaurus
kubectl cluster-info --context kind-ytsaurus
kubectl cluster-info
```
cert-manager
Нужен для работы с TLS-сертификатами внутри кластера.

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.17.1/cert-manager.yaml

# Ждём, пока webhook поднимется
kubectl get pods -A
YTsaurus оператор
```bash
helm install ytsaurus oci://ghcr.io/ytsaurus/ytop-chart --version 0.31.0
```
Вторая попытка установки упадёт с cannot reuse a name that is still in use —
это нормально, значит первый раз всё уже прошло. Смотри helm list.

Проверка:

```bash
helm status ytsaurus
```
Сам кластер YTsaurus
```bash
curl -s https://raw.githubusercontent.com/ytsaurus/ytsaurus/refs/heads/main/yt/docs/code-examples/cluster-config/cluster_v1_local.yaml > cluster_v1_local.yaml
kubectl apply -f cluster_v1_local.yaml
``` 

Сетевой доступ
Kind создаёт внутреннюю сеть. Чтобы дотянуться снаружи — port-forward.

Так как у меня облачная VM, а не локальная машина, пришлось использовать --address 0.0.0.0
и отдельно открывать порты в security group облака.

```bash
nohup kubectl port-forward --address 0.0.0.0 service/ytsaurus-ui 8080:80 > /tmp/pf-ui.log 2>&1 &
nohup kubectl port-forward --address 0.0.0.0 service/http-proxies-lb 8081:80 > /tmp/pf-http.log 2>&1 &
nohup kubectl port-forward --address 0.0.0.0 pod/rp-0 8082:9013 > /tmp/pf-rpc.log 2>&1 &
```
Про & в конце — однажды забыл, и терминал просто завис.
 & = запусти в фоне

RPC-прокси в моей сборке чарта назывался не rpc-proxies-lb, а просто под rp-0.
Пришлось пробрасывать к поду напрямую. Проверить реальные порты можно через:

```bash
kubectl get pod rp-0 -o jsonpath='{.spec.containers[0].ports}'
```
[`Скриншот: Kubectl_pod_check.png`](./images_text_src/Kubectl_pod_check.png)  

Установка ytsaurus-client (CLI)
```bash
pip3 install --user ytsaurus-client
```
Но Ubuntu 24.04 ругается на externally-managed-environment (PEP 668), поэтому:

```bash
pip3 install --user --break-system-packages ytsaurus-client
pip3 install --user --break-system-packages ytsaurus-yson       # для схем
pip3 install --user --break-system-packages ytsaurus-rpc-driver # для RPC
```
Можно было через venv, но я панк.

PATH:

```bash
export PATH="$PATH:$HOME/.local/bin"
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc
yt --version
```
Переменные окружения
Чтобы каждый раз не писать --proxy, сохранил в ~/.bashrc:

```bash
export YT_PROXY='http://localhost:8081'
export YT_CONFIG_PATCHES='{proxy={enable_proxy_discovery=%false}}'
export YT_TOKEN=password

# Навсегда:
echo 'export YT_PROXY=http://localhost:8081' >> ~/.bashrc
echo 'export YT_CONFIG_PATCHES="{proxy={enable_proxy_discovery=%false}}"' >> ~/.bashrc
echo 'export YT_TOKEN=password' >> ~/.bashrc
source ~/.bashrc

# Проверка
yt whoami   # должно вернуть admin
```
Скриншоты тут [`Моя виртуальная машина в клауде`](./images_text_src/Виртуальная_машина_в_клауде.png) 
  и [`YTsaurus по адресу моей виртуальной машины`](./images_text_src/Открыл свой YTsaurus.png)
 

Создание директории  
```bash
yt create map_node //home/ilyakubashin/ratings_project --recursive 
--recursive создаёт всю цепочку //home → //home/ilyakubashin → //home/ilyakubashin/ratings_project.
```  
