# Pontuação e avaliação

A maioria das ferramentas de currículo *afirma* que gera ótimos currículos; quase
nenhuma *mede* isso. Esta skill avalia cada resultado de três formas: invariantes de
veracidade (bloqueios obrigatórios), uma nota rotulada de cobertura/qualidade e o teste
de leitura rápida humana.

> Tradução de `../06-scoring-and-evaluation.md`. Em caso de divergência, vale o original em inglês.

## 1. Invariantes de veracidade (bloqueios; todas precisam passar)

São verificações baratas e determinísticas. Rode `ats-resume validate resume.json
--source perfil-mestre.json`. Qualquer falha bloqueia o resultado:

- **Nenhuma seção removida em silêncio.** Toda seção preenchida na fonte aparece (ou
  sua remoção foi explícita).
- **Nenhum empregador inventado.** Toda empresa do resultado aparece na fonte.
- **Nenhuma data/cargo inventado.** Cargo e datas de cada função remetem à fonte.
- **Identidade intacta.** Nome, contato e dados pessoais iguais aos da fonte.
- **Esquema válido.** O resultado valida contra `assets/resume.schema.json`.
- **Métricas justificadas.** Os números do resultado existem na fonte ou estão marcados
  como estimativas confirmadas pela pessoa (com ressalva "~/aprox.").

Se uma verificação falhar, pare e reconcilie com a pessoa; nunca "corrija" inventando.

## 2. Nota de cobertura e qualidade (estimativa rotulada, não falsa nota de ATS)

Nunca apresente uma "nota ATS 100/100" precisa; nenhuma ferramenta reproduz de fato um
ATS específico. Informe isto como *estimativa* explícita de aderência de palavras-chave
+ qualidade:

```
Nota = 0,40 * cobertura_obrigatorias       # termos obrigatórios da vaga presentes
     + 0,20 * cobertura_desejaveis         # termos desejáveis da vaga presentes
     + 0,20 * taxa_de_quantificacao        # % de bullets com métrica
     + 0,10 * completude_de_secoes         # seções padrão presentes / 5
     + 0,10 * distribuicao_de_termos       # seções com termos da vaga / seções com conteúdo
```

`ats-resume coverage resume.json --jd vaga.txt` calcula a nota. Faixas (orientação):
**85%+ forte · 70–84% moderada · <70% fraca.** Sempre diga o que ela mede (aderência
de palavras-chave + quantificação) e o que não mede (o veredito interno de um ATS real).

## 3. Revisão de linguagem genérica

Rode `ats-resume deslop resume.json` (ou `ats-resume check arquivo.pdf`) para sinalizar
marcas de texto de IA e enchimento (jargões, verbos inflados, travessões como muleta,
"responsável por"), em inglês e em português. Veja `assets/pt-BR/ai-slop-blacklist.md`.
Todo rascunho passa por essa revisão; é a diferença entre um currículo que soa humano e
um que soa gerado.

## 4. Teste de leitura rápida (7 segundos)

Simule a leitura do recrutador:
- Em ~7 segundos dá para achar **nome, cargo + empresa atuais e a melhor conquista**?
- O material mais forte, quantificado e com palavras-chave está no **terço superior**?
- Todo bullet começa pelo impacto, com um verbo forte e simples, e cabe bem numa linha?
- Pontos de atenção (lacunas, muitas trocas) estão explicados, não escondidos?

Se a leitura rápida falhar, o currículo perde mesmo com leitura perfeita pelo sistema.
Corrija a ordem e o conteúdo do terço superior e rode de novo.

## Resumo da avaliação para a pessoa

Informe, de forma breve e honesta:
1. Invariantes de veracidade: passou/falhou (todas precisam passar).
2. Estimativa de cobertura: X%, com as 3–5 principais palavras-chave ausentes para as
   quais a pessoa realmente se qualifica.
3. Ajustes de linguagem genérica aplicados.
4. Resultado do teste de leitura rápida e mudanças de ordem feitas.
