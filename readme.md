# O que ele faz?

O `susy.py` vai fazer umas mágicas e te dizer onde você fez merda no lab de mc.

# Onde eu coloco isso?

Crie uma pasta dentro da sua pasta de MC e coloque o `susy.py` dentro dessa pasta.

# Precisa de alguma estrutura específica nas pastas?

Sim! O susy.py deve ficar dentro de sua própria pasta
dentro da pasta de MC e cada lab deve ficar dentro de sua própria pasta também,
já compilados. No exemplo abaixo eu chamei a pasta do `susy.py` de "ferramentas"

```
Pasta de MC
│
├── lab00
│   ├── lab00.c
│   └── lab00
│
├── lab01
│   ├── lab01.c
│   └── lab01
.
.
.
├── lab42
│   ├── lab42.c
│   └── lab42
│
├── ferramentas
│   └── susy.py
```

É importante que os nomes estejam dessa forma que tá escrito ali em cima. O programa
não lê mentes, então escreva do jeito que funciona

# Como eu rodo os testes?
- Instale [Python versão 3.x](https://www.python.org/)(ou seja, não é a versão 2)

**OBS USUÁRIOS DE WINDOWS:** No começo da instalação de Python, não esqueça de marcar a opção que diz:
`Add Python to environment variables`!

Depois de ter instalado, abra seu terminal dentro
da pasta onde está o `susy.py` e digite os comandos a seguir:

```
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install requests
```
Isso vai criar o ambiente e configurar tudo pra você.

Agora você precisa alterar a sua turma, porque o `susy.py` não sabe qual é.

Pra isso, abra o `susy.py` em um editor de textos qualquer e vá na linha 9 e
mude a sua turma.

"Como eu acho minha turma?"

Simples. Abra o site do susy lá onde tem seus labs. A URL deve ser algo assim:
```
https://susy.ic.unicamp.br:9999/mc102mn/
```
Você vai copiar essa última parada. No caso, `mc102mn`. Só isso.


Agora, pra rodar os testes, basta fazer:
```
python susy.py <número do lab>
```
Por exemplo, pra rodar o lab 5:
```
python susy.py 5
```

Depois que você fechar esse terminal, é necessário reativar
o ambiente que você criou ali em cima. Pra fazer isso,
basta ir até a pasta do `susy.py` e rodar:
```
source venv/bin/activate
```
e rodar seus testes normalmente.
