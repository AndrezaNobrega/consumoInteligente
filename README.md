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

resoluçã

<h2>2. Um usuário não deve ultrapasar um valor máximo em metros cúbicos.</h2>
 &emsp; No problema, foi adotado um "teto de gastos", a cada contagem que o nó recebe, ele verifica se o hidrômetro passou do valor de teto. Há um valor de teto "default", que é o zero, nada acontece até que seja enviado um valor de teto pelo administrador. O valor é enviado para o servidor central, o qual encaminha para todos os nós conectados, onde ocorre a verificação e os possíveis cortes.


resoluçao

<h2>3. Visualizar N hidrômetros de maior consumo.</h2>

&emsp; A cada ciclo de contagem de um nó, é enviada uma lista ordena com hidrometros:gasto, o servidor central recebe e a ordena. O admin portanto, pode inserir o valor desejado para a visualização. Como o valor é indeterminado, pode ocorrer de não existir a quantidade pedida conectada à névoa, por isso, o servidor irá enviar todas as conexões de forma ordenada.

resolução

<h2>4. Selecionar um deles para visualizar os dados com o menor tempo de latência possível.</h2>
 
   ![recording](https://user-images.githubusercontent.com/52046375/200215750-3c9ea427-a549-4fdc-a514-0f6435508e5e.gif)
   
&emsp; Para essa solução, foi usada a tecnologia de <br /><a href="https://www.educba.com/flask-websocket/">websockets</a>, neste caso da biblioteca Flask, (Flask-SocketIO)  que é uma tecnologia a qual torna possível abrir uma sessão de comunicação interativa entre o navegador do usuário e um servidor. Com esta API, você pode enviar mensagens para um servidor e receber respostas orientadas a eventos sem ter que consultar o servidor para obter uma resposta.

&emsp; Nesse caso, a API se inscreve no tópico do hidrômetro, a API então envia as mensagem para o scrip JS, que exibe na página em em "tempo real".   
 
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
 

 # Considerações finais 
