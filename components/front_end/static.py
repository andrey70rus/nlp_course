import dash
from dash import html, dcc
import pandas as pd
import requests
import dash_bootstrap_components as dbc

# Создаем объект Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])  # OR MATERIA | MINTY | FLATLY

# Описываем интерфейс

slider = html.Div(
    [
        dbc.Label("Глубина анализа, дней", html_for="slider_depth"),
        dcc.Slider(id="slider_depth", min=2, max=14, step=1, value=7),
    ],
    className="mb-3", style={'max-width': 500}
)

app.layout = dbc.Container([
    dbc.Container([
        html.H1("Ключевые слова Telegram канала", className="display-3"),
        dbc.Form(
            [
                dbc.Label("Введите ссылку на Telegram канал:"),
                dbc.Input(id="telegram_url", placeholder="https://t.me/...", type="url"),
                slider,
                dbc.Button(
                    "Получить ключевые слова",
                    id="submit_button", color="primary", className="mt-3"
                ),
            ]
        )
    ]),
    html.Div(id="table_container", className="mt-3")
], fluid=True, style={"margin": "16px"})


# Функция для загрузки таблиц из API и их представления в виде HTML
def get_tables(telegram_url, slider_depth):

    channel_link = telegram_url.replace('https://t.me/', '')
    response = requests.get(
        '127.0.0.1:7070'
        f'/api/key_words_qualifier/get_keywords/{channel_link}_{slider_depth}'
    )

    # Получаем JSON-ответ и преобразуем его в DataFrame
    df = pd.DataFrame(response.json())
    # Создаем HTML-таблицу на основе DataFrame
    table = html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(len(df))
        ])
    ], className="table table-responsive table-striped")
    # Возвращаем HTML-таблицу
    return table


# Описываем callback-функцию для кнопки "Получить таблицы"
@app.callback(
    dash.dependencies.Output("table_container", "children"),
    [dash.dependencies.Input("submit_button", "n_clicks")],
    [dash.dependencies.State("telegram_url", "value")],
    [dash.dependencies.State("slider_depth", "value")]
)
def update_tables(n_clicks, telegram_url, slider_depth):
    if n_clicks is not None:
        return get_tables(telegram_url, slider_depth)


# Запускаем приложение
if __name__ == "__main__":
    app.run_server(debug=True)
