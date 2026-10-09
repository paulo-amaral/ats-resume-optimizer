# Palavras-chave e adaptação à descrição da vaga

Adaptar é **selecionar e espelhar**, não inventar. Parta do Perfil Mestre
(`05-perfil-mestre.md`) e use a linguagem da vaga com honestidade.

> Tradução de `../03-keywords-and-tailoring.md`. Em caso de divergência, vale o original em inglês.

## Passo 1: analisar a descrição da vaga

Extraia e classifique as palavras-chave:
- **Obrigatórias**: competências técnicas, ferramentas, tecnologias, certificações,
  metodologias e o **título exato do cargo**. É isso que parsers e buscas booleanas
  capturam.
- **Desejáveis / diferenciais**: competências secundárias e qualificações extras.
- **Contextuais**: termos de domínio, setor, escala e formato de equipe que mostram
  aderência.

Observe **frequência e posição**: uma competência citada 5× (e no título) pesa mais do
que uma citada uma vez; reorganize o conteúdo para começar pelas mais enfatizadas.
Expressões de competências comportamentais ("excelente comunicação") são quase
invisíveis para parsers; demonstre-as com conquistas, não as liste.

## Passo 2: análise de lacunas

Compare as palavras-chave classificadas com o Perfil Mestre:
- **Tem e mostra**: já aparece num bullet real. Ótimo.
- **Tem, mas não mostra**: a pessoa tem a qualificação, mas ela não aparece. Inclua
  (competências + um bullet real).
- **Não tem**: deixe de fora. **Não** invente. Se faltarem muitos requisitos
  obrigatórios, veja o filtro "candidatar ou não" abaixo.

## Passo 3: espelhar a linguagem (correspondência exata)

- Use a **redação exata** da vaga para competências técnicas. ATS de correspondência
  exata (Taleo, Oracle, iCIMS/Brassring e, em grande parte, Greenhouse) não resolvem
  sinônimos nem radicais: "React.js" ≠ "React" para um comparador simples, então use a
  forma da vaga.
- **Siglas nos dois sentidos:** "Search Engine Optimization (SEO)" na primeira
  ocorrência, depois a sigla. ATS de correspondência exata não ligam os dois sozinhos.
- Coloque cada termo-chave em **≥2 lugares**: na seção de Competências **e** num bullet
  real de experiência, para que pareça demonstrado, não apenas listado.

## Passo 4: NÃO encher nem esconder

- **Densidade de palavras-chave é mito e excesso piora o resultado.** Repetir "gestão
  de projetos" 12× classifica *pior* do que uma redação natural e variada; recrutadores
  (~76%) querem uso natural. Use cada termo-chave ~1–3×.
- **Nunca use texto oculto/branco.** Camadas de IA de 2025/2026 detectam isso
  ativamente e marcam a candidatura como manipuladora. Risco alto, ganho negativo.
- Camadas modernas de IA/semânticas entendem contexto ("construí pipelines de ETL para
  dados financeiros" combina com "Engenheiro de Dados em banco"), então **escreva com
  clareza e fatos**: isso atende tanto o filtro exato quanto a camada de IA.

## Passo 5: estimativa de cobertura (rotule com honestidade)

Informe uma **estimativa de cobertura de palavras-chave**, nunca uma falsa "nota ATS
100/100". Use:

```
ats-resume coverage resume.json --jd vaga.txt
```

O comando informa o % de palavras-chave obrigatórias e desejáveis presentes no
currículo e lista as ausentes. Ele entende vagas em português ("Requisitos",
"Diferenciais", "Desejável") e compara sem diferenciar acentos. Interpretação da nota
ponderada:

```
Nota = 0,40 * cobertura_obrigatorias
     + 0,20 * cobertura_desejaveis
     + 0,20 * taxa_de_quantificacao      # % de bullets com métrica
     + 0,10 * completude_de_secoes       # seções padrão presentes / 5
     + 0,10 * distribuicao_de_termos     # seções com termos da vaga / seções com conteúdo
```

Faixas (heurística; apresente como orientação, não como verdade absoluta): **85%+
forte · 70–84% moderada · <70% fraca.** Sempre diga que isso estima a aderência de
palavras-chave, não a nota interna de um ATS específico.

## Filtro "candidatar ou não"

Antes de investir na adaptação, estime a aderência e decida:

```
Geral = cobertura_obrigatorias * 0,7 + cobertura_desejaveis * 0,3
```

| Faixa | Leitura | Ação |
| --- | --- | --- |
| 90–100% | Provavelmente acima do nível (percepção de risco de saída) | Candidate-se; posicione-se para o nível certo |
| 75–89% | Aderência forte | Candidate-se já, com currículo adaptado |
| 60–74% | Boa aderência com lacunas | Candidate-se com uma carta forte que trate as lacunas |
| 50–59% | Desafio | Só se houver interesse real; destaque conquistas transferíveis |
| <50% | Baixa aderência | Pule, a menos que seja a vaga dos sonhos; use o tempo em outra |

Procure também **sinais de alerta** na vaga (lista irreal de requisitos, escopo vago,
sinais de alta rotatividade) e mostre-os para que a pessoa decida sabendo dos riscos.

## Perguntas eliminatórias (o mecanismo real de rejeição)

ATS raramente rejeitam pelo currículo, mas as **perguntas eliminatórias** do formulário
rejeitam. São os filtros "Você tem X anos de Y?", "Você tem autorização para trabalhar
em...?", "Qual sua pretensão salarial?". Oriente a pessoa a:
- **Responder com honestidade, mas com estratégia.** Um requisito rígido que ela não
  cumpre (autorização de trabalho, registro profissional obrigatório) é um filtro real;
  não desperdice a candidatura. Numa pergunta flexível de "anos de experiência",
  responda a verdade; se faltar um ano mas a qualificação for clara, candidate-se mesmo
  assim (muitas são filtros, não muros).
- **Pretensão salarial:** quando obrigatório, informe uma faixa pesquisada, não um
  valor único.
- **Nunca mentir numa pergunta eliminatória**: isso aparece na triagem e queima a
  relação.
- Tratar um paredão de perguntas invasivas + baixa aderência como sinal para investir o
  esforço em outra vaga (veja o filtro acima).

## Várias vagas de uma vez

Com um Perfil Mestre, adaptar para N vagas = N seleções de uma única base verdadeira.
Mantenha uma nota curta por variante dizendo quais funções/bullets foram destacados ou
ocultados e por quê (sistema de visibilidade em `05-perfil-mestre.md`), para que as
variantes fiquem consistentes e os fatos nunca precisem ser refeitos.
