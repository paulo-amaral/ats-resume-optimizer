# Otimização do perfil no LinkedIn

O LinkedIn é um **buscador de talentos**, não um ATS. O recrutador faz uma busca e cada
perfil recebe uma pontuação em relação a ela; então otimize para o ranking da busca de
recrutadores *e* para a leitura humana no feed. Traga para cá a espinha de
palavras-chave do currículo e adapte ao peso dos campos e ao tom de conversa do
LinkedIn.

> Tradução de `../04-linkedin.md`. Em caso de divergência, vale o original em inglês.

> Sobre os números: o LinkedIn não publica os pesos exatos do algoritmo. Os
> multiplicadores abaixo (5x, 40x etc.) são números bem corroborados por consultorias e
> coaches, que repetem estatísticas antigas do próprio blog de talentos do LinkedIn;
> indicam direção, não são constantes oficiais. Os limites de caracteres e a mecânica
> de completude são relatados de forma consistente.

## Como o ranking funciona

- **Primeiro correspondência de texto, depois peso de relevância.** O algoritmo não
  deduz experiência: se a palavra-chave não está literalmente no perfil, você fica
  invisível para ela. Depois os perfis são ordenados por posição/densidade das
  palavras-chave, completude, recomendações de competências e atividade recente.
- **Dois campos de busca separados para recrutadores:**
  - **Campo de cargo**: busca só **títulos de cargos** atuais/anteriores. O cargo-alvo
    precisa ser um título real ou estar no título do perfil, não perdido no texto.
  - **Campo de palavras-chave**: busca no perfil inteiro.
- **O título do perfil (headline) tem o maior peso** (~5x os outros campos). As 3
  competências fixadas no topo também pesam muito.
- **Bônus de completude ("All-Star")**: perfis All-Star aparecem muito mais; atualizar a
  posição atual é uma das maiores alavancas de visibilidade.
- **Atividade recente**: "ativo recentemente" (últimos 30 dias) ranqueia melhor;
  publicar ~1×/semana e atualizar o perfil ajuda.
- **Validações como desempate**: uma competência com 50+ validações fica acima da mesma
  competência com 5.
- **Destaques ("Spotlights") do Recruiter** aumentam a chance de resposta: Open to
  Work, "engajado com a marca empregadora", ativo recentemente, candidatos anteriores;
  com uma pontuação de IA de probabilidade de interesse por cima.

## Limites por campo (2026) + fórmulas

| Campo | Limite | Visível antes do corte |
| --- | --- | --- |
| Título (headline) | **220** | ~70 caracteres na prévia mobile/busca |
| Sobre | **2.600** | ~300 no desktop / ~200 no mobile antes de "ver mais" |
| Cargo na experiência | **100** | — |
| Descrição da experiência | **2.000** | — |
| Competência (cada) | **80** | 3 fixadas no topo |
| Competências, máximo | **100** | 5 = mínimo All-Star; **20–30 recomendadas** |
| URL personalizada | **3–100** | mantenha < ~20–26 |
| Recomendação | **3.000** | — |
| Publicação | **3.000** | ~200 antes de "ver mais" |
| Nota de conexão | **300** | — |
| Assunto / corpo de InMail | **200 / 1.900** | — |

### Título (o campo de maior alavancagem)
Nunca deixe o padrão "Cargo na Empresa". Coloque cargo + valor nos primeiros ~70
caracteres; use separadores `|` ou `•`; repita o cargo-alvo exatamente. Fórmulas:
1. **Cargo + Especialidade + Valor**: `Gerente de Produto Sênior | SaaS B2B e Fintech | Produtos usados por 2M+ pessoas`
2. **Cargo + Resultado + Prova** (melhor para atrair recrutadores): `SDR | 220 reuniões agendadas em 2026 | 4x a meta`
3. **Pilha de palavras-chave + Valor**: `Cientista de Dados | Python, ML, LLMs, MLOps | Transformando modelos em receita`

### Sobre
Primeira pessoa, tom de conversa. Estrutura:
1. **Gancho (2–3 primeiras linhas / ~300 caracteres)**: precisa merecer o clique em
   "ver mais"; comece com uma afirmação forte de valor ou "quem eu ajudo + como".
2. **Corpo (3–5 parágrafos curtos)**: história + conquistas quantificadas; distribua
   naturalmente as palavras-chave do cargo-alvo (5+ palavras-chave do cargo → mais
   buscas).
3. **Chamada para ação**: como falar com você e o que você busca.

Use quebras de linha (57%+ das visualizações são no celular). Tamanho recomendado:
~1.800–2.200 caracteres.

