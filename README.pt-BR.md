# ATS Resume Optimizer: verificador de currículo ATS, gerador de CV e otimizador de LinkedIn

**English:** [README.md](README.md)

Veja seu currículo do jeito que um **sistema de recrutamento (ATS)** lê, adapte o texto
a uma vaga e exporte um **PDF ou DOCX compatível com ATS**. Funciona de três formas:

1. **App no terminal (TUI):** escolha o currículo, cole a vaga e veja o resultado na hora.
2. **Linha de comando (CLI):** um comando para cada tarefa.
3. **Skill de agente de IA para Claude Code:** a IA escreve o texto com você; as ferramentas conferem formato, palavras-chave e veracidade.

Pensado para a leitura de ATS (Workday, Greenhouse, Lever, Taleo, iCIMS, Ashby; e
[orientações para Gupy](skills/resume-ats-linkedin-optimizer/references/09-brazil-market.md)),
para a leitura rápida de recrutadores e para a busca do LinkedIn. **Zero invenção:**
nunca cria empresas, cargos, datas ou números.

![App no terminal](https://raw.githubusercontent.com/paulo-amaral/ats-resume-optimizer/main/docs/tui.svg)

## Comece em 1 minuto

Instale o [uv](https://docs.astral.sh/uv/getting-started/installation/) (um instalador
que já cuida do Python). Depois:

```bash
uv tool install "ats-resume[tui]"
ats-resume tui --lang pt
```

Também funciona com `pipx install "ats-resume[tui]"` ou `pip install "ats-resume[tui]"`.
Para testar sem instalar: `uvx ats-resume check meu-cv.pdf`.

No painel da esquerda, escolha seu currículo (PDF, DOCX, TXT ou JSON). Cole a descrição
da vaga e leia as três abas: **Arquivo ATS**, **Estilo** e **Palavras-chave**.

## O que dá para fazer

| Objetivo | Comando |
| --- | --- |
| Verificar o currículo que você já tem | `ats-resume check meu-cv.pdf` |
| Comparar com uma vaga | `ats-resume check meu-cv.pdf --job vaga.txt` |
| Converter PDF/DOCX em JSON editável | `ats-resume import meu-cv.pdf` |
| Começar de um exemplo em português | `ats-resume new --lang pt` |
| Exportar PDF ou DOCX compatível com ATS | `ats-resume render resume.json -o Nome-Sobrenome-CV.pdf -t modern` |
| Exportar LaTeX (Overleaf) ou PDF via LaTeX | `ats-resume render resume.json -o cv.tex` / `-o cv.pdf --latex` |
| Provar que nada foi inventado | `ats-resume validate resume.json --source mestre.json` |
| App interativo | `ats-resume tui` |

A porcentagem é uma **estimativa** de aderência de palavras-chave. Nenhuma ferramenta
reproduz a nota interna de um ATS, e esta não finge que faz isso.

## Suporte a português

- Títulos de seção em português (Experiência Profissional, Formação Acadêmica...) e papel A4.
- Comparação de palavras-chave que entende acentos ("gestão" = "gestao") e marcadores de vaga em português ("Requisitos", "Diferenciais", "Desejável").
- Detecção de clichês: "responsável por", "proativo", "focado em resultados", "alavanquei"...
- Todas as referências da skill traduzidas em [`references/pt-BR/`](skills/resume-ats-linkedin-optimizer/references/pt-BR/).
- [Guia do mercado brasileiro](skills/resume-ats-linkedin-optimizer/references/pt-BR/09-mercado-brasileiro.md): o que não colocar no CV (Lei 9.029/1995, LGPD) e como a Gupy faz a triagem, com fontes.

## Usar com seu agente de IA

| Agente | Instalação |
| --- | --- |
| **Claude Code** | `/plugin marketplace add paulo-amaral/ats-resume-optimizer` e depois `/plugin install ats-resume-optimizer@ats-resume-optimizer` |
| **Claude Cowork** (desktop) | Em Customize, abra Plugins, escolha **Add marketplace**, informe `paulo-amaral/ats-resume-optimizer` e instale o plugin |
| **OpenAI Codex** | `git clone https://github.com/paulo-amaral/ats-resume-optimizer && mkdir -p ~/.agents/skills && cp -R ats-resume-optimizer/skills/resume-ats-linkedin-optimizer ~/.agents/skills/` |
| **Cursor, Gemini CLI e outros** | Abra este repositório no agente: o [`AGENTS.md`](AGENTS.md) diz o que fazer. Ou adicione a pasta `skills/resume-ats-linkedin-optimizer/` ao contexto. |

Depois peça, em português:

- *"Aqui está meu CV antigo (cv.pdf). Importe, verifique para ATS e melhore."*
- *"Adapte meu currículo para esta vaga: ..."*
- *"Melhore meu título e o Sobre do LinkedIn."*
- *"Escreva uma carta de apresentação para esta vaga."*

**Importar um CV anterior.** `ats-resume import cv-antigo.pdf` extrai o que é seguro
extrair automaticamente (contato, título, resumo, competências, idioma) e guarda as
outras seções como texto bruto para o agente estruturar, perguntando a você quando algo
for ambíguo. O original continua sendo a fonte da verdade: `ats-resume validate` prova
que nenhuma empresa, cargo, data ou contato foi inventado. Passo a passo: [`AGENTS.md`](AGENTS.md).

## LaTeX

`ats-resume render resume.json -o cv.tex` gera o código LaTeX para editar ou subir no
Overleaf, onde o compilador precisa estar em XeLaTeX; `-o cv.pdf --latex` compila no seu
computador com [Tectonic](https://tectonic-typesetting.github.io/), XeLaTeX ou LuaLaTeX.
A saída é ajustada para a extração de texto dos ATS: kerning desligado, porque pares como
"AW" e "Va" eram extraídos como palavras partidas ("A WS", "V arejo"). O pdfLaTeX não é
usado por esse motivo: ele não desliga o kerning, e o CI pegou a palavra "Texas" partida. Um teste compila os exemplos e falha se
qualquer palavra do original sumir do texto extraído.

## Privacidade

Tudo roda no seu computador. Nada é enviado para servidor nenhum. O `.gitignore`
já ignora `*.pdf`, `*.docx` e `resume.json` para evitar publicar seus dados por engano.

## Créditos

Baseado em [artificialguybr/resume-ats-linkedin-optimizer](https://github.com/artificialguybr/resume-ats-linkedin-optimizer),
de João Vitor Amaral (MIT).

## Licença

MIT. Veja [LICENSE](LICENSE).
