# Leitura por ATS e formatação segura para ATS

Como os sistemas de recrutamento (ATS) leem um currículo, o que os faz falhar e as
regras de formatação que funcionam em todos eles. Otimize para **leitura limpa pelo
sistema + leitura rápida por pessoas**, não para um robô mítico de rejeição automática
(veja `07-mitos-e-verdades.md`).

> Tradução de `../01-ats-and-formatting.md`. Em caso de divergência, vale o original em inglês.

## Como a leitura (parsing) funciona de fato

O currículo passa por duas etapas; **a leitura é o portão antes de tudo**:

1. **Entrada + leitura**: o arquivo vira texto simples, o layout é descartado e um
   parser distribui o texto em campos: nome, contato, histórico profissional (com
   datas), formação, competências. O que o parser lê errado ou descarta fica invisível
   para todas as etapas seguintes, inclusive a triagem por IA.
2. **Busca / ranking / IA**: recrutadores fazem buscas booleanas por palavras-chave na
   base processada (resultados ordenados pela frequência dos termos buscados); cada vez
   mais, uma camada de LLM resume e pontua o texto extraído.

Consequência de projeto: se o conteúdo não sai limpo da etapa 1, o resto não importa.

## O que quebra a leitura (em ordem aproximada de gravidade)

1. **Várias colunas / layout em duas colunas**: a falha nº 1 (~34% dos erros de
   leitura). Parsers leem da esquerda para a direita, de cima para baixo, então duas
   colunas se misturam e viram texto sem sentido. Currículos de uma coluna são lidos
   ~96% completos contra ~78% dos de duas colunas ou exportados de ferramentas de
   design. **Use uma coluna.**
2. **Cabeçalho e rodapé**: muitos parsers (principalmente o Workday) os descartam.
   Contato colocado ali pode sumir. **Não coloque nada essencial no cabeçalho/rodapé.**
3. **Tabelas** (inclusive tabelas invisíveis de layout): embaralham a cronologia e o
   mapeamento de campos; é a principal falha do Taleo. Uma tabela bonita de
   competências vira uma sequência truncada. **Sem tabelas.**
4. **Caixas de texto, gráficos, ícones, logotipos, fotos, barras de nível**: não são
   extraídos como texto; o que está dentro desaparece. **Nada disso.**
5. **Marcadores fora do padrão** (→ ✓ ➤ ✦): viram lixo na tokenização e fragmentam os
   bullets. **Use marcadores redondos ou quadrados padrão.**
6. **Fontes decorativas ou incomuns**: erros de mapeamento de caracteres. **Só fontes
   comuns (web-safe).**
7. **PDF de imagem / digitalizado**: o verdadeiro problema de formato. O texto precisa
   ser selecionável.

## Comportamento por plataforma

| Plataforma | Estilo | Observações |
| --- | --- | --- |
| **Workday** | O mais rígido; rótulos de seção exatos | Descarta cabeçalho/rodapé; quer o contato nas primeiras ~10–15 linhas; prefere `MM/AAAA`; pode perder competências de várias palavras |
| **Taleo** | O mais antigo, rígido; exige `MM/AAAA` | Um título lido errado desloca tudo o que vem depois; **apaga conteúdo sem avisar**; tabelas são sua falha nº 1 |
| **Greenhouse** | Parser Sovren, mais tolerante/semântico | Mais limpo com títulos convencionais em uma coluna; ainda favorece rótulos padrão |
| **Lever** | O mais tolerante | Remove barras laterais de forma agressiva (perdeu ~60% do conteúdo de várias colunas em testes); grava "Present" literalmente |
| **iCIMS** | Validação após a leitura; marca campos incertos | Lê colunas em linha reta → texto sem sentido; reconhece "Present", mas não "Ongoing/Now/Current" |
| **Ashby / SmartRecruiters** | Modernos, tolerantes | Uma coluna limpa é lida bem em todos |
| **LinkedIn** | Centrado no perfil | Recrutadores fazem busca booleana na base; seu *perfil* costuma pesar mais na visibilidade do que o arquivo enviado. Repita as palavras-chave lá também |

Para o Brasil (Gupy), veja `09-mercado-brasileiro.md`.

**Regra prática:** um arquivo de uma coluna, sem tabelas, sem cabeçalho/rodapé, com
títulos e marcadores padrão e texto selecionável funciona em todos. Projete para os mais
rígidos (Workday/Taleo) e você estará seguro em qualquer um.

## Formato: PDF ou DOCX (as fontes divergem; esta é a escolha defensável)

- **O formato do arquivo raramente é o problema; o layout é.** PDF e DOCX são lidos
  bem quando o arquivo é limpo, de uma coluna e com texto; ambos falham com colunas,
  tabelas e gráficos.
- **Padrão: PDF com texto**, exportado de um editor de texto (não digitalizado, não
  "imprimir como imagem"). Leitura confiável nos ATS modernos + aparência estável para
  quem lê.
- **Use DOCX quando:** a vaga pedir; houver um parser antigo e rígido (versões antigas
  de Taleo/Workday), pois o DOCX tem ordem de extração mais previsível; ou o portal
  preencher campos automaticamente a partir do arquivo.
