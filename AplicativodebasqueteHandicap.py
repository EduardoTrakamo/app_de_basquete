import streamlit as st
import math

st.set_page_config(page_title="Bot de Handicap - Basquete Real", layout="centered")

st.title("🏀 Bot de Handicap - Basquete ao Vivo (com projeção de jogo completo)")
st.markdown("Preencha os dados da partida e receba uma sugestão sólida de aposta baseada na projeção do placar final.")

# Quarto atual
st.subheader("⏱️ Quarto Atual")
quarto_atual = st.selectbox("Estamos em qual quarto?", [1, 2, 3, 4], index=1)
quartos_jogados = quarto_atual
quartos_restantes = 4 - quartos_jogados

# Entradas de pontuação por quarto
st.subheader("📊 Pontos por Quarto - Time A e Time B")
pontos_A = []
pontos_B = []
for i in range(1, 5):
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input(f"Q{i} - Time A", min_value=0, max_value=100, step=1, key=f"A{i}")
    with col2:
        b = st.number_input(f"Q{i} - Time B", min_value=0, max_value=100, step=1, key=f"B{i}")
    pontos_A.append(a)
    pontos_B.append(b)

# Handicaps
st.subheader("📈 Handicaps da Betano")
handicapA = st.text_input("Handicap Time A (ex: -4.5)")
handicapB = st.text_input("Handicap Time B (ex: +4.5)")

# Estatísticas reais
st.subheader("📋 Estatísticas da Partida (parciais ao vivo)")
col1, col2 = st.columns(2)

with col1:
    fg_a = st.text_input("Time A - FG (ex: 23/50)")
    fg3_a = st.text_input("Time A - 3PT (ex: 8/20)")
    reb_a = st.number_input("Time A - Rebotes", min_value=0, step=1)
    tov_a = st.number_input("Time A - Turnovers", min_value=0, step=1)

with col2:
    fg_b = st.text_input("Time B - FG (ex: 20/45)")
    fg3_b = st.text_input("Time B - 3PT (ex: 6/18)")
    reb_b = st.number_input("Time B - Rebotes", min_value=0, step=1)
    tov_b = st.number_input("Time B - Turnovers", min_value=0, step=1)

# Botão para gerar sugestão
if st.button("🎯 Gerar Sugestão de Aposta"):
    try:
        hA = float(handicapA)
        hB = float(handicapB)
    except ValueError:
        st.error("⚠️ Preencha os handicaps corretamente.")
        st.stop()

    total_A = sum(pontos_A)
    total_B = sum(pontos_B)
    diff = total_A - total_B

    # Projeção do placar final
    media_diff_por_quarto = diff / quartos_jogados if quartos_jogados > 0 else 0
    projecao_diff = diff + media_diff_por_quarto * quartos_restantes
    projecao_final_A = total_A + (media_diff_por_quarto * quartos_restantes / 2)
    projecao_final_B = total_B - (media_diff_por_quarto * quartos_restantes / 2)

    margem_proj_A = (projecao_final_A + hA) - projecao_final_B
    margem_proj_B = (projecao_final_B + hB) - projecao_final_A

    def parse_fg(fg_text):
        try:
            made, att = map(int, fg_text.strip().split("/"))
            return (made / att) * 100 if att > 0 else 0
        except:
            return 0

    fg_pct_a = parse_fg(fg_a)
    fg_pct_b = parse_fg(fg_b)
    fg3_pct_a = parse_fg(fg3_a)
    fg3_pct_b = parse_fg(fg3_b)

    def performance(fg, fg3, reb, tov):
        return (0.4 * fg) + (0.2 * fg3) + (0.2 * reb) - (0.2 * tov)

    perf_a = performance(fg_pct_a, fg3_pct_a, reb_a, tov_a)
    perf_b = performance(fg_pct_b, fg3_pct_b, reb_b, tov_b)
    perf_diff = perf_a - perf_b

    def sigmoide(x):
        return 1 / (1 + math.exp(-x))

    chance_A = sigmoide((perf_diff + margem_proj_A) / 5)
    chance_B = sigmoide((-perf_diff + margem_proj_B) / 5)

    st.subheader("📌 Resultado da Análise")
    st.markdown(f"""
    - 🏀 Total Time A: **{total_A}** | Total Time B: **{total_B}**  
    - 📉 Diferença atual: **{diff:+}** após {quartos_jogados} quarto(s)  
    - 📈 Diferença projetada final: **{projecao_diff:+.1f}**  
    - 📏 Margem projetada A: **{margem_proj_A:+.1f}** | B: **{margem_proj_B:+.1f}**  
    - 📊 Performance A: **{perf_a:.1f}** | B: **{perf_b:.1f}**
    """)

    if chance_A > 0.6:
        st.success(f"✅ Sugestão: Apostar no Time A com handicap {hA:+} (Chance de cobertura até o fim: {chance_A*100:.1f}%)")
    elif chance_B > 0.6:
        st.success(f"✅ Sugestão: Apostar no Time B com handicap {hB:+} (Chance de cobertura até o fim: {chance_B*100:.1f}%)")
    elif 0.5 < chance_A <= 0.6:
        st.warning(f"⚠️ Aposta moderada no Time A ({chance_A*100:.1f}%)")
    elif 0.5 < chance_B <= 0.6:
        st.warning(f"⚠️ Aposta moderada no Time B ({chance_B*100:.1f}%)")
    else:
        st.error("❌ Nenhum dos times tem boa chance de cobertura até o fim. Melhor evitar aposta agora.")
