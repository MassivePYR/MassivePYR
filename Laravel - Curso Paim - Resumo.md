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

a "função" que é rodada nas rotas na execução no controller é chamada de action.
```
Route::get('endereço('/')', callback(){
    return FunçãoDoController
    });
```
Um controlador pode ter varias actions.

Se passarmos para a rota duas "Strings":
```
Route::get('endereço('/')', "NomeDoController@Action");

Route::get('/', "PrincipalController@principal");   -   demostração

Route::get('/', [\app\http\controllers\PrincipalController::class, 'principal']);   -   Laravel 8.x+
```

o laravel compreende o que está descrito diretamente na rota e executa a action do controller.

---
## View's

Um dos métodos de processamento do Front-end, pelo servidor, do que vai ser servido/visto para o "Cliente" - visualmente

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

# Voltando as Rotas - Avançando com as Routes

## Enviando Parametros para as Rotas
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
<b>Lembrando sempre, parametros não obrigatórios devem ser 'enviados' juntos</b> não se pode enviar por exemplo um "nome?,categoria,assunto,mensagem?"

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

## Tratando parametros de rotas com expressoes regulares (Elimina a chance de receber uma requisição invalida)

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

### Listar rotas
o artisan varios comando e um para mostrar as rotas sendo utilizadas é o comando Route List "artisan route:list"

## Agrupando Rotas (gera maior organização -- aproxima do Restfull)
excelente para paginas que precisam de autenticação para o acesso

usa-se então o comando:
```
Route::Prefix('/"o Prefixo"')->group(function(){
    espera que se coloque aqui as rotas que utilizaram o prefixo ex:
    Route::get('/clientes', function(){
        return 'Clientes'; - essa linha não é a melhor forma de trazer uma resposta mas por via de ensinar o uso do 'prefix'... é um callback... só pra esclarecer
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
## ... Do controlador para a "view"
seguindo o pensamento do capitulo anterior, seguiremos a mesma ideia usando a rota "teste" e o controlador "TesteController". Então, agora faremos uma view 'teste.blade.php' para continuar o pensamento.. antes, vamos adicionar um return dentro de nossa função teste dentro do controller assim:
```
Class TesteController extends Controller{
    public function teste(int $p1, int $p2){
        return view('site.teste') 
        //site. por a view estar dentro da pasta site nesse caso, não é obrigatório
    }
}
```
## Array Associativo
nesse método seria assim:
```
Class TesteController extends Controller{
    public function teste(int $p1, int $p2){
        return view('site.teste',['p1' => $p1,'p2' => $p2])
    }
}
```
p1 e p2 serão recebidos como variáveis dentro da view.

`como uma boa prática é ótimo útilizar no nome do índice do array associativo o nome da própria variável.`

dentro da view:
```
P1 = {{ $p1 }}
<br/>
P2 = {{ $p2 }}
```
## Compact() - nativo do php
no compact o codigo já fica um pouco mais simples, o compact do php localiza na entrada da função no controller as variaveis que são chamadas como String
```
Class TesteController extends Controller{
    public function teste(int $p1, int $p2){
        return view('site.teste', compact('p1','p2'));
    }
}
```
por ser php, usa-se aspas simples e não é necessário usar o "$", a view fica da mesma forma que a no array associativo.

## With() - do FrameWork Laravel
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

## .. Do controlador para a "view" - com Strings - dica do Copilot

### Passando um array para a view - copilot mode - usando o compact()
```
Class TesteController extends Controller{
    public function teste(int $p1, int $p2){
        $array = [
            'nome' => 'João',
            'sobrenome' => 'Silva',
            'idade' => '30'
        ];
        return view('site.teste', compact('p1','p2','array'));
    }
}
```
dentro da view:
```
P1 = {{ $p1 }}
<br/>
P2 = {{ $p2 }}
<br/>
Nome = {{ $array['nome'] }}
<br/>
Sobrenome = {{ $array['sobrenome'] }}
<br/>
Idade = {{ $array['idade'] }}
```
* na penta geralmente fazemos qualquer retorno de dados direto do controller para a view como json.

as partes do Blade Foram puladas por não serem tão importantes para o momento, mas, é importante saber que existe e que é uma ferramenta muito poderosa.

# Uma leve passada no PHP/blade - Dicionário de ferramentas do Blade/PHP
@dd - dump and die - mostra o que tem dentro da variável e para a execução do código

```
@dd($array)
```

@dump - mostra o que tem dentro da variável
```
@dump($array)
```

## @if/@else
estrutura condicional
```	
@if($p1 > $p2)
    <p>P1 é maior que P2</p>
@elseif($p1 == $p2)
    <p>P1 é igual a P2</p>     - no blade
@else
    <p>P1 é menor que P2</p>
@endif
```
```	
@php
    if($p1 > $p2){
        echo 'P1 é maior que P2';
    }elseif($p1 == $p2){
        echo 'P1 é igual a P2';   - no php
    }else{
        echo 'P1 é menor que P2';
    }
