# Laravel - Curso Paim - Resumo
esse resumo foi feito pra você que como eu prefere ler do que ter que assistir vídeos, tentei fazer a melhor sintese do que é necessário para cada processo e como o executar.

<b> Get-Post-Put-Patch-Delete-Options </b> 
---
Se tu não sabe o que é vá estudar "http" dps volta aí.

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
    function(
        String $nome = 'Desconhecido',
        String $categoria,
        String $assunto,
        String $mensagem = 'mensagem não informada){
        echo "Estamos Aqui: $nome - $categoria - $assunto - mensagem";
    });
```

Isso aqui não existe ↑ não funciona!!!

O laravel não compreende o que você está querendo que aconteça elementos opcionais devem ser passados da direita para esquerda!!

### Tratando parametros de rotas com expressoes regulares (Elimina a chance de receber uma requisição invalida)

Para garantir a conformidade dos dados de entrada precisamos tratar esses recebimentos ex:
em um caso onde por exemplo a categoria é representada por um id devemos tratar para que só seja possivel enviar numeros para nossa rota:

```
Route::get('/site.principal/{nome?}/{categoria_id}, 
    function(
        String $nome = 'Desconhecido',
        String $categoria_id = 1   //1 - informação - exemplo 
        ) {
        echo "Estamos Aqui: $nome - $categoria_id";
    }->where('categoria_id','[0-9]+'));
```

ao menos um caractere de 0-9 deve ser enviado a partir desse tratamento,
se a rota receber algo diferente da condição anterior ele deve recusar essa requisição - <b>Erro 404</b>.

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
#### Listar rotas
o artisan varios comando e um para mostrar as rotas sendo utilizadas é o comando Route List "artisan route:list"

## Agrupando Rotas (gera maior organização -- aproxima do Restfull)
excelente para paginas que precisam de autenticação para o acesso

usa-se então o comando:
```
Route::Prefix('/"o Prefixo"')->group(function(){
    espera que se coloque aqui as rotas que utilizaram o prefixo ex:
    Route::get('/clientes', function(){
        return 'Clientes'; - essa linha não é a melhor forma de trazer uma resposta
                            mas por via de ensinar o uso do 'prefix'... é um callback... só pra esclarecer
        });
});
```
exemplo
```
Route::Prefix('/app')->group(function(){
    Route::get('/clientes', function(){
        return 'Clientes';
        });
});
```
## Nomeando Rotas (bastante importante para manutenção de código)
é muito necessário essa execução para desacoplar a rota propriamente dita do elemento
evita a dependência direta do nome da rota; evita quebrar código; centraliza as modificações no controller

pra ficar mais visivel vou utilizar um codigo um pouco maior
```
Route::get('/', [\app\http\controllers\PrincipalController::class, 'principal'])->name('site.index');
Route::get('/sobre-nos', [\app\http\controllers\SobreNosController::class, 'principal'])->name('site.sobrenos');
Route::get('/contato', [\app\http\controllers\ContatoController::class, 'principal'])->name('site.contato');
Route::get('/login', [\app\http\controllers\LoginController::class, 'principal'])->name('site.login');

Route::prefix('/app')->group(function(){
    Route::get('/clientes', function(){return 'Clientes';})->name('app.clientes');
    Route::get('/fornecedores', function(){return 'Fornecedores';})->name('app.fornecedores');
    Route::get('/produtos', function(){return 'Produtos';})->name('app.produtos');
});
```
a função name renomeia a rota para um nome "simplificado", o acesso a rota continua o mesmo, esse "nome" serve para dentro da propria logica da aplicação ... um apelido que facilita a ser chamado no código. exemplo no HTML

```
o que antes seria assim, com a rota absoluta
<a href="/Principal">principal</a>

pode agora ser chamado pela função Route usando o "apelido"
<a href="{{ Route(site.index')}}>principal</a>
```

## Redirecionamento de Rota
Te permite direcionar o fluxo de navegação do usuário pela aplicação web, permitindo levar o usuário de uma pagina a outra, exemplo de uma campanha ou uma pagina de sucesso.. Um exemplo desse redirecionamento:
assim seria a primeira implementação das rotas "rota1" e "rota2":
```
Route::get('/rota1', function(){
    echo 'Rota 1';
    })->name('app.rota1');

