# Brazilian market (PT-BR CVs)

Load this when the user applies to jobs in Brazil or writes the CV in Portuguese.
Everything in references 01–08 still applies; this file only covers what differs.
Each item is marked **[law]**, **[source]** (documented by a vendor) or
**[recommendation]** (practice derived from the first two; not a legal rule).

## 1. Personal data: what to leave out

- **[law]** Lei nº 9.029/1995, Art. 1º, bans "qualquer prática discriminatória e
  limitativa para efeito de acesso à relação de trabalho [...] por motivo de sexo,
  origem, raça, cor, estado civil, situação familiar, deficiência, reabilitação
  profissional, idade, entre outros" (wording given by Lei nº 13.146/2015).
- **[law]** LGPD (Lei nº 13.709/2018), Art. 6º, III, principle of *necessidade*:
  processing limited "ao mínimo necessário para a realização de suas finalidades".
  Art. 5º, II, defines *dado pessoal sensível* (racial or ethnic origin, religion,
  political opinion, union membership, health, sex life, genetic or biometric data).
- **[recommendation]** Because employers cannot use those factors and should collect
  only what is necessary, do not put them on the CV. Leave out: **estado civil, filhos,
  data de nascimento/idade, foto, CPF, RG, CNH number, endereço completo**, religion,
  health information. City + state (e.g., "São Paulo, SP") is enough for location.
  Candidates can supply documents later, during hiring, when the company asks.
- **[recommendation]** Exception: if the user wants to apply to roles reserved for
  pessoas com deficiência (PcD), say so only where the posting asks for it.

## 2. Gupy and other ATS used in Brazil

- **[source]** Gupy describes its AI screening as follows: "o sistema compara seu
  perfil com o que a vaga pede, buscando afinidade em experiências, formação e
  competências", and its agents "organizam uma lista para o time recrutador,
  priorizando quem parece mais alinhado". It also states the agents are designed to
  ignore sensitive information. Source: <https://gupy.io/inteligencia-artificial>.
- **[recommendation]** Practical consequence: on Gupy-style portals, fill in **every
  form field** (experiências, formação, competências) and do not rely only on the
  uploaded PDF. Mirror the exact wording of the posting in skills and bullets, as in
  `03-keywords-and-tailoring.md`. Answer knockout questions truthfully.
- The core rules in `01-ats-and-formatting.md` (single column, text-based PDF,
  standard headings) apply unchanged.

## 3. Format conventions in PT-BR **[recommendation]**

| Item | Use |
|---|---|
| Paper | A4 (`"lang": "pt"` sets it automatically) |
| Headings | Resumo Profissional, Experiência Profissional, Formação Acadêmica, Competências, Certificações, Idiomas |
| Dates | `mar. 2021 – atual` or `03/2021 – atual`; keep one format across the CV |
| Degree | "Bacharelado em Ciência da Computação", "MBA em Gestão de Projetos (em andamento)" |
| Languages | Name + level: "Inglês (avançado)", "Espanhol (intermediário)"; add a certificate (TOEFL, IELTS, DELE) if real |
| Length | 1 page up to ~5 years of experience; 2 pages above that |
| Verbs | First person, past tense, no subject: "Reduzi", "Implantei", "Liderei" (see `assets/pt-BR/action-verbs.md`) |

## 4. Writing style

- Avoid the generic PT-BR clichés in `assets/pt-BR/ai-slop-blacklist.md`
  ("proativo", "focado em resultados", "responsável por"). `ats-resume check` flags them.
- Numbers use the Brazilian format: `R$ 2,1 milhões`, `12 mil`, `40%`.
- Keep English tool and technology names as written in the posting (e.g., "Kubernetes",
  "Power BI"); do not translate them.

## Sources

- Brasil. Lei nº 9.029, de 13 de abril de 1995. <https://www.planalto.gov.br/ccivil_03/leis/l9029.htm>
- Brasil. Lei nº 13.709, de 14 de agosto de 2018 (LGPD). <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm>
- Gupy. Inteligência artificial. <https://gupy.io/inteligencia-artificial>