@endphp
```

## @unless
o inverso do if

```
@unless($p1 == $p2)
    <p>P1 é diferente de P2</p>
@endunless
```

em php o mais proximo seria o if not if(!(condição)) ou if(x1 != x2), ex:

```
@php
    if($p1 != $p2){
        echo 'P1 é diferente de P2';
    }
@endphp
```

## @isset - verifica se a variável existe.
se sim, executa o que está dentro do bloco

```
@isset($p1)
    <p>P1 existe</p>
@endisset
```

```
@php
    if(isset($p1)){
        echo 'P1 existe';
    }
@endphp
```

## @empty
verifica se a variável está vazia, se sim, retorna true.

```
@empty($p1)
    <p>P1 não existe</p>
@endempty
```

```
@php
    if(empty($p1)){
        echo 'P1 não existe';
    }
@endphp
```

## Ternário - operador ternário
é um if simplificado

```
<p>{{ $p1 > $p2 ? 'P1 é maior que P2' : 'P1 é menor que P2' }}</p>
```

```
@php
    echo $p1 > $p2 ? 'P1 é maior que P2' : 'P1 é menor que P2';
@endphp
```

## ?? - Null Coalesce
verifica se a variável existe, se sim, retorna o valor dela, se não, retorna o valor padrão

```
<p>{{ $p1 ?? 'Não existe' }}</p>
```

```
@php
    echo $p1 ?? 'Não existe';
@endphp
```

## @switch/@case/@break/@default
switch é um if com várias condições, ou seja, se alguma condição for verdadeira, ele executa o bloco referente a ela

```
@switch($p1)
    @case(1)
        <p>É igual a 1</p>
        @break
    @case(2)
        <p>É igual a 2</p>
        @break
    @case(3)
        <p>É igual a 3</p>
        @break
    @default
        <p>Não é igual a 1, 2 ou 3</p>
@endswitch
```

```
@php
    switch($p1){
        case 1:
            echo 'É igual a 1';
            break;
        case 2:
            echo 'É igual a 2';
            break;
        case 3:
            echo 'É igual a 3';
            break;
        default:
            echo 'Não é igual a 1, 2 ou 3';
    }
@endphp
```

## @for/@endfor
for é um laço de repetição "para", ou seja, para cada iteração, ele executa o bloco

```
@for($i = 0; $i < 10; $i++)
    <p>Valor: {{ $i }}</p>
@endfor
```

```
@php
    for($i = 0; $i < 10; $i++){
        echo 'Valor: '.$i;
    }
@endphp
```

## @while/@endwhile
while é um laço de repetição "enquanto", ou seja, enquanto a condição for verdadeira, ele executa o bloco

```
@php
    $i = 0;
@endphp
@while($i < 10)
    <p>Valor: {{ $i }}</p>
    @php
        $i++;
    @endphp
@endwhile
```

```
@php
    $i = 0;
    while($i < 10){
        echo 'Valor: '.$i;
        $i++;
    }
@endphp
```

## @foreach/@endforeach
foreach é um laço de repetição para arrays e coleções de dados (objetos) "para cada"

```
@foreach($array as $key => $value)
    <p>Chave: {{ $key }} - Valor: {{ $value }}</p>
@endforeach
```

```
@php
    foreach($array as $key => $value){
        echo 'Chave: '.$key.' - Valor: '.$value;
    }
@endphp
```

## @forelse/@empty/@endforelse
forelse é um foreach com else, ou seja, se o array estiver vazio, ele executa o else ao invés do foreach

```
@forelse($array as $key => $value)
    <p>Chave: {{ $key }} - Valor: {{ $value }}</p>
@empty
    <p>Não existem registros</p>
@endforelse
```

```
@php
    if(count($array) > 0){
        foreach($array as $key => $value){
            echo 'Chave: '.$key.' - Valor: '.$value;
        }
    }else{
        echo 'Não existem registros';
    }
@endphp
```

## @continue/@break
continue - pula para a próxima iteração do laço

break - sai do laço

```
@foreach($array as $key => $value)
    @continue($key == 'p1')
    <p>Chave: {{ $key }} - Valor: {{ $value }}</p>
    @break($key == 'p2')
@endforeach
```

```
@php
    foreach($array as $key => $value){
        if($key == 'p1'){
            continue;
        }
        echo 'Chave: '.$key.' - Valor: '.$value;
        if($key == 'p2'){
            break;
        }
    }
@endphp
```
## @loop/@first/@last
loop - variável que contém informações sobre o laço atual

first - verifica se é a primeira iteração

last - verifica se é a última iteração
```
@foreach($array as $key => $value)
    @if($loop->first)
        <p>Primeira iteração</p>
    @endif
    <p>Chave: {{ $key }} - Valor: {{ $value }}</p>
    @if($loop->last)
        <p>Última iteração</p>
    @endif