Route::get('/rota2', function(){
    echo 'Rota 2';
    })->name('app.rota2');
```
alguns metodos de redirecionamento:

```
Route::redirect('rota2','rota1'); - um metodo de redirecionamento

Route::get('/rota2', function(){
    return redirect()->route('app.rota1'); - redirecionamento no metodo de callback
    })->name('app.rota2');
```
o terceiro metodo seria pelo controller o que é mais comumente usado;

## Rota de Fallback (evita a mula de sair do eixo).
"uma rota de contingência, envia o usuário para essa pagina caso a rota que o usuario acessou não for encontrada" evita erros...

pode ser implementada assim.
```
Route::fallback(function(){
    //poderia apontar para um controllador, poderia ser retornado uma view, mas no nosso caso por agora..

    echo "A rota acessada não existe. <a href="'.route('site.index').'">Clique aqui</a> para ir para pagina inicial"
})
```
## Encaminhando parametros para o controlador
é meio que obvio o que isso faz pelo titulo mas... para que isso ocorra, é necessário uma rota que receba elementos e os direcione para o controlador 

para efeitos de teste criaremos um do zero
```
Route::get('/teste/{p1}/{p2}',[\app\http\controllers\TesteController::class, 'teste'])->name('teste'); "versão Laravel 8.x+"
```
então criamos o controlador usando o artisan: `"sail ou php" artisan make:controller TesteController`

cria-se então a função padrão dentro do controller 
```
Class TesteController extends Controller{
    public function teste(int $p1, int $p2){ // o nome das variaveis não precisa ser o mesmo da rota do controller
        //daí então usa esses elementos para o que tu quer fazer.. 

        echo "A soma de $p1 + $p2 é: ".($p1+$p2); // exemplo uma soma desses parametros
    }
}
```

## // Do controlador para a "view"
seguindo o pensamento do capitulo anterior, seguiremos a mesma ideia usando a rota "teste" e o controlador "TesteController". Então, agora faremos uma view 'teste.blade.php' para continuar o pensamento.. antes, vamos adicionar um return dentro de nossa função teste dentro do controller assim:
```
Class TesteController extends Controller{
    public function teste(int $p1, int $p2){
        return view('site.teste') 
        //site. por a view estar dentro da pasta site nesse caso, não é obrigatório
    }
}
```
### Array Associativo
aqui seria assim:
```
Class TesteController extends Controller{
    public function teste(int $p1, int $p2){
        return view('site.teste',['p1' => $p1,'p2' => $p2])
    }
}
```
p1 e p2 serão recebidos como variáveis e "site." por a view estar dentro da pasta site nesse caso, não é obrigatório

`como boa prática é ótimo útilizar o índice do array associativo o nome da própria variável.`

dentro da view:
```
P1 = {{ $p1 }}
<br/>
P2 = {{ $p2 }}

```

### Compact() - nativo do php
no compact o codigo já fica um pouco mais simples, o compact do php localiza na entrada da função no controller as variaveis que são chamadas como String

```
Class TesteController extends Controller{
    public function teste(int $p1, int $p2){
        return view('site.teste', compact('p1','p2'));
    }
}
```
por ser php, usa-se aspas simples e não é necessário usar o "$", a view fica da mesma forma que a no array associativo.
 

### With() - do FrameWork Laravel
tem menos chances de ser usado, as estruturas são as mesmas só muda o return do TesteController
```
Class TesteController extends Controller{
    public function teste(int $p1, int $p2){
        return view('site.teste')->with('p1', $p1)->with('p2', $p2);
    }
}
```
já é bem claro o porque ser pouco ou não utilizado,
o casting é feito de forma singular, então, necessita ser chamado, o método, toda vez que for passar alguma variável.
com 2 o código já fica maior do que o "compact".

---
