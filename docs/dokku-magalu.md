# Tutorial: Deploy rápido e simples com Dokku e Magalu Cloud  
  
Este tutorial descreve, passo a passo,  como realizar o deploy de um projeto **Python/Django** em uma máquina virtual da **Magalu Cloud** utilizando o **Dokku**.  
  
## Pré-requisitos  
  
- Conta ativa na **Magalu Cloud** com acesso ao painel de criação de máquinas virtuais.  
- Máquina virtual criada (exemplo: BV2-2-10 com **Ubuntu 24.04 LTS**, 2vCPU, 2GB RAM e 10GB disco local).  
- Acesso ao terminal com **SSH** configurado.  
- **Git** instalado na máquina de desenvolvimento.  
- Projeto de exemplo em Python/Django disponível: [python-django-example](https://github.com/juniorcarvalho/python-django-example).   
  
  
[Dokku](http://Dokku.viewdocs.io/Dokku/) é a menor implementação PaaS que você já viu. De uma forma simples e rápida consegue-se configurar um servidor para deploy. Se existe alguma dúvida sobre PaaS, SaaS, etc., uma pesquisa rápida no google vai retornar várias referências.  
  
Nesse exemplo vamos utilizar uma máquina virtual na [Magalu Cloud](http://magalu.cloud). Uma máquina BV2-2-10, 2vCpu, 2GB de ram e 10GB de tamanho de disco local com Ubuntu 24.04 LTS.  
  
A documentação completa de uso na [Magalu Cloud](http://magalu.cloud) pode ser visualizada aqui: [Documentação Magalu Cloud](https://docs.magalu.cloud/docs/docs/). E aqui um vídeo que mostra como criar uma máquina virtual. [Como criar uma máquina virtual](https://docs.magalu.cloud/docs/computing/virtual-machine/tutorials/create-virtual-machine)  
  
Nesse exemplo vou utilizar um projeto simples em python, django e django-rest-framework. Esse projeto provê apenas um endpoint ‘status’ retornando uma resposta json.  
  
Projeto disponível aqui: [python-django-example](https://github.com/juniorcarvalho/python-Django-example)  
  
## 1. Instalando o Dokku  
  
Após criar a máquina virtual na [Magalu Cloud](http://magalu.cloud) vamos realizar o acesso via ssh pelo terminal. Vou utilizar ssh padrão de terminal, mas é possível utilizar outros clientes ssh como o [putty](https://putty.org/index.html).  
  
```bash    
ssh ubuntu@201.23.72.173
```  
  
No primeiro acesso confirme o questionamento sobre a autenticidade digitando ‘yes’.  
  
```bash  
ED25519 key fingerprint is SHA256:tbnvJ/WRO/vbi95X7D+M0mHAZq3pIo1wI39VprSnx5Y.This key is not known by any other names.Are you sure you want to continue connecting (yes/no/[fingerprint])?
```  
  
Conforme a documentação do [Dokku,](https://Dokku.com/) para realizar a instalação:  
  
```bash  
wget -NP . https://dokku.com/bootstrap.sh  
sudo DOKKU_TAG=v0.36.7 bash bootstrap.sh  
```  
  
## 2. Configurando a chave SSH  
  
Precisamos configurar no Dokku a chave pública para que seja possível executar o deploy.  
  
Na nossa máquina de desenvolvimento, vamos checar se nosso usuário tem uma chave pública:  
  
```bash  
ls -al ~/.ssh
```    
Caso não tenha nenhum arquivo .pub , pode gerar com o comando:  
  
```bash  
ssh-keygen -t rsa
```    
No meu caso eu tenho um `id_rsa.pub`. Vou ler o conteúdo, selecioná-lo e copiar:  
  
```bash  
  
cat ~/.ssh/id_rsa.pub  
```  
  
Com o conteúdo do arquivo copiado, vamos executar o comando na maquina remota:  
 
```bash  
echo 'CONTENTS_OF_ID_RSA_PUB_FILE' | sudo dokku ssh-keys:add admin
```    
CONTENTS_OF_ID_RSA_PUB_FILE = a chave copiada da maquina de desenvolvimento.
  
Confirme se a chave foi criada com o comando:  
  
```bash  
dokku ssh-keys:list
```    
## 3. Criando a App  
  
No terminal, conectado na nossa máquina virtual:  
  
```bash  
dokku apps:create python-django-example  
```    
Para listar os apps existentes:  
  
```bash  
dokku apps
```    
Quando criamos um novo aplicativo, por padrão o Dokku não fornece nenhum banco de dados como MySQL ou PostgreSQL. É preciso instalar plugins. Existem [plugins](https://Dokku.com/docs/community/plugins/) oficiais para banco de dados. Nesse exemplo vou utilizar o PostgreSQL.  
  
**Instalando o plugin postgres e configurando o serviço de banco de dados**  
  
```bash  
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
```  
  
Criando o serviço postgres:  
  
```bash  
dokku postgres:create database  
```  
Vamos criar o link entre os serviços de banco de dados e nossa app.  
  
```bash  
dokku postgres:link database python-django-example  
```  


Após esse comando vai ser criado automaticamente a variável DATABASE_URL em nosso app.  
  
## 4. Configurando variáveis de ambiente  
  
Temos que configurar algumas variáveis de ambiente em nosso app. Como estamos usando Django, vamos criar  `SECRET_KEY` e `DEBUG`. Acesse a documentação [environment-variables](https://Dokku.com/docs/configuration/environment-variables/) para mais informações.  
  
```bash  
dokku config:set python-django-example `DEBUG`='False'  
dokku config:set python-django-example `SECRET_KEY`='sua secret_key'  
dokku config:set python-django-example ALLOWED_HOSTS='127.0.0.1, .localhost,201.23.72.173'
```  
  
Observação: Precisamos adicionar o IP do servidor em ALLOWED_HOSTS, no caso do exemplo o IP é o 201.23.72.173.  
  
Para listar as variáveis de ambiente de nossa app:  
  
```bash  
dokku config python-django-example
```  
  
## 5. Executando o primeiro deploy  
  
Na nossa máquina de desenvolvimento vamos configurar o git para fazer o primeiro deploy. Vamos adicionar nosso repositorio remoto Dokku da seguinte forma:  
Comando: `git remote add dokku dokku@[IP-do-servidor]:[nome-app]`  
```bash  
git remote add dokku dokku@201.23.72.173:python-django-example
```  
  
Executando o deploy:  
  
```bash  
git push Dokku main  
```  
  
## 6. Criando as tabelas do banco de dados  
  
Nossa app está no ar mais ainda não tem as tabelas de nossa base de dados. Na máquina virtual execute:  
  
```bash  
dokku run python-django-example python manage.py migrate
```  
  
## 7. Configurando o domínio  
  
Precisamos configurar o domínio para conseguir acessar o servidor. No nosso exemplo não temos URL então vamos configurar o acesso pelo IP mesmo.  

Onde 201.23.72.173 é o ip do servidor.  
```bash  
dokku domains:add python-django-example 201.23.72.173
dokku ps:restart python-django-example 
```  
  
Caso tenha uma URL exemplo: django-example.com.br:  
  
```bash  
dokku domains:add python-django-example django-example.com.br
dokku config:set python-django-example ALLOWED_HOSTS="django-example.com.br,127.0.0.1, .localhost"
dokku ps:restart python-django-example 
```  

## 8. dokku-letsencrypt
dokku-letsencrypt é o plugin oficial do dokku que permite recuperar e instalar automaticamente certificados TLS de letsencrypt.org

Instalando o plugin:  
```bash
sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
```
Configurando:
```bash
# configura o email para registro do certificado
dokku letsencrypt:set --global email your@email.tld
# ativa o letsencrypt para a app
dokku letsencrypt:enable python-django-example
# renovação automatica do certificado
dokku letsencrypt:cron-job --add
```
## 9. Acessando a aplicação  
  
**Admin Django**: [http://201.23.72.173/admin](http://201.23.72.173/admin)  
  
**API**: [http://201.23.72.173/api/status/](http://201.23.72.173/api/status/)  
  
## 10. Considerações finais  
  
Já utilizo o Dokku em projetos pessoais e testes. Sempre funcionou muito bem para pequenas aplicações. Vale a pena estudar mais pois as possibilidades de integrações são grandes.   
  
Qualquer dúvida ou sugestão me envie um email: joseadolfojr@gmail.com
