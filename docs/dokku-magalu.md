---


---

<h1 id="tutorial-deploy-rápido-e-simples-com-dokku-e-magalu-cloud">Tutorial: Deploy rápido e simples com Dokku e Magalu Cloud</h1>
<p>Este tutorial descreve, passo a passo,  como realizar o deploy de um projeto <strong>Python/Django</strong> em uma máquina virtual da <strong>Magalu Cloud</strong> utilizando o <strong>Dokku</strong>.</p>
<h2 id="pré-requisitos">Pré-requisitos</h2>
<ul>
<li>Conta ativa na <strong>Magalu Cloud</strong> com acesso ao painel de criação de máquinas virtuais.</li>
<li>Máquina virtual criada (exemplo: BV2-2-10 com <strong>Ubuntu 24.04 LTS</strong>, 2vCPU, 2GB RAM e 10GB disco local).</li>
<li>Acesso ao terminal com <strong>SSH</strong> configurado.</li>
<li><strong>Git</strong> instalado na máquina de desenvolvimento.</li>
<li>Projeto de exemplo em Python/Django disponível: <a href="https://github.com/juniorcarvalho/python-django-example">python-django-example</a>.</li>
</ul>
<p><a href="http://Dokku.viewdocs.io/Dokku/">Dokku</a> é a menor implementação PaaS que você já viu. De uma forma simples e rápida consegue-se configurar um servidor para deploy. Se existe alguma dúvida sobre PaaS, SaaS, etc., uma pesquisa rápida no google vai retornar várias referências.</p>
<p>Nesse exemplo vamos utilizar uma máquina virtual na <a href="http://magalu.cloud">Magalu Cloud</a>. Uma máquina BV2-2-10, 2vCpu, 2GB de ram e 10GB de tamanho de disco local com Ubuntu 24.04 LTS.</p>
<p>A documentação completa de uso na <a href="http://magalu.cloud">Magalu Cloud</a> pode ser visualizada aqui: <a href="https://docs.magalu.cloud/docs/docs/">Documentação Magalu Cloud</a>. E aqui um vídeo que mostra como criar uma máquina virtual. <a href="https://docs.magalu.cloud/docs/computing/virtual-machine/tutorials/create-virtual-machine">Como criar uma máquina virtual</a></p>
<p>Nesse exemplo vou utilizar um projeto simples em python, Django e Django-rest-framework. Esse projeto provê apenas um endpoint ‘status’ retornando uma resposta json.</p>
<p>Projeto disponível aqui: <a href="https://github.com/juniorcarvalho/python-Django-example">python-django-example</a></p>
<h2 id="instalando-o-dokku">1. Instalando o Dokku</h2>
<p>Após criar a máquina virtual na <a href="http://magalu.cloud">Magalu Cloud</a> vamos realizar o acesso via ssh pelo terminal. Vou utilizar ssh padrão de terminal, mas é possível utilizar outros clientes ssh como o <a href="https://putty.org/index.html">putty</a>.</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">ssh</span> ubuntu@201.23.72.173
</code></pre>
<p>No primeiro acesso confirme o questionamento sobre a autenticidade digitando ‘yes’.</p>
<pre class=" language-bash"><code class="prism  language-bash">ED25519 key fingerprint is SHA256:tbnvJ/WRO/vbi95X7D+M0mHAZq3pIo1wI39VprSnx5Y.This key is not known by any other names.Are you sure you want to <span class="token keyword">continue</span> connecting <span class="token punctuation">(</span>yes/no/<span class="token punctuation">[</span>fingerprint<span class="token punctuation">]</span><span class="token punctuation">)</span>?
</code></pre>
<p>Conforme a documentação do <a href="https://Dokku.com/">Dokku,</a> para realizar a instalação:</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">wget</span> -NP <span class="token keyword">.</span> <span class="token punctuation">[</span>https://dokku.com/bootstrap.sh<span class="token punctuation">]</span><span class="token punctuation">(</span>https://dokku.com/bootstrap.sh<span class="token punctuation">)</span>  
<span class="token function">sudo</span> DOKKU_TAG<span class="token operator">=</span>v0.36.7 <span class="token function">bash</span> <span class="token punctuation">[</span>bootstrap.sh<span class="token punctuation">]</span><span class="token punctuation">(</span>http://bootstrap.sh/<span class="token punctuation">)</span>  
</code></pre>
<h2 id="configurando-a-chave-ssh">2. Configurando a chave SSH</h2>
<p>Precisamos configurar no Dokku a chave pública para que seja possível executar o deploy.</p>
<p>Na nossa máquina de desenvolvimento, vamos checar se nosso usuário tem uma chave pública:</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">ls</span> -al ~/.ssh
</code></pre>
<p>Caso não tenha nenhum arquivo .pub , pode gerar com o comando:</p>
<pre class=" language-bash"><code class="prism  language-bash">ssh-keygen -t rsa
</code></pre>
<p>No meu caso eu tenho um <code>id_rsa.pub</code>. Vou ler o conteúdo, selecioná-lo e copiar:</p>
<pre class=" language-bash"><code class="prism  language-bash">  
<span class="token function">cat</span> ~/.ssh/id_rsa.pub  
</code></pre>
<p>Com o conteúdo do arquivo copiado, vamos executar o comando na maquina remota:</p>
<p>Esse comando deve ser executado como root, então antes execute:</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">sudo</span> <span class="token function">su</span>
</code></pre>
<p>e depois:</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token keyword">echo</span> <span class="token string">'CONTENTS_OF_ID_RSA_PUB_FILE'</span> <span class="token operator">|</span> Dokku ssh-keys:add admin
</code></pre>
<p>CONTENTS_OF_ID_RSA_PUB_FILE = a chave copiada da maquina de desenvolvimento.</p>
<p>para sair do root: <code>exit</code></p>
<p>Confirme se a chave foi criada com o comando:</p>
<pre class=" language-bash"><code class="prism  language-bash">dokku ssh-keys:list
</code></pre>
<h2 id="criando-a-app">3. Criando a App</h2>
<p>No terminal, conectado na nossa máquina virtual:</p>
<pre class=" language-bash"><code class="prism  language-bash">dokku apps:create python-django-example  
</code></pre>
<p>Para listar os apps existentes:</p>
<pre class=" language-bash"><code class="prism  language-bash">dokku apps
</code></pre>
<p>Quando criamos um novo aplicativo, por padrão o Dokku não fornece nenhum banco de dados como MySQL ou PostgreSQL. É preciso instalar plugins. Existem <a href="https://Dokku.com/docs/community/plugins/">plugins</a> oficiais para banco de dados. Nesse exemplo vou utilizar o PostgreSQL.</p>
<p><strong>Instalando o plugin postgres e configurando o serviço de banco de dados</strong></p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">sudo</span> dokku plugin:install https://github.com/dokku/dokku-postgres.git
</code></pre>
<p>Criando o serviço postgres:</p>
<pre class=" language-bash"><code class="prism  language-bash">dokku postgres:create database  
</code></pre>
<p>Vamos criar o link entre os serviços de banco de dados e nossa app.</p>
<pre class=" language-bash"><code class="prism  language-bash">dokku postgres:link database python-django-example  
</code></pre>
<p>Após esse comando vai ser criado automaticamente a variável DATABASE_URL em nosso app.</p>
<h2 id="configurando-variáveis-de-ambiente">4. Configurando variáveis de ambiente</h2>
<p>Temos que configurar algumas variáveis de ambiente em nosso app. Como estamos usando Django, vamos criar  <code>SECRET_KEY</code> e <code>DEBUG</code>. Acesse a documentação <a href="https://Dokku.com/docs/configuration/environment-variables/">environment-variables</a> para mais informações.</p>
<pre class=" language-bash"><code class="prism  language-bash">dokku config:set python-django-example <span class="token variable"><span class="token variable">`</span>DEBUG<span class="token variable">`</span></span><span class="token operator">=</span><span class="token string">'False'</span>  
dokku config:set python-django-example <span class="token variable"><span class="token variable">`</span>SECRET_KEY<span class="token variable">`</span></span><span class="token operator">=</span><span class="token string">'sua secret_key'</span>  
dokku config:set python-django-example ALLOWED_HOSTS<span class="token operator">=</span><span class="token string">'127.0.0.1, .localhost,201.23.72.173'</span>
</code></pre>
<p>Observação: Precisamos adicionar o IP do servidor em ALLOWED_HOSTS, no caso do exemplo o IP é o 201.23.72.173.</p>
<p>Para listar as variáveis de ambiente de nossa app:</p>
<pre class=" language-bash"><code class="prism  language-bash">dokku config python-django-example
</code></pre>
<h2 id="executando-o-primeiro-deploy">5. Executando o primeiro deploy</h2>
<p>Na nossa máquina de desenvolvimento vamos configurar o git para fazer o primeiro deploy. Vamos adicionar nosso repositorio remoto Dokku da seguinte forma:<br>
Comando: <code>git remote add dokku dokku@[IP-do-servidor]:[nome-app]</code></p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">git</span> remote add dokku dokku@201.23.72.173:python-django-example
</code></pre>
<p>Executando o deploy:</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">git</span> push Dokku main  
</code></pre>
<h2 id="criando-as-tabelas-do-banco-de-dados">6. Criando as tabelas do banco de dados</h2>
<p>Nossa app está no ar mais ainda não tem as tabelas de nossa base de dados. Na máquina virtual execute:</p>
<pre class=" language-bash"><code class="prism  language-bash">dokku run python-django-example python manage.py migrate
</code></pre>
<h2 id="configurando-o-domínio">7. Configurando o domínio</h2>
<p>Precisamos configurar o domínio para conseguir acessar o servidor. No nosso exemplo não temos URL então vamos configurar o acesso pelo IP mesmo.</p>
<pre class=" language-bash"><code class="prism  language-bash">dokku domains:add python-django-example 201.23.72.173
dokku ps:restart python-django-example 
</code></pre>
<p>Caso tenha uma URL exemplo: <a href="http://django-example.com.br">django-example.com.br</a>:</p>
<pre class=" language-bash"><code class="prism  language-bash">dokku domains:add python-django-example django-example.com.br
dokku config:set python-django-example ALLOWED_HOSTS<span class="token operator">=</span><span class="token string">"django-example.com.br,127.0.0.1, .localhost"</span>
dokku ps:restart python-django-example 
</code></pre>
<h2 id="acessando-a-aplicação">8. Acessando a aplicação</h2>
<p><strong>Admin Django</strong>: <a href="http://201.23.72.173/admin">http://201.23.72.173/admin</a></p>
<p><strong>API</strong>: <a href="http://201.23.72.173/api/status/">http://201.23.72.173/api/status/</a></p>
<h2 id="considerações-finais">9. Considerações finais</h2>
<p>Já utilizo o Dokku em projetos pessoais e testes. Sempre funcionou muito bem para pequenas aplicações. Vale a pena estudar mais pois as possibilidades de integrações são grandes.</p>
<p>Qualquer dúvida ou sugestão me envie um email: <a href="mailto:joseadolfojr@gmail.com">joseadolfojr@gmail.com</a></p>