@endforeach
```
```
@php
    foreach($array as $key => $value){
        if($key == 0){
            echo 'Primeira iteração';
        }
        echo 'Chave: '.$key.' - Valor: '.$value;
        if($key == count($array) - 1){
            echo 'Última iteração';
        }
    }
@endphp
```
## @count/@endcount
count - conta a quantidade de elementos de um array ou coleção
```
<p>Quantidade: {{ count($array) }}</p>
```
```
@php
    echo 'Quantidade: '.count($array);
@endphp
```
pode ser utilizado em conjunto com o loop para saber a quantidade de iterações
```
@foreach($array as $key => $value)
    <p>Chave: {{ $key }} - Valor: {{ $value }}</p>
    @if($loop->count == 1)
        <p>Única iteração</p>
    @endif
@endforeach
```
```
@php
    foreach($array as $key => $value){
        echo 'Chave: '.$key.' - Valor: '.$value;
        if(count($array) == 1){
            echo 'Única iteração';
        }
    }
@endphp
```
## @include/@includeIf/@includeWhen/@includeFirst/@each
include - inclui uma view

includeIf - inclui uma view se a condição for verdadeira

includeWhen - inclui uma view quando a condição for verdadeira

includeFirst - inclui a primeira view que existir

each - inclui uma view para cada elemento de um array ou coleção
```
@include('site.includes.sidebar')
```
```
@includeIf('site.includes.sidebar')
```
```
@includeWhen($p1 == $p2, 'site.includes.sidebar')
```
```
@includeFirst(['site.includes.sidebar', 'site.includes.sidebar2'])
```
```
@each('site.includes.sidebar', $array, 'value')
```
## @stack/@push/@prepend
stack - cria uma pilha de conteúdo

push - adiciona conteúdo na pilha

prepend - adiciona conteúdo no início da pilha

```
@stack('scripts')
```
```
@push('scripts')
    <script>
        alert('Teste');
    </script>
@endpush
```
```
@prepend('scripts')
    <script>
        alert('Teste');
    </script>
@endprepend
```
## @section/@endsection/@show/@yield/@extends
section - define uma seção de conteúdo

endsection - finaliza uma seção de conteúdo

show - exibe o conteúdo de uma seção

yield - exibe o conteúdo de uma seção

extends - define que a view estende outra view

``` 
@section('titulo', 'Título da página')
```
```
@section('conteudo')
    <p>Conteúdo da página</p>
@endsection
```
```
@section('conteudo')
    <p>Conteúdo da página</p>
@show
```
```
@section('conteudo')
    <p>Conteúdo da página</p>
@yield('conteudo')
```
```
@extends('site.layouts.basico')
```
## @auth/@endauth/@guest/@endguest
auth - verifica se o usuário está autenticado

endauth - finaliza a verificação de autenticação

guest - verifica se o usuário não está autenticado

endguest - finaliza a verificação de não autenticação
```
@auth
    <p>Usuário autenticado</p>
@endauth
```
```
@guest
    <p>Usuário não autenticado</p>
