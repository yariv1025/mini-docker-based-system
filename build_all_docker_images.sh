docker build -f analyze_module/Dockerfile . -t analyze_module
docker build -f password_module/Dockerfile . -t password_module
docker build -f controller_module/Dockerfile . -t controller_module