- **Sempre siga uma instrução explícita de formato** da vaga.
- O teste que resolve: abra o arquivo, selecione tudo e cole num editor de texto
  simples. Se o texto sair limpo e na ordem certa, o ATS consegue ler. Tenha PDF e DOCX
  à mão. `ats-resume check arquivo.pdf` faz essa verificação.

## Títulos de seção padrão (use estes; não invente)

Reconhecidos de forma confiável pelos principais parsers (currículos em inglês):
- **Summary** (ou "Professional Summary")
- **Work Experience** (ou "Experience" / "Professional Experience", todos servem)
- **Education**
- **Skills** (ou "Technical Skills")
- **Certifications**
- Opcionais: **Projects**, **Publications**, **Awards**

Em currículos em português, use os equivalentes convencionais (convenção de mercado,
não dado medido): **Resumo Profissional**, **Experiência Profissional**, **Formação
Acadêmica**, **Competências**, **Certificações**, **Projetos**, **Idiomas**.

Evite títulos criativos ("Onde fiz a diferença"). **Não** policie demais os sinônimos
padrão: "Professional Experience" e "Technical Skills" são padrão e seguros; alguns
guias afirmam o contrário, sem razão.

## Ordem das seções (cronologia inversa, padrão dos EUA)

1. Contato (no corpo do documento, no topo)
2. Resumo (opcional, recomendado para quem tem experiência)
3. Experiência Profissional (cronologia inversa)
4. Formação
5. Competências
6. Certificações / extras

Reordene conforme o momento de carreira:
- **Recém-formado(a):** Contato → Resumo/Objetivo → Formação → Projetos/Estágios →
  Experiência → Competências (formação primeiro, é o ativo mais forte).
- **Pleno/Sênior:** Contato → Resumo → Experiência → Competências → Formação →
  Certificações (a experiência domina; a formação vai para o fim).
- **Transição de carreira:** Contato → Resumo que faz a ponte → Competências/Projetos
  relevantes → Experiência reenquadrada → Formação (destaque competências
  transferíveis).

## Datas

- Formato `Mês Ano – Mês Ano` (ex.: "January 2018 – April 2022"); parsers reconhecem
  esse intervalo. Workday/Taleo preferem a precisão `MM/AAAA`.
- Em inglês, use a palavra literal **"Present"** para a função atual (evite
  Current/Now/Ongoing). Em português, a convenção é "atual" (ex.: `mar. 2021 – atual`
  ou `03/2021 – atual`); mantenha um único formato no CV todo.
- Datas alinhadas à direita funcionam num layout de uma coluna.

## Contato

- No **corpo do documento**, no topo da página; nunca no cabeçalho/rodapé.
- Nome sozinho na primeira linha; depois telefone, e-mail profissional, cidade/estado,
  URL do LinkedIn, cada um em sua linha ou separados de forma simples (barra vertical,
  vírgula). URLs em texto, não ícones. Sem foto, idade, endereço completo ou dados
  pessoais.

## Detalhes de formatação

- **Layout:** uma coluna. Sem tabelas, caixas de texto, colunas ou gráficos.
- **Fontes:** Calibri, Cambria, Georgia, Arial, Helvetica, Times New Roman, Garamond,
  Tahoma, Verdana. Corpo 10–12 pt; títulos 14–16 pt; nome maior que tudo.
- **Margens:** 1 polegada (2,54 cm) padrão; 0,5 polegada (1,27 cm) no mínimo absoluto.
- **Marcadores:** círculos sólidos/vazados ou quadrados padrão; sem símbolos
  personalizados.
- **Pontuação:** consistente; números em algarismos (8, não oito); sem ponto final nos
  bullets (ou sempre com ponto; o importante é ser consistente).

## Tamanho (a regra de uma página está ultrapassada)

- **1 página** para menos de ~10 anos de experiência / estudantes / recém-formados.
- **2 páginas** acima de ~10 anos: pesquisas com recrutadores de 2025/2026 mostram que
  a maioria hoje aceita ou prefere 1–2 páginas.
- **3 páginas** só para CVs executivos, acadêmicos, de governo (EUA) ou da área médica.
- ATS **não** penalizam o tamanho. Como pessoas leem rápido, o material mais forte, com
  palavras-chave e números, precisa estar no **terço superior** de qualquer forma.

## Nome do arquivo

`Nome-Sobrenome-Curriculo.pdf` (hífens ou sublinhados passam entre sistemas de forma
mais previsível do que espaços). Inclua o nome completo. Siga qualquer padrão de nome
pedido pela vaga.

## Checklist de segurança para ATS (saída da Fase 3)

- [ ] Uma coluna, sem tabelas, caixas de texto ou colunas
- [ ] Nada no cabeçalho ou rodapé (contato no topo do corpo)
- [ ] Sem gráficos, ícones, logotipos, fotos ou barras de nível
- [ ] Títulos de seção padrão, cronologia inversa
- [ ] Marcadores padrão
- [ ] Fonte comum, corpo 10–12 pt / títulos 14–16 pt, margens ≥ 0,5"
- [ ] Datas como `Mês Ano – Mês Ano` + "Present"/"atual"
- [ ] Texto selecionável/copiável (não é imagem)
- [ ] Siglas escritas por extenso uma vez, com a sigla entre parênteses
- [ ] Arquivo nomeado `Nome-Sobrenome-Curriculo.pdf`, no formato pedido pelo portal
