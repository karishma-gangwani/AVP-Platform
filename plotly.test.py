import plotly.express as px

df_test = px.data.iris()
fig_scatter = px.scatter(df_test, x="sepal_width", y="sepal_length", color="species")
fig_scatter.show()