### Experiência (comparada aos bullets do currículo)
Pública, indexada pelo algoritmo e lida por pessoas, sem pressão de tamanho. Acrescente
contexto/história ("o porquê"). **Anexe mídia** (apresentações, estudos de caso,
portfólio, vídeos), uma vantagem nativa que o currículo não tem. Por função: um resumo
de escopo de 2–3 frases + 3–6 bullets CAR (função atual até ~8, antigas 2–3), cada um
com verbo de ação + resultado quantificado. Reescreva os bullets do currículo de forma
um pouco mais humana; não copie e cole. Repita o cargo-alvo no título da função e nos
bullets.

### Competências
Limite de 100; seja seletivo com **20–30 competências direcionadas**. Misture ~40–50%
técnicas, 20–30% funcionais, algumas do setor + poucas comportamentais. As **3
fixadas** pesam mais; ordene assim: (1) cargo/função-alvo, (2) diferencial técnico mais
forte, (3) competência do setor em alta demanda. Concentre validações nas ~10
principais; faça as avaliações de competência / selos verificados para as três fixadas
(reprovações são privadas). Analise 15–20 vagas-alvo e espelhe as competências mais
frequentes.

### Destaques / Recomendações / URL / Capa / Foto
- **Destaques:** 3–5 itens: melhores publicações, links de portfólio, estudos de caso.
  Uma vitrine curada de provas.
- **Recomendações:** 5–10 de qualidade, de gestores, colegas, liderados, clientes.
- **URL personalizada:** `linkedin.com/in/nome-sobrenome`; < ~20 caracteres; sem
  números/ano de nascimento; pode ser alterada 5× a cada 6 meses.
- **Capa:** 1584×396 (4:1); mantenha o texto na zona segura central de ~1260×300.
- **Foto:** mínimo 400×400 (800×800 é melhor), rosto ocupando 60–70% do quadro, dos
  ombros para cima, de frente; gera grandes aumentos de visualizações e mensagens.

## Estratégia de palavras-chave: LinkedIn × ATS (as diferenças)

- **Mesma espinha de palavras-chave, superfícies diferentes.** Ajuste primeiro o
  currículo para o ATS, depois leve os termos exatos para o LinkedIn.
- **A posição do campo importa mais no LinkedIn**: o cargo-alvo precisa ser um título
  real (campo de cargo ≠ campo de palavras-chave). Num ATS, a simples presença importa
  mais do que a seção.
- **Repetição + posição se somam** no LinkedIn (título ~5x + Sobre + 3 competências
  fixadas + um cargo). Um ATS verifica sobretudo presença/frequência.
- **Validações, atividade e completude entram no ranking** do LinkedIn; nada disso
  existe num ATS.
- **Leitura humana ao mesmo tempo:** evite listas cruas de palavras-chave que até
  passariam num ATS; perfis são lidos por pessoas no feed.

## Nuance do "Open to Work"

A moldura verde pública aumenta as respostas (~35–40% a mais) e recrutadores a leem
como um sinal neutro de disponibilidade, mas alguns gestores enxergam risco nela.
**"Somente recrutadores"** faz você aparecer na busca do Recruiter sem a moldura
pública.

## Diferenças currículo ↔ LinkedIn (tabela rápida)

| | Currículo | LinkedIn |
| --- | --- | --- |
| Público | Privado, ATS + um recrutador | Público, buscador + muitas pessoas |
| Voz | Enxuta, sem pronomes | Primeira pessoa, conversa |
| Tamanho | 1–2 páginas | Sem pressão; mais longo é OK |
| Palavras-chave | Correspondência exata com a vaga | Setor inteiro + cargo-alvo, repetidas com estratégia |
| Mídia | Nenhuma | Apresentações, links, vídeo são bem-vindos |
| Atualização | Por candidatura | Sempre atual |

## Erros comuns
Título padrão/fraco · título voltado ao passado · Sobre sem gancho (perdido no corte de
~300 caracteres) · palavras-chave ausentes (invisível) · abaixo de All-Star (sem foto,
<5 competências, sem descrição da função atual) · copiar e colar bullets do currículo ·
3 competências fixadas desalinhadas com o objetivo · inatividade · formatação pensada
só para desktop · jargão interno em vez de termos buscáveis · URL com números ou
genérica.

## Checklist All-Star
- [ ] Foto profissional + capa (zona segura respeitada)
- [ ] Título rico em palavras-chave (220 caracteres usados, o mais importante no início)
- [ ] Sobre com gancho + história + palavras-chave + chamada para ação
- [ ] Função atual preenchida com descrição + mídia
- [ ] ≥5 posições anteriores (de preferência todas as relevantes) com bullets CAR
- [ ] 20–30 competências; 3 fixadas alinhadas ao cargo-alvo; validações concentradas
- [ ] Formação, certificações, destaques, 5–10 recomendações
- [ ] URL personalizada; localização e setor definidos
- [ ] Open to Work configurado (público ou só recrutadores, conforme preferência)
