<p align="center">
 <img width="100px" src="https://th.bing.com/th/id/R.02dc5a07fba13bf8fafcd5a9ef4650f2?rik=eUGmhqSWUgGq3Q&riu=http%3a%2f%2fdesignlooter.com%2fimages%2fwater-drop-svg-2.png&ehk=wRcSGTKTSlUGC4f05vU4XiJGsENTi9gq1%2fDJzsp%2fIIQ%3d&risl=&pid=ImgRaw&r=0" align="center" alt="GitHub Readme Stats" />
 <h2 align="center">Consumo Inteligente: Um estudo utilizando conceitos de IoT, com um modelo descentralizado (Fog/Edge Computing) e a abordagem Peer-to-Peer</h2>
 <p align="center">Protótipo de um sistema completo de controle inteligente gastos. Trazendo automação na coleta e controle dos dados, bem como disponibilizando para consulta para admnistrador e clientes.</p>
</p>
<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=Concluido&color=GREEN&style=for-the-badge"/>
</p>


 
# Índice

- [Pessoas desenvolvedoras](#desenvolvedoras)
- [Acesso ao projeto](#Acesso)
- [Tecnologias utilizadas](#Tecnologias)
- [Solução](#Solução)
- [Componentes](#componentes)
   - [Broker](#Broker)
   - [Hidrômetro](#Hidrômetro)
   - [Servidor](#Servidor)
   - [Nó](#Nó)
   - [Tela do usuário](#Usuário)
   - [Tela do administrador](#Administrador)
   - [API REST](#APIREST)
   - [Banco de dados](#dados)
- [Demonstração](#demonstraçao)
- [Considerações finais](#consideracoes)




  
# Desenvolvedoras
<br /><a href="https://github.com/AndrezaNobrega">Andreza Nóbrega</a>
<br /><a href="https://github.com/Evelynsuzarte">Evelyn Suzarte</a>

# Acesso
 - colocar links do dockerhub

# Tecnologias


<ul>
  <li>MQTT</li>
  <li>Fog Computing</li>
  <li>Python</li>
  <li>Flask</li>
  <li>SQLite</li>
</ul>



# Solução
  (descrever toda a solução do projeto por alto, quando formos falar sobre cada componente especificamente, iremos dar uma aprofundada)
  -MQTT
  <p2>É iniciado um número desejado de hidrômetros através do terminal, selecionando o seu setor e seu nível de vazão, em seguida devemos iniciar o servidor para recebimento dos dados e logo após conectar a névoa, onde será processados as questões da média, bloqueio, etc. </p2>
# Componentes 
 
<h2> - Broker</h2>

<p2> O broker é um servidor que recebe todas as mensagens dos clientes e, em seguida, roteia essas mensagens para os clientes de destino relevantes. Esses clientes estão conectados ao broker através de tópicos, onde os clientes conectados se inscrevem (subscriber) para receber as mensagens que o tópico gera, e esse movimento de envio de mensagens ao tópico é chamado de publish. Esse modelo de operação de envio de mensagens compõe o protocolo MQTT (Message Queuing Telemetry Transport) que é um protocolo de mensagens leve para sensores e pequenos dispositivos otimizado para redes TCP/IP.<p2>

 <h2> - Hidrômetro</h2>

<p2> O hidrômetro funciona como o sensor do sistema, além dele enviar dados (servindo como publish) ele também recebe dados (servindo como subscriber) para gerenciamento do hidrômetro. Assim, nele podemos verificar a vazão de água atual, o consumo total do período, status de vazamento e pode ser bloqueado por dois motivos: estar em débito e consumo maior que a média de consumo de todos os hidrômetros. Eles estão conectados ao nó da nuvem, que também chamamos de setores, onde lá são gerenciados.</p2>

<h2> - Servidor</h2>
 
<p2> Esse servidor serve como um servidor geral para gerenciamento da nuvem, onde ele faz q conexão com o interface dos clientes (adm e cliente) e com os nós da nuvem. Ele faz apenas o gerenciamento de envio de dados entre essas duas partes.</p2> 

<h2>- Nó </h2>
<p2> No nó da nuvem ficam conectados os hidrômetros que estão conectados a um banco de dados que cada nó tem. Assim, qualquer ação de gerenciamento como de bloqueio, desbloqueio, visualização de consumo e outros, são feitos através do nó.</p2>

<h2>- Tela do usuário</h2>
<p2> Na tela do usuário ele tem acesso a funções de visualização dos dados de um hidrômetro, consumo atual, pagar a conta e valor da conta.
As solicitações do usuário são gerenciadas pela API, que são enviadas ao servidor, que se conecta ao nó ( que também chamamos de setor).</p2>

<h2>- Tela do administrador</h2>
<p2> Na tela da administrador ele tem acesso a funções de visualização dos dados de um hidrômetro, consumo atual, pagar a conta e valor da conta.
As solicitações do usuário são gerenciadas pela API, que são enviadas ao servidor, que se conecta ao nó ( que também chamamos de setor.</p2>
Visualização dos n hidrômetros, Visualizar hidrômetro selecionado,Bloqueio por valor de teto de gastos,Visualizar hidrômetros com vazamento 

<h2>- API REST</h2>
<p2> A API faz a ligação entre a interface do administrador e do cliente, e todo o restante das conexões. <p2> 

<h2>- Banco de dados</h2>
<p2> No banco de dados é manipulado as buscas, criações e atualizações nos dados. As alterações são feitas a partir dos nós da névoa. Ao criar um hidrômetro,é solicitado o setor a que ele pertence, nesse momento, é criado um banco para o setor (que é a névoa), caso não exista, e é inserido na tabela de hidrômetros, assim como, no momento que é criado um hidrômetro, também é criado uma tabela de histórico para ele. A cada interação com o banco é solicitado o id e o setor do hidrômetro para poder se buscar a tabela que ele existe. </p2> 
 
 # Demonstração 
 
 # Considerações finais 
