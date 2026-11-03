from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


st.set_page_config(
    page_title="Indian Flight Delay Analytics",
    page_icon="✈️",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "dataset_voos" / "india_flight_delay_model_input.csv"

QUANTITATIVE_COLUMNS = [
    "Scheduled_Departure_Hour",
    "Scheduled_Departure_Minute",
    "Temperature_C",
    "Humidity_pct",
    "Wind_Speed_kmh",
    "Visibility_km",
    "Rainfall_mm",
    "Cloud_Cover_pct",
    "Origin_Congestion_Index",
    "Previous_Flight_Delay_Minutes",
    "Turnaround_Risk_Index",
    "Departure_Delay",
]

LABELS = {
    "Scheduled_Departure_Hour": "Hora programada",
    "Scheduled_Departure_Minute": "Minuto programado",
    "Temperature_C": "Temperatura (°C)",
    "Humidity_pct": "Umidade (%)",
    "Wind_Speed_kmh": "Velocidade do vento (km/h)",
    "Visibility_km": "Visibilidade (km)",
    "Rainfall_mm": "Chuva (mm)",
    "Cloud_Cover_pct": "Cobertura de nuvens (%)",
    "Origin_Congestion_Index": "Índice de congestionamento",
    "Previous_Flight_Delay_Minutes": "Atraso do voo anterior (min)",
    "Turnaround_Risk_Index": "Índice de risco de turnaround",
    "Departure_Delay": "Atraso na partida (min)",
}

COLORS = {
    "navy": "#12263A",
    "blue": "#2F80ED",
    "cyan": "#56CCF2",
    "orange": "#F2994A",
    "red": "#EB5757",
    "green": "#27AE60",
    "light": "#F4F7FB",
}


@st.cache_data(show_spinner="Carregando dados de voos...")
def load_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path, parse_dates=["Flight_Date"])
    return data


def format_number(value: float, decimals: int = 1) -> str:
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def empty_state() -> None:
    st.warning("Nenhum voo atende aos filtros atuais. Ajuste o intervalo ou os filtros laterais.")
    st.stop()


