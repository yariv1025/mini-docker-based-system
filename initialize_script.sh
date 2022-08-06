docker network create --driver bridge analyze_module_network
docker network create --driver bridge password_module_network


docker build -f analyze_module/Dockerfile . -t analyze_module
docker build -f password_module/Dockerfile . -t password_module
docker build -f controller_module/Dockerfile . -t controller_module
