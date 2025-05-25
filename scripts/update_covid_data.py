import pandas as pd
import requests
import json
import os
from datetime import datetime

# URL do arquivo CSV da OMS
DATA_URL = "https://data.who.int/dashboards/covid19/who-covid-19-global-data.csv"
# País de interesse
TARGET_COUNTRY = 'Brazil'

# Função para formatar números com separador de milhares (para o Brasil, use ponto)
def format_number_br(value):
    if pd.isna(value):
        return "-"
    return f"{int(value):,}".replace(",", ".") # Substitui vírgula por ponto para milhares

def fetch_and_process_data():
    try:
        # Baixar os dados
        print(f"Baixando dados de: {DATA_URL}")
        response = requests.get(DATA_URL, stream=True) # Use stream=True para arquivos grandes
        response.raise_for_status() # Lança um erro para status de resposta ruins (4xx ou 5xx)

        # Carregar os dados em um DataFrame do Pandas diretamente do conteúdo da resposta
        # Decodificar o conteúdo da resposta e usar io.StringIO para ler como arquivo
        from io import StringIO
        df = pd.read_csv(StringIO(response.content.decode('utf-8')))
        print("Dados baixados e carregados com sucesso.")

        # Inspecionar as colunas disponíveis para depuração
        # print("Colunas disponíveis no CSV:", df.columns.tolist())

        # Renomear colunas para consistência (se necessário, com base na inspeção)
        # As colunas da OMS parecem ser 'Country', 'Date_reported', 'Cumulative_cases', 'Cumulative_deaths'
        df.rename(columns={
            'Country': 'location',
            'Date_reported': 'date',
            'Cumulative_cases': 'total_cases',
            'Cumulative_deaths': 'total_deaths'
        }, inplace=True)

        # Filtrar dados para o país de interesse
        df_country = df[df['location'] == TARGET_COUNTRY].copy()

        # Converter a coluna 'date' para datetime
        df_country['date'] = pd.to_datetime(df_country['date'])

        if df_country.empty:
            print(f"Nenhum dado encontrado para o país '{TARGET_COUNTRY}'.")
            return {
                "total_cases": "-",
                "total_deaths": "-",
                "lethality_rate": "-",
                "data_date": "N/A"
            }

        # Ordenar por data para garantir que a última data seja a mais recente
        df_country = df_country.sort_values(by='date', ascending=False)

        # Obter a linha com a data mais recente disponível para o país
        latest_data_row = df_country.iloc[0]

        # Obter os totais acumulados da última data
        total_cases = latest_data_row['total_cases']
        total_deaths = latest_data_row['total_deaths']
        latest_date = latest_data_row['date']

        # Calcular a taxa de letalidade
        lethality_rate = None
        if pd.notna(total_cases) and total_cases > 0:
            lethality_rate = (total_deaths / total_cases) * 100

        # Preparar os dados para o JSON
        data_to_save = {
            "total_cases": format_number_br(total_cases),
            "total_deaths": format_number_br(total_deaths),
            "lethality_rate": f"{lethality_rate:.2f}%" if lethality_rate is not None else "-",
            "data_date": latest_date.strftime('%d/%m/%Y') if pd.notna(latest_date) else "N/A"
        }

        # Criar a pasta 'data' se não existir
        output_dir = 'data'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'covid_metrics.json')

        # Salvar os dados em um arquivo JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

        print(f"Dados processados e salvos em: {output_path}")
        print(f"Última data de dados: {data_to_save['data_date']}")
        print(f"Total de casos: {data_to_save['total_cases']}")
        print(f"Total de óbitos: {data_to_save['total_deaths']}")
        print(f"Taxa de Letalidade: {data_to_save['lethality_rate']}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar os dados: {e}")
    except pd.errors.EmptyDataError:
        print("Erro: O arquivo CSV está vazio ou mal formatado.")
    except KeyError as e:
        print(f"Erro de coluna: A coluna {e} não foi encontrada no CSV. Verifique os nomes das colunas da OMS.")
        print("Colunas disponíveis no CSV (primeiras linhas):")
        print(df.head()) # Imprime as primeiras linhas para ajudar a depurar
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    fetch_and_process_data()