st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #E8F0FA 0%, #F7F9FC 45%, #EAF3F8 100%);
            color: #12263A;
        }
        [data-testid="stHeader"] {background: rgba(232, 240, 250, 0.88);}
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #12263A 0%, #1C3A57 100%);
        }
        [data-testid="stSidebar"] * {color: #F7FBFF;}
        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-baseweb="input"] > div {
            background-color: #F7FBFF;
            color: #12263A;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] * {color: #12263A;}
        [data-testid="stMetric"] {
            background: linear-gradient(145deg, #173A5E 0%, #245A85 100%);
            border: 1px solid #3479A9;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 5px 14px rgba(18, 38, 58, 0.18);
        }
        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] *,
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] * {
            color: #FFFFFF !important;
        }
        [data-testid="stMetricValue"] {font-weight: 750;}
        h1, h2, h3 {color: #102A43 !important;}
        p, li {color: #29435C;}
        .subtitle {color: #526577; margin-top: -12px; margin-bottom: 24px;}
        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            background: #DCE9F7;
            border-radius: 12px;
            padding: 5px;
        }
        [data-testid="stTabs"] button {
            color: #173A5E !important;
            font-weight: 700;
        }
        [data-testid="stTabs"] button[aria-selected="true"] {
            background: #2F80ED;
            border-radius: 8px;
            color: #FFFFFF !important;
        }
        [data-testid="stExpander"] {
            background: #DCEBFA;
            border: 1px solid #9EC5EA;
            border-radius: 10px;
        }
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary *,
        [data-testid="stExpander"] p,
        [data-testid="stExpander"] li {
            color: #102A43 !important;
        }
        .privacy-note {
            padding: 12px 14px;
            background: #DCEBFA;
            border-left: 4px solid #2F80ED;
            border-radius: 6px;
            color: #102A43;
        }
        .privacy-note * {color: #102A43 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✈️ Indian Flight Delay Analytics")
st.markdown(
    '<p class="subtitle">Distribuição, correlações e indicadores para apoiar gestores de operações aéreas.</p>',
    unsafe_allow_html=True,
)

if not DATA_PATH.exists():
    st.error(f"Arquivo de dados não encontrado em: {DATA_PATH}")
    st.stop()

df = load_data(DATA_PATH)

st.sidebar.header("Filtros da análise")
selected_variable = st.sidebar.selectbox(
    "Variável quantitativa",
    QUANTITATIVE_COLUMNS,
    index=QUANTITATIVE_COLUMNS.index("Departure_Delay"),
    format_func=lambda value: LABELS[value],
    help="Define a variável do histograma e do filtro de intervalo.",
)

variable_min = float(df[selected_variable].min())
variable_max = float(df[selected_variable].max())
step = 1.0 if pd.api.types.is_integer_dtype(df[selected_variable]) else 0.1
selected_range = st.sidebar.slider(
    f"Intervalo — {LABELS[selected_variable]}",
    min_value=variable_min,
    max_value=variable_max,
    value=(variable_min, variable_max),
    step=step,
    help="Valores fora deste intervalo são excluídos dos dois dashboards.",
)

airlines = sorted(df["Airline"].unique())
selected_airlines = st.sidebar.multiselect(
    "Companhias aéreas",
    airlines,
    default=airlines,
)

weather_options = sorted(df["Weather"].unique())
selected_weather = st.sidebar.multiselect(
    "Condição climática",
    weather_options,
    default=weather_options,
)

filtered = df[
    df[selected_variable].between(selected_range[0], selected_range[1], inclusive="both")
    & df["Airline"].isin(selected_airlines)
    & df["Weather"].isin(selected_weather)
].copy()

st.sidebar.caption(f"{len(filtered):,} de {len(df):,} voos selecionados".replace(",", "."))
st.sidebar.markdown("---")
st.sidebar.info("Os filtros são aplicados simultaneamente às duas abas.")

if filtered.empty:
    empty_state()

tab_lab, tab_kpi = st.tabs(["🔬 Dashboard 1 · Laboratório", "📊 Dashboard 2 · Operações"])

with tab_lab:
    st.header("Laboratório de distribuição e correlação")
    st.caption("Explore a forma da distribuição e as relações lineares entre variáveis quantitativas.")

    left, right = st.columns([1, 1.35], gap="large")

    with left:
        st.subheader(f"Distribuição: {LABELS[selected_variable]}")
        fig_hist, ax_hist = plt.subplots(figsize=(8, 5.4))
        sns.histplot(
            data=filtered,
            x=selected_variable,
            bins=30,
            kde=True,
            color=COLORS["blue"],
            edgecolor="white",
            ax=ax_hist,
        )
        mean_value = filtered[selected_variable].mean()
        median_value = filtered[selected_variable].median()
        ax_hist.axvline(mean_value, color=COLORS["red"], linestyle="--", label=f"Média: {mean_value:.1f}")
        ax_hist.axvline(median_value, color=COLORS["green"], linestyle=":", label=f"Mediana: {median_value:.1f}")
        ax_hist.set_xlabel(LABELS[selected_variable])
        ax_hist.set_ylabel("Quantidade de voos")
        ax_hist.legend(frameon=False)
        sns.despine()
        fig_hist.tight_layout()
        st.pyplot(fig_hist, width="stretch")
        plt.close(fig_hist)

        q1 = filtered[selected_variable].quantile(0.25)
        q3 = filtered[selected_variable].quantile(0.75)
        c1, c2, c3 = st.columns(3)
        c1.metric("Média", format_number(mean_value))
        c2.metric("Mediana", format_number(median_value))
        c3.metric("Intervalo interquartil", format_number(q3 - q1))

    with right:
        st.subheader("Mapa de calor das correlações")
        corr = filtered[QUANTITATIVE_COLUMNS].corr(method="pearson")
        display_labels = [LABELS[col] for col in QUANTITATIVE_COLUMNS]
        fig_corr, ax_corr = plt.subplots(figsize=(11, 8.6))
        sns.heatmap(
            corr,
            cmap="RdBu_r",
            center=0,
            vmin=-1,
            vmax=1,
            square=True,
            linewidths=0.4,
            cbar_kws={"label": "Correlação de Pearson", "shrink": 0.75},
            ax=ax_corr,
        )
        ax_corr.set_xticklabels(display_labels, rotation=45, ha="right", fontsize=8)
        ax_corr.set_yticklabels(display_labels, rotation=0, fontsize=8)
        fig_corr.tight_layout()
        st.pyplot(fig_corr, width="stretch")
        plt.close(fig_corr)

    with st.expander("Como interpretar este painel?"):
        st.markdown(
            """
            - O histograma mostra concentração, dispersão e possíveis assimetrias da variável escolhida.
            - No mapa, valores próximos de **+1** indicam relação linear positiva; próximos de **−1**, relação negativa.
            - Correlação não implica causalidade e deve ser interpretada com conhecimento operacional.
            """
        )

with tab_kpi:
    st.header("Visão executiva para gestores de operações")
    st.caption("Indicadores voltados à pontualidade e à identificação de fontes de risco operacional.")

    total_flights = len(filtered)
    avg_delay = filtered["Departure_Delay"].mean()
    on_time_rate = filtered["Departure_Delay"].le(15).mean() * 100
    severe_delay_rate = filtered["Departure_Delay"].ge(60).mean() * 100
    avg_risk = filtered["Turnaround_Risk_Index"].mean()

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Voos analisados", f"{total_flights:,}".replace(",", "."))
    k2.metric("Atraso médio", f"{format_number(avg_delay)} min")
    k3.metric("Pontualidade (≤15 min)", f"{format_number(on_time_rate)}%")
    k4.metric("Atrasos severos (≥60 min)", f"{format_number(severe_delay_rate)}%")
    k5.metric("Risco médio de turnaround", format_number(avg_risk))

    st.markdown("### Onde priorizar ações")
    chart1, chart2 = st.columns(2, gap="large")

    with chart1:
        airline_summary = (
            filtered.groupby("Airline", as_index=False)
            .agg(Atraso_medio=("Departure_Delay", "mean"), Voos=("Flight_Number", "size"))
            .sort_values("Atraso_medio", ascending=True)
        )
        fig_airline, ax_airline = plt.subplots(figsize=(8, 5.5))
        sns.barplot(data=airline_summary, y="Airline", x="Atraso_medio", color=COLORS["blue"], ax=ax_airline)
        ax_airline.set_title("Atraso médio por companhia")
        ax_airline.set_xlabel("Atraso médio (minutos)")
        ax_airline.set_ylabel("")
        sns.despine()
        fig_airline.tight_layout()
        st.pyplot(fig_airline, width="stretch")
        plt.close(fig_airline)

    with chart2:
        hourly = filtered.groupby("Scheduled_Departure_Hour", as_index=False)["Departure_Delay"].mean()
        fig_hour, ax_hour = plt.subplots(figsize=(8, 5.5))
        sns.lineplot(
            data=hourly,
            x="Scheduled_Departure_Hour",
            y="Departure_Delay",
            marker="o",
            color=COLORS["orange"],
            linewidth=2.5,
            ax=ax_hour,
        )
        ax_hour.set_title("Atraso médio ao longo do dia")
        ax_hour.set_xlabel("Hora programada da partida")
        ax_hour.set_ylabel("Atraso médio (minutos)")
        ax_hour.set_xticks(range(5, 24, 2))
        sns.despine()
        fig_hour.tight_layout()
        st.pyplot(fig_hour, width="stretch")
        plt.close(fig_hour)

    weather_summary = (
        filtered.groupby("Weather", as_index=False)
        .agg(
            Atraso_medio=("Departure_Delay", "mean"),
            Taxa_severa=("Departure_Delay", lambda values: values.ge(60).mean() * 100),
            Voos=("Flight_Number", "size"),
        )
        .sort_values("Atraso_medio", ascending=False)
    )
    fig_weather, ax_weather = plt.subplots(figsize=(12, 4.8))
    sns.barplot(data=weather_summary, x="Weather", y="Atraso_medio", hue="Taxa_severa", palette="YlOrRd", ax=ax_weather)
    ax_weather.set_title("Impacto das condições climáticas no atraso")
    ax_weather.set_xlabel("Condição climática")
    ax_weather.set_ylabel("Atraso médio (minutos)")
    legend = ax_weather.get_legend()
    if legend:
        legend.set_title("% de atrasos severos")
    sns.despine()
    fig_weather.tight_layout()
    st.pyplot(fig_weather, width="stretch")
    plt.close(fig_weather)

    st.markdown(
        '<div class="privacy-note"><b>Privacidade:</b> o painel usa apenas dados operacionais agregados. '
        "Não há nomes, documentos, contatos ou outras informações pessoais de passageiros.</div>",
        unsafe_allow_html=True,
    )

st.caption("Fonte: India Flight Delay Model Input · Recorte histórico de 2023 a 2025")