@endguest
```
# @csrf
o que é o token @crsf e para que serve?

o token crsf é um método de segurança que o laravel utiliza para evitar ataques de cross-site request forgery,
ou seja, é um token que é gerado pelo laravel e que é enviado para o navegador do usuário,
e quando o usuário envia um formulário, esse token é enviado junto, e o laravel verifica se o token é válido,
se for, o formulário é processado, se não, o formulário é rejeitado.

# Models
Models são as classes que representam as tabelas do banco de dados, ou seja,
são as classes que representam os dados da aplicação.

Dentro das models também são criados os relacionamentos entre as tabelas regra de negócio
(1-n, n-n, 1-1, etc...) usando o ORM Eloquent,
os termos só diferem em serem escritos por extenso em inglês.(onehasmany, manytomany, onetoone, etc...)

## Criando um model
para criar um model, basta executar o comando artisan make:model NomeModel
```
php artisan make:model Cliente -mrc
```
o parâmetro -mrc cria o model, a migration, o controller e as rotas para o controller

o mrc é flexivel, pois é um conjunto de comandos que podem ser usados separadamente, por exemplo, se eu quiser criar apenas o model e a migration, eu posso executar o comando:
```
php artisan make:model Cliente -m
```
## Criando uma migration
uma migration é um arquivo que contém as instruções para criar uma tabela no banco de dados.

para criar uma migration, basta executar o comando artisan make:migration NomeMigration
```
php artisan make:migration create_clientes_table
```

criou uma tabela que não precisava? não tem problema, basta executar o comando artisan migrate:rollback
```
php artisan migrate:rollback --step=1
```
o parâmetro --step=1 define quantas migrations serão desfeitas, se não for definido, todas as migrations serão desfeitas.

precisa desfazer todas as migrations? basta executar o comando artisan migrate:reset
```
php artisan migrate:reset
```
precisa adicionar mais informações na tabela? basta criar uma nova migration
```
php artisan make:migration add_campo_to_clientes_table
```
ou editar a migration existente e executar o comando artisan migrate:refresh
```
php artisan migrate:refresh
```
## adicionando chaves estrangeiras
### 1:1
primeiro, é necessário criar a migration da tabela que receberá a chave estrangeira nesse exemplo, a tabela produtos já existe(tabela origem), então, basta criar a tabela relação "produtos_detalhes" onde serão contidos os detalhes dos produtos.
```
php artisan make:migration create_produtos_detalhes_table
```
assim, é criada a migration da tabela produtos_detalhes já com o down function básico implementado, então, basta adicionar os campos que serão necessários
```
Schema::create('produtos_detalhes', function (Blueprint $table) {
    //colunas
    $table->id();
    $table->unsignedBigInteger('produto_id');
    $table->float('comprimento', 8, 2);
    $table->float('largura', 8, 2);
    $table->float('altura', 8, 2);
    $table->timestamps();

    //constraint
    $table->foreign('produto_id')->references('id')->on('produtos');
    $table->unique('produto_id'); //garante o relacionamento 1:1
});
```
dessa forma só é necessário executar o comando artisan migrate e a tabela será criada.

### 1:n
... continuando o exemplo anterior, agora, uma tabela chamada unidades que se relaciona com a tabela produtos e produtos_detalhes. todo esse processo é muito parecido com o anterior, a diferença é que agora é que não temos o constraint unique, que limitava o relacionamento anterior a 1:1. além disso quem recebe a chave estrangeira é a tabela produtos_detalhes e a tabela produtos.
```
php artisan make:migration create_unidades_table
```
```
Schema::create('unidades', function (Blueprint $table) {
    //colunas
    $table->id();
    $table->string('unidade', 5); //cm, mm, kg, g, etc...
    $table->string('descricao', 30);
    $table->timestamps();

    // adicionando o relacionamento com a tabela produtos.
    schema::table('produtos', function(Blueprint $table){
        $table->unsignedBigInteger('unidade_id');
        $table->foreign('unidade_id')->references('id')->on('unidades');
    });

    // adicionando o relacionamento com a tabela produtos_detalhes.
    schema::table('produtos_detalhes', function(Blueprint $table){
        $table->unsignedBigInteger('unidade_id');
        $table->foreign('unidade_id')->references('id')->on('unidades');
    });

    // além disso resta implementar o down function.
    public function down()
    {
        Schema::table('produtos', function(Blueprint $table){
            $table->dropForeign('produto_unidade_id_foreign'); //[tabela]_[coluna]_foreign - nome padrão do laravel
            $table->dropColumn('unidade_id');
        });

        Schema::table('produtos_detalhes', function(Blueprint $table){
            $table->dropForeign('produto_detalhes_unidade_id_foreign');
            $table->dropColumn('unidade_id');
        });

        Schema::dropIfExists('unidades');
    }
    //usa a lógica inversa da criação da tabela para desfazer as alterações.
});
```
tudo pronto, basta executar o comando artisan migrate e as tabelas serão criadas.

### n:n
... continuando o mesmo projeto, criaremos uma tabela chamada filiais, para temos um relacionamento n:n com a tabela produtos é necessário criar uma tabela relacionamento, que no caso será a tabela produto_filiais.
```
php artisan make:migration ajuste_produtos_filiais
```
```
no up function:

//criando a tabela filiais
    Schema::create('filiais', function (Blueprint $table) {
        $table->id();
        $table->string('filial', 30);
        $table->timestamps();
    });

//criando a tabela produto_filiais
    Schema::create('produto_filiais', function (Blueprint $table) {
        $table->id();
        $table->unsignedBigInteger('filial_id');
        $table->unsignedBigInteger('produto_id');
        $table->decimal('preco_venda', 8, 2);
        $table->integer('estoque_minimo');
        $table->integer('estoque_maximo');
        $table->timestamps();

        //foreign keys (constraints)
        $table->foreign('filial_id')->references('id')->on('filiais');
        $table->foreign('produto_id')->references('id')->on('produtos');
    });

    //removendo colunas da tabela produtos
    Schema::table('produtos', function(Blueprint $table){
        $table->dropColumn(['preco_venda', 'estoque_minimo', 'estoque_maximo']);
    });

no down function:

    //adicionar colunas da tabela produtos
    Schema::table('produtos', function(Blueprint $table){
        $table->decimal('preco_venda', 8, 2);
        $table->integer('estoque_minimo');
        $table->integer('estoque_maximo');
    });
    
    Schema::dropIfExists('produto_filiais');
    Schema::dropIfExists('filiais');
