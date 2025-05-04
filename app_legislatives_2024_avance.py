
import streamlit as st
import pandas as pd
import json
import plotly.express as px

# --- Chargement des données ---
votes_df = pd.read_excel("Législatives 2024 Geo v1.0.xlsx", sheet_name="Votes")
iris_df = pd.read_excel("Législatives 2024 Geo v1.0.xlsx", sheet_name="IRIS_DISP")

iris_df = iris_df.rename(columns={
    "Taux de pauvreté au seuil de 60 % (%)": "Pauvre",
    "dont part des indemnités de chômage (%)": "Chomage",
    "Part des pensions, retraites et rentes (%)": "Pensions",
    "Part de l'ensemble des prestations sociales (%)": "Prestations",
    "dont part des prestations logement (%)": "Prestations_logement"
})

for col in ["Pauvre", "Chomage", "Pensions", "Prestations", "Prestations_logement"]:
    iris_df[col] = iris_df[col].astype(str).str.replace(",", ".").str.extract('([\d\.]+)').astype(float)

partis = ['% ENS', '% LFI', '% RN', '% ECO', '% LR', '% PS', '% UDI', '% REC']

st.title("Carte interactive - Législatives 2024 Paris (version avancée)")
st.sidebar.header("Filtres")

parti_selection = st.sidebar.multiselect("Sélectionnez le ou les partis :", [p.replace('% ', '') for p in partis], default=[p.replace('% ', '') for p in partis])
indicateur_selection = st.sidebar.selectbox("Sélectionnez un indicateur social :", ["Pauvre", "Chomage", "Pensions", "Prestations", "Prestations_logement"])
quartiers = sorted(votes_df['Quartier'].dropna().unique())
quartier_selection = st.sidebar.multiselect("Sélectionnez un ou plusieurs quartiers :", quartiers, default=quartiers)

votes_filtered = votes_df[votes_df['Quartier'].isin(quartier_selection)]

votes_agg = votes_filtered.groupby("Quartier")[partis].mean().reset_index()
votes_agg['Parti dominant'] = votes_agg[partis].idxmax(axis=1).str.replace('% ', '')

couleurs_partis = {
    'ENS': '#ADD8E6',
    'LFI': 'red',
    'RN': 'black',
    'ECO': 'green',
    'LR': 'darkblue',
    'PS': 'pink',
    'UDI': 'gray',
    'REC': 'brown'
}
votes_agg['couleur'] = votes_agg['Parti dominant'].map(couleurs_partis)
votes_plot = votes_filtered.merge(votes_agg[['Quartier', 'Parti dominant', 'couleur']], on="Quartier", how="left")

fig = px.scatter_mapbox(
    votes_plot,
    lat="LAT",
    lon="LON",
    color=votes_plot['Parti dominant'],
    color_discrete_map=couleurs_partis,
    size=votes_plot[[f"% {p}" for p in parti_selection]].max(axis=1),
    size_max=20,
    zoom=11,
    mapbox_style="carto-positron",
    hover_name="Quartier",
    hover_data={p: True for p in partis}
)

votes_plot = votes_plot.merge(iris_df[["Quartier", indicateur_selection]], on="Quartier", how="left")
fig.update_traces(marker=dict(opacity=0.8))
st.plotly_chart(fig, use_container_width=True)

st.header("Résultats détaillés")
for quartier in quartier_selection:
    st.subheader(f"Quartier : {quartier}")
    vote_row = votes_agg[votes_agg['Quartier'] == quartier]
    iris_row = iris_df[iris_df['Quartier'] == quartier]

    if not vote_row.empty:
        for p in partis:
            if p.replace('% ', '') in parti_selection:
                st.write(f"{p} : {vote_row.iloc[0][p]*100:.1f}%")

    if not iris_row.empty:
        ind_value = iris_row.iloc[0][indicateur_selection]
        st.write(f"{indicateur_selection} : {ind_value if pd.notnull(ind_value) else 'N/A'}%")
