# 🤖 AutoRoot — Gerenciador de Automações de Coleta de Relatórios

Automação em Python (Selenium + Google Drive/Sheets API) que loga em múltiplas plataformas de terceiros, extrai relatórios periódicos e centraliza tudo automaticamente no Google Drive — eliminando a coleta manual repetitiva desses dados.

---

## 📁 Estrutura do Repositório

```
📦 AutoRoot/
├── run.py                                  # Ponto de entrada da aplicação
├── src/
│   ├── app/
│   │   ├── main.py                         # Orquestra o fluxo geral (config → login → coleta → upload)
│   │   └── scheduler.py                    # Regras de agendamento (dia/hora) de cada relatório
│   ├── common/                             # Módulos compartilhados (driver, login, arquivos, Drive, logs...)
│   └── scripts/                            # Um módulo de coleta por plataforma integrada
├── resources/
│   ├── configs/                            # JSONs de configuração (não versionados)
│   ├── selectors/                          # JSONs de seletores web (não versionados)
│   └── templates/                          # Modelos de referência dos JSONs acima
└── README.md
```

---

## ⚙️ O que o projeto faz

O AutoRoot funciona como um **gerenciador central de automações**: um único executável dispara, sequencialmente, a checagem e coleta de relatórios em diversas plataformas de terceiros (sistemas de gestão, telefonia, CRM, entre outros). Para cada uma delas, o fluxo geral é:

1. **Login automatizado** na plataforma, incluindo resolução de **reCAPTCHA** (via API do 2Captcha) e **autenticação em duas etapas (2FA/TOTP)** quando exigido pelo site.
2. **Verificação do agendamento**: cada tipo de relatório tem sua própria regra de disparo (dia do mês, dia da semana e hora), definida no `scheduler.py`. Só é coletado o que "bate" com o horário da execução atual.
3. **Extração do relatório**: preenchimento de filtros de período (mês atual, mês anterior ou parcial), disparo do download e espera ativa pelo arquivo na pasta de Downloads.
4. **Tratamento do arquivo**: conversão de tabelas HTML para `.xlsx` quando necessário, e renomeação padronizada (`tipo_mes_ano.xlsx`).
5. **Upload para o Google Drive**: o relatório é enviado (criado ou atualizado) na pasta correspondente via Service Account.
6. **Log e auditoria**: toda a execução gera um log local; se algum erro ocorrer, os prints de tela do momento da falha e o log de erro são enviados a uma pasta específica no Drive — caso contrário, apenas o log padrão é arquivado.

---

## 🔄 Execução e Agendamento

O `.exe` gerado não roda continuamente: ele é disparado pelo **Agendador de Tarefas do Windows** em horários específicos ao longo do dia. A cada disparo, o `scheduler.py` avalia a data/hora atual e decide, para cada plataforma, quais relatórios devem ser coletados naquela execução — permitindo consolidar rotinas diárias, semanais e mensais em um único ponto de entrada.

---

## 🌐 Integrações

O projeto integra **6 plataformas distintas**, cada uma com seu próprio módulo de coleta, cobrindo áreas como:

- Ordens de serviço
- Gestão de veículos e boletos
- Atendimento e conjuntura operacional
- Telefonia
- Custos e pagamentos
- CRM

---

## 🔐 Configuração

As credenciais e seletores de cada plataforma **não são versionados** por segurança (`resources/configs/`, `resources/selectors/` e os JSONs sensíveis estão no `.gitignore`). O repositório disponibiliza apenas os modelos de referência em `resources/templates/`:

- `config.template.json` — URLs, credenciais e IDs de pasta do Drive por plataforma
- `selector.template.json` — seletores dos elementos web usados na automação
- `2Captcha.template.json` — chave de API e site keys para resolução de reCAPTCHA
- `credenciais.template.json` — credenciais da Service Account do Google Drive
- `log.template.json` — pastas de destino dos logs (normal e de erro)

---

## 🛠️ Tecnologias

- **Python** — linguagem principal
- **Selenium** + `webdriver-manager` — automação de navegador
- **Google Drive API** (`google-api-python-client`) — upload de relatórios e logs
- **2Captcha** (`2captcha-python`) — resolução automática de reCAPTCHA
- **pyotp** — geração de códigos 2FA (TOTP)
- **pandas** + `openpyxl` + `BeautifulSoup` — tratamento e conversão de relatórios (HTML → Excel)
- **PyInstaller** — empacotamento em executável

---

## 📌 Observações Técnicas

- Login com múltiplas tentativas (retry) nas plataformas que exigem 2FA, evitando falhas por instabilidade momentânea.
- Conversão automática de relatórios exportados em formato HTML (`.xls`) para `.xlsx` real, compatível com o upload ao Drive.
- Em caso de erro em qualquer etapa, a automação captura screenshot do estado da tela e segue para a próxima coleta, sem interromper o restante do fluxo.
- Upload de relatórios é feito com lógica de *upsert*: se o arquivo já existe na pasta de destino, ele é atualizado; caso contrário, é criado.

---

## 📦 Gerando o Executável

```bash
pyinstaller --onefile --add-data "resources;resources" run.py
```

---

## ⚖️ Licença

Projeto de uso interno/privado. Direitos reservados; não destinado a distribuição ou reuso externo.