```
tudo pronto, basta executar o comando artisan migrate e as tabelas serão criadas.

## Migrate After
por padrão, as migrations são executadas em ordem alfabética, mas, e se eu quiser que uma migration seja executada depois de outra? se eu já tiver criado a tabela mas queira a re-orderar? basta adicionar o atributo after na migration.

primeiro criaremos uma migration alter_fornecedores_table
```
php artisan make:migration alter_fornecedores_nova_coluna_site_com_after
```
na function up, adicionaremos a coluna site depois da coluna nome
```
Schema::table('fornecedores', function(Blueprint $table){
    $table->string('site', 150)->after('nome')->nullable();
});
```
na function down, removeremos a coluna site
```
Schema::table('fornecedores', function(Blueprint $table){
    $table->dropColumn('site');
});
```
agora basta executar a migration, pronto.

## Status, Reset, Refresh e Fresh

Status -> mostra o status das migrations
```
php artisan migrate:status
```
Reset -> desfaz todas as migrations
```
php artisan migrate:reset
```
Refresh -> desfaz todas as migrations e executa novamente
```
php artisan migrate:refresh
```
Fresh -> desfaz todas as migrations e executa novamente, mas, não executa as migrations que já foram executadas
```
php artisan migrate:fresh
```
## Rollback

Rollback -> desfaz a última migration
```
php artisan migrate:rollback
```
Rollback --step=2 -> desfaz as duas últimas migrations
```
php artisan migrate:rollback --step=2
```
# Eloquente ORM
ORM (Object Relational Mapping) é um mapeamento objeto-relacional, ou seja, é uma técnica de desenvolvimento que consiste em mapear as tabelas do banco de dados em classes e os registros das tabelas em objetos.

Eloquent é o ORM do Laravel, ele é responsável por fazer o mapeamento objeto-relacional. O Eloquent é uma implementação do Active Record, que é um padrão de projeto que mapeia as tabelas do banco de dados em classes e os registros das tabelas em objetos.

## Tinker
Tinker é uma ferramenta que permite executar comandos do Laravel através do terminal, é muito útil para testar o código.
para acessar o tinker, basta executar o comando artisan tinker
```
php artisan tinker
```
### Criando um registro
para criar um registro, basta instanciar a classe e atribuir os valores aos atributos
```
$cliente = new \App\Cliente();
$cliente->nome = 'João';
$cliente->telefone = '11 99999-9999';
Print_r($cliente->getAttributes()); // serve para mostrar os atributos do objeto instanciado
```

em seguida, basta executar o método save()
```
$cliente->save();
```

### Ajustando o nome da tabela no Model para um correto ORM
o Eloquent parte do nome da classe para definir a tabela que está escrita no padrão camelCase, ex:
```
SiteContato
```
o Eloquent entende que a tabela é site_contatos 
pois sempre que hover uma letra maiúscula,
ele adiciona um underline antes da letra maiúscula e transforma todas as letras em minúsculas e adiciona um "s" no final.

porém, se o nome da classe for Fornecedor, o Eloquent entende que a tabela é fornecedors, pois, ele não entende que o plural de fornecedor é fornecedores, para isso, é necessário definir o nome da tabela no model.
```
class Fornecedor extends Model
{
    protected $table = 'fornecedores';
}
```
quando nomear uma tabela e necessário fechar o tinker e abrir novamente para que o tinker reconheça a alteração.

### Create e Fillable
primeiro de tudo, o metodo create() é um metodo estatico, cabe a nos sabermos a diferença entre o metodo estático e o metodo convencional.

o metodo estático não depende da instancia de um objeto para ser executado, ou seja, não é necessário instanciar a classe para executar o metodo, ex:
```
\App\Cliente::create(['nome' => 'Maria', 'telefone' => '11 99999-9999']);
```
o metodo convencional depende da instancia de um objeto para ser executado, ou seja, é necessário instanciar a classe para executar o metodo, ex:
```
$cliente = new \App\Cliente();
$cliente->nome = 'João';
$cliente->telefone = '11 99999-9999';
$cliente->save();
```
para usar o create é necessario preencher o atributo fillable no model, ex:
```
class Cliente extends Model
{
    protected $fillable = ['nome','telefone'];
}
```
novamente é necessário fechar o tinker e abrir novamente para que o tinker reconheça a alteração.

## selecionando registros

### all()
o metodo all() retorna todos os registros da tabela
```
\App\Cliente::all();
```
lembrando que podemos usar o dd()->toArray() para ver o resultado do metodo
```
dd(\App\Cliente::all()->toArray());
```
ou mesmo dentro do print_r
```
print_r(\App\Cliente::all()->toArray());
```
ou ainda um foreach
```
foreach(\App\Cliente::all() as $key => $value){
    echo $value->nome; echo '<br/>';
}
```
dando caracteristicas ao Output

### find()
o metodo find() retorna um registro específico da tabela, a diferença é que o find() recebe a primary_key, o id, do registro como parâmetro
```
\App\Cliente::find(1);
```
### where()
o metodo where() retorna um ou mais registros da tabela
esse metodo diferente do metodo all() e find() é na verdade um construtor, ele permite que sejam adicionados mais metodos a ele para construir uma query mais complexa de acesso aos registros no banco de dados.
```
*where(comparação)operadores logicos(comparação);
```
temos os principais operadores logicos:
```
> maior que
< menor que
>= maior ou igual que
<= menor ou igual que
<> - diferente de
like - semelhante a
```
exemplo:
```
use \App\Cliente;
$clientes = Cliente::where('nome', 'João')->get();
```
ainda temos o operador == que pode ser omitido, ex:
```
use \App\Cliente;
$clientes = Cliente::where('nome', 'João')->get();
```
por fim temos o operador like que é usado para buscar registros semelhantes, ex:
```
use \App\Cliente;
$clientes = Cliente::where('nome', 'like', '%a%')->get();
```
nesse caso, o like busca todos os registros que contenham a letra "a" no nome.
não importando o que vem antes ou depois da letra "a".

### Wherein()
o metodo wherein() retorna um ou mais registros da tabela, a diferença é que o wherein() recebe um array como parâmetro
```
use \App\Cliente;
$clientes = Cliente::wherein('motivo_contato', [1,3])->get();
```
nesse caso, o wherein() busca todos os registros que contenham os valores 1 ou 3 no campo motivo_contato.

### WhereNotin()
já no metodo wherenotin() é o inverso, ou seja, busca todos os registros que não contenham os valores 1 ou 3 no campo motivo_contato.
```
use \App\Cliente;
$clientes = Cliente::wherenotin('motivo_contato', [1,3])->get();
```
### WhereBetween()
o metodo wherebetween() retorna um ou mais registros da tabela, a diferença é que o wherebetween() busca os registros que estão entre os valores passados como parâmetro
```
use \App\Cliente;
$clientes = Cliente::wherebetween('id', [1,3])->get();
```
nesse caso, o wherebetween() busca todos os registros que contenham os valores entre 1 e 3 no campo id.

### WhereNotBetween()
já no metodo wherenotbetween() é o inverso, ou seja, busca todos os registros que não contenham os valores entre 1 e 3 no campo id.
```
use \App\Cliente;
$clientes = Cliente::wherenotbetween('id', [1,3])->get();
```
### Selecionando registros com dois ou mais "Wheres"
para selecionar registros com dois ou mais wheres, basta encadear os metodos where(), ex:
```
use \App\Cliente;
$clientes = Cliente::where('nome','<>','João')->whereIn('motivo_contato', [1,2])->whereBetween('created_at', ['2021-01-01 00:00:00', '2021-01-31 00:00:00'])->get();
```
nesse caso, o where() busca todos os registros que não contenham o nome "João" no campo nome, o wherein() busca todos os registros que contenham os valores 1 ou 2 no campo motivo_contato e o wherebetween() busca todos os registros que contenham os valores entre 2021-01-01 00:00:00 e 2021-01-31 00:00:00 no campo created_at.

### Selecionando registros com "Or"
para selecionar registros com "or", basta encadear o metodo orwhere(), lembrando que no operador or somente uma das condições precisa ser verdadeira para que o registro seja retornado, ex:
```
use \App\Cliente;
$clientes = Cliente::where('nome','<>','João')->orwhere('motivo_contato', 1)->get();
```
nesse caso, o where() busca todos os registros que não contenham o nome "João" no campo nome e o orwhere() busca todos os registros que contenham o valor 1 no campo motivo_contato.

### Selecionando registros com "WhereNotNull"
para selecionar registros com "wherenotnull", basta encadear o metodo wherenotnull(), ex:
```
use \App\Cliente;
$clientes = Cliente::where('nome','<>','João')->wherenotnull('motivo_contato')->get();
```
nesse caso, o where() busca todos os registros que não contenham o nome "João" no campo nome e o wherenotnull() busca todos os registros que não contenham o valor null no campo motivo_contato.

### Selecionando registros com "WhereNull"
para selecionar registros com "wherenull", basta encadear o metodo wherenull(), ex:
```
use \App\Cliente;]
$clientes = Cliente::whereNotNull('updated_at')->get();
```
nesse caso, o wherenotnull() busca todos os registros que não contenham o valor null no campo updated_at.

### Selecionando registros com "WhereDate"
para selecionar registros com "wheredate", basta .. ex:
```
use \App\Cliente;
$clientes = Cliente::whereDate('created_at', '2021-01-01')->get();
```
nesse caso, o wheredate() busca todos os registros que contenham a data 2021-01-01 no campo created_at.

Selecionando registros com "WhereMonth"  basta .. ex:
```
use \App\Cliente;
$clientes = Cliente::whereMonth('created_at', '01')->get();
```
nesse caso, o wheremonth() busca todos os registros que contenham o mês 01 no campo created_at.

Selecionando registros com "WhereDay"  basta .. ex:
```
use \App\Cliente;
$clientes = Cliente::whereDay('created_at', '01')->get();
```
nesse caso, o whereday() busca todos os registros que contenham o dia 01 no campo created_at.

Selecionando registros com "WhereYear"  basta .. ex:
```
use \App\Cliente;
$clientes = Cliente::whereYear('created_at', '2021')->get();
```
nesse caso, o whereyear() busca todos os registros que contenham o ano 2021 no campo created_at.

### Selecionando registros com "WhereTime"
para selecionar registros com "wheretime", basta .. ex:
```
use \App\Cliente;
$clientes = Cliente::whereTime('created_at', '08:00:00')->get();
```
nesse caso, o wheretime() busca todos os registros que contenham o horário 08:00:00 no campo created_at.

### Selecionando registros com "WhereColumn"
para selecionar registros com "wherecolumn", basta .. ex:
```
use \App\Cliente;
$clientes = Cliente::whereColumn('nome', 'telefone')->get();
```
nesse caso, o wherecolumn() busca todos os registros que contenham o valores iguais no campo nome e no campo telefone.

## Selecionando registros aplicando precedência logica em operaçoes logicas.
para selecionar registros aplicando precedência logica em operaçoes logicas, basta .. ex:
```
use \App\Cliente;
$clientes = Cliente::where('nome','<>','João')->orwhere(function($query){
    $query->wherein('motivo_contato', [1,2]);
})->get();
```
### Ordenando registros
para ordenar registros, basta encadear o metodo orderby(), ex:
```
use \App\Cliente;
$clientes = Cliente::orderby('nome')->get();
```
nesse caso, o orderby() ordena os registros em ordem crescente pelo campo nome.

### Ordenando registros em ordem decrescente
para ordenar registros em ordem decrescente, basta encadear o metodo orderby() e o metodo desc(), ex:
```
use \App\Cliente;
$clientes = Cliente::all()->orderby('nome')->desc();
```
nesse caso, o orderby() ordena os registros em ordem decrescente pelo campo nome.

# Introdução as Collections
Collections são objetos que representam uma coleção de dados, ou seja, são objetos que representam um conjunto de dados.

### first()
o metodo first() retorna o primeiro registro da coleção
```
use \App\Cliente;
$clientes = Cliente::where('nome','<>','João')->orwhere(function($query){
    $query->wherein('motivo_contato', [1,2]);
})->get()->first();
```
nesse caso, o first() retorna o primeiro registro da coleção.

### last()
o metodo last() retorna o último registro da coleção
```
use \App\Cliente;
$clientes = Cliente::where('nome','<>','João')->orwhere(function($query){
    $query->wherein('motivo_contato', [1,2]);
})->get()->last();
```
nesse caso, o last() retorna o último registro da coleção.

### reverse()
o metodo reverse() retorna a coleção em ordem reversa
```
use \App\Cliente;
$clientes = Cliente::where('nome','<>','João')->orwhere(function($query){
    $query->wherein('motivo_contato', [1,2]);
})->get()->reverse();
```
nesse caso, o reverse() retorna a coleção em ordem reversa.

## ToArray e ToJson
### toArray()
o metodo toArray() retorna a coleção em formato de array
```
use \App\Cliente;
$clientes = Cliente::all()->toArray();
```
nesse caso, o toArray() retorna a coleção em formato de array.

### toJson()
o metodo toJson() retorna a coleção em formato de json
```
use \App\Cliente;
$clientes = Cliente::all()->toJson();
```
nesse caso, o toJson() retorna a coleção em formato de json.

### pluck
o metodo pluck() retorna uma coleção com os valores de uma coluna específica
```
use \App\Cliente;
$clientes = Cliente::all()->pluck('email');
```
nesse caso, o pluck() retorna uma coleção com os valores da coluna email.

### Eloquent - metodos nativos dos objetos Collection
por ser uma lista gigantesca, não será possível abordar todos os metodos nativos dos objetos Collection, mas, é possível acessar a documentação oficial do laravel para saber mais sobre os metodos nativos dos objetos Collection.
<a href='https://laravel.com/docs/10.x/collections'>aqui</a>

---
# atualizando registros
para atualizar registros, basta instanciar a classe e atribuir os valores aos atributos
```
$cliente = \App\Cliente::find(1);
$cliente->nome = 'João';
$cliente->telefone = '11 99999-9999';
Print_r($cliente->getAttributes());
// serve para mostrar os atributos do objeto instanciado
```
em seguida, basta executar o método save()
```
$cliente->save();
```
## Fill()
utilizando o declarado no fillable do model, podemos usar o metodo fill() para atribuir os valores aos atributos
```
$cliente = \App\Cliente::find(1);
$cliente->fill(['nome' => 'João', 'telefone' => '11 99999-9999']);
$cliente->save();
```
## Where->update()
podemos usar o metodo where() para buscar os registros que queremos atualizar e em seguida usar o metodo update() para atualizar os registros
```
\App\Cliente::wherein('id', [1,2])->update(['nome' => 'Fornecedor Teste', 'site' => 'fornecedor.com.br']);
```
nesse caso, o where() busca todos os registros que contenham os valores 1 ou 2 no campo id e o update() atualiza os registros com os valores 'Fornecedor Teste' no campo nome e 'fornecedor.com.br' no campo site.

## Delete e Destroy (Deletando Registros)

```
use \App\Cliente;
$cliente = Cliente::find(1);
$cliente->delete();
```
se a resposta for true, o registro foi deletado com sucesso.
```
use \App\Cliente;
$cliente = Cliente::destroy(1);
```
se a resposta for true, o registro foi deletado com sucesso.

## Soft Delete
o soft delete é um recurso que permite que os registros não sejam deletados do banco de dados, mas, que sejam marcados como deletados, ou seja, o registro não é deletado, mas, não é mais exibido nas consultas.

para usar o soft delete, basta adicionar a trait SoftDeletes no model
```
use Illuminate\Database\Eloquent\SoftDeletes;

