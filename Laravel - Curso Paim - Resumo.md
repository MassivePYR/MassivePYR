# Laravel - Curso Paim - Resumo

<b> Get-Post-Put-Patch-Delete-Options </b>
---

## Rotas (Routes) -> São os caminhos para uma aplicação, controlados pelo controller responsável

<b>web.php</b> -> registra as rotas que trabalham processando paginas no back-end e servindo de acordo com as requisições, permite cookies e sessão.

<b>api.php</b> -> registra as rotas de uma API, logo não suportam cookies e sessão, haja vista uma API ter proposito de responder dados as requisições feitas.

<b>channels.php</b> -> Rotas broadcast, transmição instantânea ex:livestream - a partir de web sockets, não necessita de requisições para atualizar o cliente.

<b>console.php</b> -> Serve para a criação de comandos personalizados que serão executados a partir do artisan.
```
Route::get($uri,$callback)
```
`uri -> rota`

`callback -> função que é executada quando se acessa esse "caminho"`

---

## Controladores (controllers) -> São os gerenciadores das actions relativas a uma ou mais rotas
os controllers servem para agrupar a logica do que deve ser feito em função da rota acessada por um determinado cliente.

Todo controller deve ser nomeado em CammelCase(XxxxxXxxx) e seguido de Controller no nome, uma boa pratica de programação

`artisan make:controller NomeController` - cria controller

app/http/controllers`- localização`

a "função" que é roda nas rotas na execução no 
```
Route::get('endereço('/')', callback(){
    return FunçãoDoController
    });
```
nesse caso chamamos essa função do controller de action. Um controlador pode ter varias actions.

Se passarmos para a rota duas "Strings":
```
Route::get('endereço('/')', "NomeDoController@Action");

Route::get('/', "PrincipalController@principal");   -   demostração

Route::get('/', [\app\http\controllers\PrincipalController::class, 'principal']);   -   Laravel 8.x+
```

o laravel compreende o que está descrito

---
## View's

Um dos metodos de processamento do Front-end, pelo servidor, do que vai ser servido/visto para o "Cliente" - visualmente

contém todo o HTML das paginas que serão processadas pelo back-end

`Resources\views` - localização

deve ser criado contendo "nome.blade.php" - padrão do blade, framework de views nativo do Laravel. - todo em lowercase

para chamar uma view é necessário chama-la no controller ex:

```
Class PrincipalController extends Controller{
    public function principal() {
        return view('nomeDaView')
    }
}
```
a Classe <b>Controller</b> que é extendida é nativa do framework. 

Além disso, se tua view estiver dentro de uma pasta dentro da pasta view ex: view\site\principal.blade.php deve ser chamada usando 'site.principal' o .blade.php deve ser omitido porque o framework já tem essa inteligencia.  

---
## Voltando as Rotas - Avançando com as Routes

### Enviando Parametros para as Rotas
Se na hora de chamar a rota der-mos a ela um "elemento" essa rota começará a esperar por parametros, para tal devemos fazer assim:
```
Route::get('/site.principal/{nome}', function(String $nome){
    echo 'Estamos Aqui: ' .$nome;
});
```
localhost/Joaquim -> "<b>Estamos aqui Joaquim</b>"

aqui o que importa é a sequencia dos parametros, logo, o nome da variável não é relevante, é utilizado o mesmo nome por ser uma boa pratica que facilita a legilidade do código.

Se quisermos receber mais parametros devemos concatená-los separados por '\' e '{}' ex:

```
Route::get('/site.principal/{nome}/{categoria}/{assunto}/{mensagem}', 
    function(String $nome, String $categoria, String $assunto, String $mensagem){
        echo "Estamos Aqui: $nome - $categoria - $assunto - mensagem";
    });
```
importante lembrar que se um parametro não for passado a rota não funcionará, retornará um erro 404

para dizer que não é obrigatório o envio de algum parametro colocamos "?" depois do nome do parametro Ex:

```
Route::get('/site.principal/{nome}/{categoria?}/{assunto?}/{mensagem?}', 
    function(String $nome, String $categoria, String $assunto, String $mensagem){
        echo "Estamos Aqui: $nome - $categoria - $assunto - mensagem";
    });
```
Assim, somente o nome será obrigatório para acessar esse metodo, cabe tratar como será cada tipo de resposta
um jeito de resolver isso é dar valores padrões aos elementos quando não obrigatorios Ex:
```
Route::get('/site.principal/{nome}/{categoria?}/{assunto?}/{mensagem?}', 
    function(
      String $nome,
      String $categoria = 'categoria não informada',
      String $assunto = 'assunto não informado',
      String $mensagem = 'mensagem não informada){
        echo "Estamos Aqui: $nome - $categoria - $assunto - mensagem";
    });
```
<b>lembrando sempre, parametros não obrigatórios devem ser 'enviados' juntos</b> não se pode enviar por exemplo um "nome?,categoria,assunto,mensagem?"

```
Route::get('/site.principal/{nome?}/{categoria}/{assunto}/{mensagem?}', 
      function(String $nome = 'Desconhecido',
        String $categoria,
        String $assunto,
        String $mensagem = 'mensagem não informada){
          echo "Estamos Aqui: $nome - $categoria - $assunto - mensagem";
    });
```

Isso aqui não existe ↑ não funciona!!!

O laravel não compreende o que você está querendo que aconteça elementos opcionais devem ser passados da direita para esquerda!!

### Tratando parametros de rotas com expressoes regulares

Para garantir a conformidade dos dados de entrada precisamos tratar esses recebimentos ex:
em um caso onde por exemplo a categoria é representada por um id devemos tratar para que só seja possivel enviar numeros para nossa rota:

```
Route::get('/site.principal/{nome?}/{categoria_id}, 
    function(
        String $nome = 'Desconhecido',
        String $categoria_id = 1   //1 - informação - exemplo 
        ) {
        echo "Estamos Aqui: $nome - $categoria_id";
    }->where('categoria_id','[0-9]+')); // ao menos um caractere de 0-9 deve ser enviado a partir desse tratamento
```
Se a rota receber algo diferente da condição anterior ele deve recusar essa requisição - <b>Erro 404</b>.

Lembrando tambem, que nesse último código o nome ainda não foi tratado então é viável receber caracteres fora do alfabeto como nome.
para tratar isso, podemos criar mais um tratamento chamando o método 'Where'

```
Route::get('/site.principal/{nome?}/{categoria_id}, 
    function(
        String $nome = 'Desconhecido',
        String $categoria_id = 1   //1 - informação - exemplo 
        ) {
        echo "Estamos Aqui: $nome - $categoria_id";
    }->where('categoria_id','[0-9]+')->where('nome','[A-Za-z]+'));
```
agora nome deve ter ao menos uma letra entre A-Z sendo maiúsculo ou minusculo. 

---
