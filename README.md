# CTF Beginner — Nimbus Logistics

Um CTF **web, nível iniciante**, no estilo TryHackMe. Você recebe acesso ao
portal interno de uma empresa fictícia de logística (a *Nimbus Logistics*) e seu
objetivo é encontrar as falhas de segurança escondidas nele e capturar as
**flags** (no formato `FLAG{...}`).

> Nenhum conhecimento prévio de segurança é necessário. Só curiosidade, um
> navegador e vontade de cutucar as coisas. 🕵️

## Cenário

A Nimbus está migrando seu portal interno para a versão 2.3 e, no meio da
correria, algumas coisas ficaram... mal feitas. Sua missão é agir como um
pentester e mostrar pra eles tudo que está errado — antes que alguém mal
intencionado faça isso.

## Regras do jogo

- Tudo que você precisa está acessível a partir do site. Nada de força bruta
  pesada nem ferramentas de negação de serviço — o desafio é de **raciocínio**,
  não de barulho.
- Explore como um curioso: leia o código-fonte das páginas, preste atenção nos
  detalhes, teste o que parece "quebrável".
- Cada flag encontrada vale um ponto. São **6 flags** no total.

## Ferramentas que ajudam (todas gratuitas)

- O próprio **navegador** (menu *Ver código-fonte* e as *DevTools* — F12).
- Um bloco de notas pra ir anotando o que achar.
- Opcional: uma extensão pra editar cookies, ou o `curl` no terminal.

## Como capturar as flags

Anote cada flag que encontrar em um arquivo `flags.md` (crie o seu, no estilo
tabela abaixo) e descreva **como** conseguiu. O "como" é o que mais importa —
é ali que você aprende.

| # | Categoria (dica leve)        | Flag encontrada | Como consegui |
|---|------------------------------|-----------------|---------------|
| 1 | Reconhecimento               |                 |               |
| 2 | Arquivos esquecidos          |                 |               |
| 3 | Autenticação                 |                 |               |
| 4 | Controle de acesso (dados)   |                 |               |
| 5 | Controle de acesso (área)    |                 |               |
| 6 | Informação exposta           |                 |               |

## Subir o ambiente

Veja [`setup.md`](./setup.md) para as especificações da VM na Azure e o passo a
passo. Em resumo: cria uma VM Ubuntu, roda `setup.sh`, e manda o link pro time.

---

*Ambiente educacional, intencionalmente vulnerável. Não hospede nada real nesta
VM e não a use em produção.*
