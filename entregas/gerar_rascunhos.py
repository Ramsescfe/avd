"""Gera os dois rascunhos dos dashboards exigidos na entrega."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle


OUTPUT_DIR = Path(__file__).parent
NAVY = "#12263A"
BLUE = "#2F80ED"
LIGHT = "#F4F7FB"
MID = "#DCE6F2"
TEXT = "#29435C"


def box(ax, x, y, width, height, title, subtitle="", color="white"):
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.015",
        linewidth=1.4,
        edgecolor=MID,
        facecolor=color,
    )
    ax.add_patch(patch)
    ax.text(x + 0.02, y + height - 0.04, title, fontsize=12, weight="bold", color=NAVY, va="top")
    if subtitle:
        ax.text(x + 0.02, y + height - 0.085, subtitle, fontsize=8.5, color=TEXT, va="top")


def base_canvas(title, tab_active):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor(LIGHT)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0.91), 1, 0.09, facecolor=NAVY, edgecolor="none"))
    ax.text(0.03, 0.955, "INDIAN FLIGHT DELAY ANALYTICS", color="white", fontsize=18, weight="bold", va="center")
    ax.text(0.03, 0.89, title, color=NAVY, fontsize=15, weight="bold", va="top")
    ax.text(0.34, 0.845, "DASHBOARD 1 · LABORATÓRIO", color=BLUE if tab_active == 1 else TEXT, fontsize=10, weight="bold")
    ax.text(0.59, 0.845, "DASHBOARD 2 · OPERAÇÕES", color=BLUE if tab_active == 2 else TEXT, fontsize=10, weight="bold")
    return fig, ax


def sidebar(ax):
    box(ax, 0.025, 0.06, 0.27, 0.76, "FILTROS DA ANÁLISE", "Aplicados simultaneamente às duas abas")
    box(ax, 0.05, 0.62, 0.22, 0.11, "Seletor de variável", "Ex.: Atraso na partida")
    box(ax, 0.05, 0.46, 0.22, 0.11, "Filtro de intervalo", "Slider mínimo — máximo")
    box(ax, 0.05, 0.30, 0.22, 0.11, "Companhias aéreas", "Seleção múltipla")
    box(ax, 0.05, 0.14, 0.22, 0.11, "Condição climática", "Seleção múltipla")


def dashboard_1():
    fig, ax = base_canvas("Rascunho 1 — Laboratório de distribuição e correlação", 1)
    sidebar(ax)
    box(ax, 0.33, 0.47, 0.29, 0.35, "HISTOGRAMA", "Distribuição da variável selecionada")
    for i, height in enumerate([0.05, 0.12, 0.20, 0.25, 0.18, 0.10, 0.06]):
        ax.add_patch(Rectangle((0.36 + i * 0.033, 0.53), 0.026, height, color=BLUE, alpha=0.82))
    ax.plot([0.475, 0.475], [0.52, 0.76], color="#EB5757", linestyle="--", linewidth=2)
    box(ax, 0.65, 0.22, 0.32, 0.60, "MAPA DE CALOR", "Correlação de Pearson")
    colors = ["#2166AC", "#67A9CF", "#D1E5F0", "#FDD4C2", "#EF8A62", "#B2182B"]
    for row in range(7):
        for col in range(7):
            ax.add_patch(Rectangle((0.69 + col * 0.035, 0.37 + row * 0.05), 0.032, 0.046, color=colors[(row + col * 2) % len(colors)]))
    for idx, label in enumerate(["MÉDIA", "MEDIANA", "INTERVALO INTERQUARTIL"]):
        box(ax, 0.33 + idx * 0.1, 0.28, 0.085, 0.12, label, "valor")
    box(ax, 0.33, 0.08, 0.29, 0.13, "COMO INTERPRETAR", "Texto de apoio sobre distribuição e correlação", color="#EEF5FF")
    fig.savefig(OUTPUT_DIR / "rascunho_dashboard1.png", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def dashboard_2():
    fig, ax = base_canvas("Rascunho 2 — KPIs para gestores de operações", 2)
    sidebar(ax)
    kpis = ["VOOS", "ATRASO MÉDIO", "PONTUALIDADE", "SEVEROS", "RISCO"]
    for idx, label in enumerate(kpis):
        box(ax, 0.33 + idx * 0.128, 0.68, 0.112, 0.14, label, "valor do KPI")
    box(ax, 0.33, 0.37, 0.30, 0.25, "ATRASO POR COMPANHIA", "Gráfico de barras horizontais")
    for i, width in enumerate([0.12, 0.19, 0.14, 0.23, 0.17]):
        ax.add_patch(Rectangle((0.37, 0.42 + i * 0.032), width, 0.02, color=BLUE, alpha=0.84))
    box(ax, 0.66, 0.37, 0.31, 0.25, "ATRASO AO LONGO DO DIA", "Gráfico de linha por hora")
    xs = [0.70, 0.75, 0.80, 0.85, 0.90, 0.94]
    ys = [0.44, 0.50, 0.47, 0.55, 0.52, 0.58]
    ax.plot(xs, ys, marker="o", color="#F2994A", linewidth=3)
    box(ax, 0.33, 0.08, 0.64, 0.23, "IMPACTO DAS CONDIÇÕES CLIMÁTICAS", "Barras: atraso médio · cor: percentual de atrasos severos")
    for i, height in enumerate([0.07, 0.11, 0.15, 0.18]):
        ax.add_patch(Rectangle((0.43 + i * 0.11, 0.12), 0.07, height, color=["#FDD49E", "#FDBB84", "#FC8D59", "#D7301F"][i]))
    fig.savefig(OUTPUT_DIR / "rascunho_dashboard2.png", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    dashboard_1()
    dashboard_2()