class Cliente extends Model
{
    use SoftDeletes;
}
```
e em migrations:
```
Public function up()
{
    Schema::create('clientes', function (Blueprint $table) {
        $table->id();
        $table->string('nome', 100);
        $table->string('telefone', 20);
        $table->string('email', 100);
        $table->timestamps();
        $table->softDeletes();
    });
}

public function down()
{
    Schema::dropSoftDeletes('clientes');
}
```
Excutando o comando artisan migrate, é criado um campo chamado deleted_at na tabela clientes.

assim, para excluir um registro, do banco de dados de verdade e não apenas marcar como deletado, basta usar o metodo forceDelete()
```
use \App\Cliente;
$cliente = Cliente::find(1);
$cliente->forceDelete();
```

### Restaurando registros
para restaurar registros, basta usar o metodo restore()
```
use \App\Cliente;
$cliente = Cliente::withTrashed()->find(1);
$cliente->restore();
```
nesse caso, o withTrashed() busca o registro mesmo que ele esteja marcado como deletado e o restore() restaura o registro.

para selecionar somente os registros removidos, basta usar o metodo onlyTrashed()
```
use \App\Cliente;
$cliente = Cliente::onlyTrashed()->get();
```
nesse caso, o onlyTrashed() busca somente os registros que estão marcados como deletados.

## Seeders
Seeders são classes que servem para popular o banco de dados com dados fictícios, ou seja, são classes que servem para popular o banco de dados com dados de teste.

para criar um seeder, basta executar o comando artisan make:seeder NomeSeeder
```
php artisan make:seeder ClientesSeeder
```
o seeder é criado na pasta database/seeds

temos que definir o que será inserido no banco de dados no metodo run()
```
use App\Cliente;
public function run()
{
    //instanciando o Objeto
    $cliente = new Cliente();
    $cliente->nome = 'João';
    $cliente->telefone = '11 99999-9999';
    $cliente->email = 'jao@clientes.com';
    $cliente->save();

    //usando o metodo create(atenção ao fillable no model)
    Cliente::create([
        'nome' => 'Maria',
        'telefone' => '11 99199-9999',
        'email' => 'dascolves@clientes.com';
    ]);

    //usando o metodo insert
    DB::table('clientes')->insert([
        'nome' => 'Marya',
        'telefone' => '11 99929-9999',
        'email' => 'dascanela@cliente.com
}
```
lembrando também que temos que definir o seeder no arquivo database/seeds/DatabaseSeeder.php
```
public function run()
{
    $this->call(ClientesSeeder::class);
}
```
para executar o seeder, basta executar o comando artisan db:seed
```
php artisan db:seed
```

por padrão, o comando db:seed executa todos os seeders, mas, se eu quiser executar um seeder específico, basta executar o comando artisan db:seed --class=NomeSeeder
```
php artisan db:seed --class=ClientesSeeder
```

## Factories
as factories permitem, através de um seeder, semear em massa uma tabela do banco de dados.

as factories do framework laravel utilizam o faker, que é um gerador de dados fictícios, ou seja, é um gerador de dados de teste.

as factories são criadas na pasta database/factories

para criar uma factory, basta executar o comando artisan make:factory NomeFactory
```
php artisan make:factory ClienteFactory --model=Cliente
```
lembrando de sempre terminar o nome da factory com Factory, pois, esse padrão facilita identificar as factories.

a factory é criada na pasta database/factories

temos que definir o que será inserido no banco de dados no metodo definition()
```
use App\Cliente;
use Faker\Generator as Faker;

$factory->define(Cliente::class, function (Faker $faker) {
    return [
        'nome' => $this->faker->name,
        'telefone' => $this->faker->phoneNumber,
        'email' => $this->faker->unique()->safeEmail,
    ];
});
```
essa ferramenta possuí uma grande variedade de dados fictícios, para saber mais, basta acessar a documentação oficial do faker<a href='https://github.com/fzaninotto/Faker'> aqui</a>.
 claro que ainda resta definir o seeder no arquivo ClienteSeeder.php
```
public function run()
{
    \App\Cliente::factory()->count(100)->create();
}
```
para executar o seeder, basta executar o comando artisan db:seed
```
php artisan db:seed
```
pronto seu banco está bem populado e pronto para desenvolver testes com mais precisão

--fim da seção 8--
