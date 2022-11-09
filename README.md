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
- [Tecnologias utilizadas](#Tecnologias)
- [Solução](#Solução)
- [Componentes](#Componentes)
   - [Broker](#Broker)
   - [Hidrômetro](#Hidrômetro)
   - [Servidor](#Servidor)
   - [Nó](#Nó)
   - [Tela do usuário](#Usuário)
   - [Tela do administrador](#Administrador)
   - [API REST](#APIREST)
   - [Banco de dados](#dados)
- [Considerações finais](#consideracoes)




  
# Desenvolvedoras
<br /><a href="https://github.com/AndrezaNobrega">Andreza Nóbrega</a>




# Tecnologias
<ul>
  <li>MQTT</li>
  <li>Fog Computing</li>
  <li>Python</li>
  <li>Flask</li>
  <li>Pandas</li>
</ul>



# Solução

  &emsp; Como uma otimização do projeto anterior, foi proposta uma nova abordagem, dessa vez utilizando um modelo descentralizado. Portanto, a solução baseia-se sobretudo na **computação em névoa** para o melhor uso da rede, tempo de resposta, escalabilidade e até segurança do projeto. 
 
 &emsp; A computação em névoa é uma infraestrutura de computação descentralizada. Nela dados, computação, armazenamento e aplicativos estão localizados em algum lugar entre a fonte de dados e a nuvem. Assim como a computação de borda, a computação em névoa traz as vantagens e o poder da nuvem para mais perto de onde os dados são criados e utilizados. Inclusive, muitas pessoas usam os termos computação em névoa e computação de borda de forma intercambiável porque ambos envolvem trazer inteligência e processamento para mais perto de onde os dados são criados.  

&emsp; Para o desenvolvimento dessa infrastrutura foi utilizado o protocolo **MQTT** (*Message Queing Telemetry Transport*)  em protoloco de transporte de mensagens de formato Cliente/Servidor, a qual possibilita a comunicação entre máquinas (M2M) e para a conectivada de IoT (*internet of things*).
  
  &emsp; Logo, para funcionar, o protocolo MQTT utiliza um modelo de Publish/Subscribe, onde permite que o cliente faça postagens e/ou capte informações enquanto o servidor irá administrar esse envio e o recebido dos respectivos dados.    
   &emsp; Os maiores desafios desse problema, foram acerca de como usar essa 'névoa' de modo com que fosse possível otimizar o uso de todos os recursos. Para isso, foi pensada numa estruturação que trouxesse ligações que permitissem a troca de informações com o menor número de saltos possível, bem como, aproveitando ao máximo a rede. 
      <p align="center">
![image](https://user-images.githubusercontent.com/52046375/200188910-3593232b-196c-4bff-805c-388667ae3c07.png)
</p>

<h2>Restrições do projeto</h2>


   1. Nenhum usuário deve ultrapassar a média do consumo;
   2. Um usuário não deve ultrapassar um valor máximo em metros cúbicos;
   3. Visualizar N hidrômetros de maior consumo
   4. Selecionar um deles para visualizar os dados com o menor tempo de latência possível;
   
   <h2>   1. Nenhum usuário deve ultrapasar a média do consumo.</h2>
  
  <p align="center">
<img src="https://media.discordapp.net/attachments/975905192069435395/1038247676577329253/image.png?width=597&height=422"/>
</p>
 &emsp; A solução para essa restrição foi dada da seguinte maneira: 1. Os nós fazem um cálculo de suas respectivas médias. 2. Após isso, essas médias são enviadas para o servidor central, o qual faz o cálculo da média geral e retorna para todos os nós da rede. Esse corte é feito baseado em "ciclos", ao ser inicializado, o nó envia uma mensagem de inicialização, essa mensagem é usada pelo servidor central para verficar se todos os nós enviaram suas médias, caso a afirmação seja positiva, ele envia a média geral para todos os nós conectados. 
 
  &emsp; A cada ciclo de contagem, como mostrado na imagem, os hidrômetros que foram bloqueados na contagem anterior são desbloqueados, e então, a lista de hidrômetros conectados é percorrida novamente e os que estiverem acima da média são bloqeuados.



<h2>2. Um usuário não deve ultrapasar um valor máximo em metros cúbicos.</h2>
 &emsp; No problema, foi adotado um "teto de gastos", a cada contagem que o nó recebe, ele verifica se o hidrômetro passou do valor de teto. Há um valor de teto "default", que é o zero, nada acontece até que seja enviado um valor de teto pelo administrador. O valor é enviado para o servidor central, o qual encaminha para todos os nós conectados, onde ocorre a verificação e os possíveis cortes.




<h2>3. Visualizar N hidrômetros de maior consumo.</h2>

&emsp; A cada ciclo de contagem de um nó, é enviada uma lista ordena com hidrometros:gasto, o servidor central recebe e a ordena. O admin portanto, pode inserir o valor desejado para a visualização. Como o valor é indeterminado, pode ocorrer de não existir a quantidade pedida conectada à névoa, por isso, o servidor irá enviar todas as conexões de forma ordenada.



<h2>4. Selecionar um deles para visualizar os dados com o menor tempo de latência possível.</h2>
 
   ![recording](https://user-images.githubusercontent.com/52046375/200215750-3c9ea427-a549-4fdc-a514-0f6435508e5e.gif)
   
&emsp; Para essa solução, foi usada a tecnologia de <a href="https://www.educba.com/flask-websocket/">websockets</a>, neste caso da biblioteca Flask (Flask-SocketIO),  que é uma tecnologia a qual torna possível abrir uma sessão de comunicação interativa entre o navegador do usuário e um servidor. Com esta API, você pode enviar mensagens para um servidor e receber respostas orientadas a eventos sem ter que consultar o servidor para obter uma resposta.

&emsp; A API então se inscreve no tópico do hidrômetro, ela  envia as mensagem para o scrip JS, que exibe na página em em "tempo real".   
 
# Componentes 
 
<h2> - Broker</h2>

<p2>  &emsp; O intermediário no processo de comunicação. Elementos que desejam publicar informações o fazem também através do broker, enviando-lhe as informações que possuem. Os elemtos que desejam receber as informações então se inscrevem no broker, para receber. Toda essa conexão é feita através de tópicos.
 
&emsp; O tópico lembra o conceito de URI, com níveis separados por barras (/). Elementos da rede podem enviar diversos tópicos para o broker e subscritores podem escolher os tópicos que desejam subscrever.  Nesse projeto foi utilizado um broker, este então manipula todas as informações do projeto.<p2> Nesse projeto foi utilizado um broker, este então manipula todas as informações do projeto.
 
![image](https://user-images.githubusercontent.com/52046375/200466617-8e3783c3-8636-427d-9c2a-cabea6365746.png)

 


 <h2> - Hidrômetro</h2>

<p2>  &emsp; O hidrômetro funciona como o sensor do sistema,  ao inicializar, é possível escolher uma "tendência" para esse dispositivo, ele pode ter um consumo alto, médio ou baixo. O hidrômentro envia mensagens para o nó, assim atuando como publisher, também como subscriber, quando recebe a mensagem de bloqueio e desbloqueio, que é feita via MQTT . Assim, nele podemos verificar a vazão de água atual, o consumo total do período, status de vazamento e pode ser bloqueado por dois motivos: estar em débito e consumo maior que a média de consumo de todos os hidrômetros. Eles estão conectados ao nó da nuvem, que por sua vez, como agrupamento é chamado de setor.</p2>

<h2> - Servidor</h2>
 
<p2>  &emsp; O servidor central é responsável por manipular informações que precisam ser compartilhada entre todos os "setores", como enviando o teto de gastos para todos os nós, bem como  calcular a média geral de todo o sistema, elencar os hidrômetros com maior gasto de todo o sistema. Ou ainda, enviar todos os hidrômetros que possuem vazamento. O servidor também possui um  arquivo atrelado com todos os ID's de hidrômetros com possível vazamento. O servidor também atua como publisher e subscriber, enviando e recebendo informações.</p2> 
 
 ![image](https://user-images.githubusercontent.com/52046375/200473044-2baaef25-5649-4e53-a127-4f040f239a1e.png)

 
   <p align="center">
 *Exemplificação dos setores*
</p>



<h2> - Nó </h2>
<p2>  &emsp;  Os nós todos juntos compõe a névoa do sistema, eles possuem como banco de dados três planilhas: dadosGerais, que possui uma ocorrência de cada hidrômetro conectado com as informações mais atualizadas, o historicoGeralNo, onde estão presentes todas as informações de todos os nós, também há a planilha de pagamentos, onde estão as datas que devem ocorrer o pagamento das contas dos hidrômetros. 
 
 &emsp; O nó é o elemento com mais responsabilidades em todo o projeto, ele manipula as informações dos hidrômetros que são do seu setor, verificando seu histórico, verificando débito, retornando consumo e o valor da conta. Também, calcula a média, bloqueia e desbloqueia com base nesta média e no teto de gastos, e também retorna os hidrômetros elencados, com os com maiores gastos. 
 </p2>

<h2>- Tela do usuário</h2>
<p2> A tela do usuário consome a API usando a biblioteca requests, essa disponibiliza as opções. Para entrar na tela, deve-se informar sua ID e setor</p2>
 <ul>
  <li>1. Histórico de gastos</li>
  <li>2. Litros acumulados </li>
  <li>3. Valor da sua conta</li>
  <li>4. Pagar conta</li>
</ul>

<h2>- Tela do administrador</h2>
<p2> A tela do administrador consome a API usando a biblioteca requests, essa disponibiliza as opções. Para entrar na tela, deve-se informar a senha do adm *1234*</p2>
 <ul>
  <li>1. Envia teto de gastos</li>
  <li>2. Lista os N maiores hidrômetros </li>
  <li>3. Lista vazamento</li>
  <li>4. Verifica débito</li>
  <li>5. Bloqueio determinado hidrômetro</li>
  <li>6. Visualiza hidrômetro em tempo real</li>
</ul>

<h2>- API REST</h2>
<p2>  &emsp; A api se conecta com o nó e com o servidor via conexões MQTT, cada método envia uma mensagem para o elemento responsável por possui aquela informação, logo em seguida se inscreve no tópico para receber a resposta. A cada requisição é aberta e fechada a conexão. Todos os métodos seguem esse padrão.<p2> 

<h2>- Banco de dados</h2>
<p2>  &emsp; O "banco de dados" do projeto consiste em planilhas utilizadas para organizar os dados e dar a persistência. Foi utilizado durante todo o projeto a biblioteca Pandas para manipular os dados, inclusive para exportar os dados para a planilha e para ler novamente.</p2> 
 

 # Considerações finais 
<p2> &emsp; O projeto consegue realizar tudo dentro do previsto. Trouxe desafios na implementação e compreensão de protocolo mqtt, também possibilitou um estudo e reflexão mais aprofundada no que diz respeito ao que é a computação de borda. Algo que poderia ser adicionado em outras versões, é uma quantidade maior brokers, visto que é um servidor, o qual manipula todas as informações. Esses servidores poderiam ser separados por setores. No entanto, como o projeto ainda está em fase de projeto, não é prejudicado o seu desempenho. Também pode ser modificada a interface no terminal, e inserir uma interface web.
 
 &emsp; Também, as comunicações que não são "fixas" poderiam ser feitas todas em REST, não apenas centralizada como ocorre na versão atual. Isso deixaria a solução menos custosa e até mais rápida. O que facilitaria a descentralização total do projeto, não sendo dependente da API central mostrada. </p2> 
