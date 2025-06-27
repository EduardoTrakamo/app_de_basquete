import streamlit as st

st.set_page_config(page_title="Bot de Handicap - eBasketball", layout="centered")

st.title("🏀 Bot de Handicap - eBasketball ao Vivo")
st.markdown("Insira os pontos por quarto e os handicaps da Betano para obter uma sugestão de aposta.")

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

st.subheader("📈 Handicaps da Betano")
handicapA = st.text_input("Handicap Time A (ex: -6.5)")
handicapB = st.text_input("Handicap Time B (ex: +6.5)")

if st.button("🎯 Gerar Sugestão de Aposta"):
    total_A = sum(pontos_A)
    total_B = sum(pontos_B)
    diff = total_A - total_B

    # Detectar quartos com pontos
    quartos_validos = [(a, b) for a, b in zip(pontos_A, pontos_B) if (a != 0 or b != 0)]
    deltas = []
    for i in range(1, len(quartos_validos)):
        ant_diff = quartos_validos[i-1][0] - quartos_validos[i-1][1]
        atual_diff = quartos_validos[i][0] - quartos_validos[i][1]
        deltas.append(atual_diff - ant_diff)
    tendencia_media = sum(deltas)/len(deltas) if deltas else 0

    try:
        hA = float(handicapA)
        hB = float(handicapB)
    except ValueError:
        st.error("⚠️ Preencha os handicaps corretamente (ex: -6.5, +6.5).")
        st.stop()

    # ✅ Cálculo corrigido da margem real
    margem_A = (total_A + hA) - total_B
    margem_B = (total_B + hB) - total_A

    if margem_A >= 2:
        sugestao = f"✅ Forte sugestão: Apostar no Time A com handicap {hA:+}"
        margem_info = f"📏 Margem atual: Cobre com {margem_A:.1f} pontos de folga"
        alerta = f"🚨 Time A cobre handicap {hA:+} com margem de {margem_A:.1f} pontos."
    elif margem_B >= 2:
        sugestao = f"✅ Forte sugestão: Apostar no Time B com handicap {hB:+}"
        margem_info = f"📏 Margem atual: Cobre com {margem_B:.1f} pontos de folga"
        alerta = f"🚨 Time B cobre handicap {hB:+} com margem de {margem_B:.1f} pontos."
    elif -1 <= margem_A < 2:
        sugestao = f"⚠️ Sugestão moderada: Apostar com cautela no Time A com handicap {hA:+}"
        margem_info = f"📏 Margem atual: Faltam {abs(margem_A):.1f} pontos para cobrir"
        alerta = ""
    elif -1 <= margem_B < 2:
        sugestao = f"⚠️ Sugestão moderada: Apostar com cautela no Time B com handicap {hB:+}"
        margem_info = f"📏 Margem atual: Faltam {abs(margem_B):.1f} pontos para cobrir"
        alerta = ""
    else:
        sugestao = "❌ Nenhum dos times está próximo de cobrir. Melhor evitar aposta agora."
        margem_info = f"📏 Time A: {margem_A:+.1f} | Time B: {margem_B:+.1f}"
        alerta = ""

    comentario = (
        "O Time A está crescendo no jogo." if tendencia_media > 0 else
        "O Time B está crescendo no jogo." if tendencia_media < 0 else
        "Jogo equilibrado em tendência."
    )

    st.subheader("📋 Resultado da Análise")
    st.markdown(f"""
    - 🏀 Total Time A: **{total_A}** | Total Time B: **{total_B}**  
    - 📉 Diferença atual: **{diff}**
    - 📈 Tendência: **{tendencia_media:.2f} por quarto**
    - 💡 {comentario}
    - 🎯 **{sugestao}**
    - {margem_info}
    - {alerta}
    """)
