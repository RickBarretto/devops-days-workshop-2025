# DOD FSA - Containers

Stack com três serviços: `nginx` servindo `./html`, `localstack` (mock de AWS) e um container dedicado com o `aws-cli`.

## Uso rápido
- Certifique-se de ter Docker + Docker Compose instalados.
- Suba os serviços: `docker compose up -d`
- Acompanhe logs (opcional): `docker compose logs -f`

## Serviços
- `nginx` exposto em `http://localhost:8080`, servindo `html/index.html` (e `style.css`).
- `localstack` exposto em `http://localhost:4566`, com serviços `s3`, `sqs` e `lambda` habilitados.
- `aws-cli` permanece rodando (`sleep infinity`) para execução de comandos dentro do container.

## Fluxo local (Nginx + LocalStack)
1. Suba os containers: `docker compose up -d`
2. Confira o site local em `http://localhost:8080`.
3. (LocalStack) Crie bucket S3, configure website e envie os arquivos:
   ```bash
   docker compose exec aws-cli aws s3api create-bucket --bucket dod-fsa-site --endpoint-url http://localstack:4566
   docker compose exec aws-cli aws s3api put-bucket-website --bucket dod-fsa-site --website-configuration '{"IndexDocument":{"Suffix":"index.html"}}' --endpoint-url http://localstack:4566
   docker compose exec aws-cli aws s3 sync /usr/share/nginx/html s3://dod-fsa-site --endpoint-url http://localstack:4566
   ```
4. Teste via LocalStack: `curl http://localhost:4566/dod-fsa-site/index.html`

## Publicar na AWS
- S3 (site estático): após configurar `aws configure` com credenciais válidas, rode:
  ```bash
  aws s3api create-bucket --bucket <nome-unico>
  aws s3api put-bucket-website --bucket <nome-unico> --website-configuration '{"IndexDocument":{"Suffix":"index.html"}}'
  aws s3 sync html/ s3://<nome-unico>
  ```
  O endpoint do site ficará em `http://<nome-unico>.s3-website-<regiao>.amazonaws.com`.
- EC2 com Nginx: copie o conteúdo para a instância e sirva com Nginx:
  ```bash
  scp -r html/ ec2-user@<ip-ec2>:/home/ec2-user/site
  ssh ec2-user@<ip-ec2> "docker run -d -p 80:80 -v /home/ec2-user/site:/usr/share/nginx/html:ro nginx:1.25-alpine"
  ```

## Utilidades
- Listar buckets no LocalStack: `docker compose exec aws-cli aws s3api list-buckets --endpoint-url http://localstack:4566`
- Derrubar os serviços: `docker compose down`