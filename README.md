# Indian Flight Delay Analytics

Aplicação Streamlit criada para explorar atrasos de voos na Índia. O projeto contém um laboratório de distribuição e correlação e um painel executivo para gestores de operações aéreas.

## Aplicação publicada

> **Link do app:** [https://avdatt.streamlit.app/](https://avdatt.streamlit.app/)

## Dashboards

- **Dashboard 1 — Laboratório:** seletor de variável quantitativa, filtro de intervalo, histograma com média e mediana e mapa de calor das correlações de Pearson.
- **Dashboard 2 — Operações:** cinco KPIs próprios e três análises visuais sobre companhias aéreas, horários de partida e condições climáticas.

O público-alvo do segundo painel são **gestores de operações de companhias aéreas**, que precisam monitorar pontualidade, severidade dos atrasos e fatores de risco para priorizar ações.

## Estrutura

```text
avd/
├── app.py
├── README.md
├── requirements.txt
├── dataset_voos/
│   └── india_flight_delay_model_input.csv
├── notebooks/
│   └── EDA_Indian_Flight_Delay.ipynb
├── entregas/
│   ├── rascunho_dashboard1.png
│   └── rascunho_dashboard2.png
└── prompts/
    └── historico_prompts.txt
```

## Como executar localmente

No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

No PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Dados e privacidade

O dataset possui 150.000 registros de voos e 23 atributos operacionais e climáticos. Não há nomes, documentos, contatos ou dados pessoais de passageiros. O aplicativo exibe somente resultados agregados.

## Checklist antes da entrega

- [ ] Abrir o link publicado em uma janela anônima.
- [ ] Testar o seletor de variável, o slider e os filtros de companhia e clima.
- [ ] Confirmar o carregamento das duas abas.
- [ ] Confirmar que não há dados pessoais ou segredos no repositório.
- [x] Substituir o campo acima pelo link real do Streamlit.
- [ ] Conferir os dois rascunhos em `entregas/`.
