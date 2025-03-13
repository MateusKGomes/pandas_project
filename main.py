import pandas as pd
from meses_pt import meses_pt

df = pd.read_csv("./data/BASE_CASE_DATA.csv",
                 encoding="utf-8-sig",
                 sep=";",
                 engine="python")


df.columns = [col.replace('�', 'ã') for col in df.columns]

data_referencia =pd.to_datetime("2024-01-01")
df['Data de nascimento:'] = pd.to_datetime(df['Data de nascimento:'], dayfirst=True)


def calcular_idade(data_nascimento, ref):
    return ref.year - data_nascimento.year - ((ref.month, ref.day) < (data_nascimento.month, data_nascimento.day))

df["idade"] = df['Data de nascimento:'].apply(calcular_idade, args=(data_referencia,))

nota_cols = [col for col in df.columns if col.startswith('Nota:')]
df[nota_cols] = df[nota_cols].apply(pd.to_numeric, errors='coerce')
df['Media_Notas'] = df[nota_cols].mean(axis=1).round(2)


df_aptos = df[
    (df["idade"].between(20, 60)) &
    (df['Media_Notas'] >= 65)
]

print(df_aptos)

#Para ONG
total_candidatos = len(df)
cidade_mais_frequente = df["Unidade:"].value_counts().idxmax()
media_notas = df['Media_Notas'].mean()
total_aptos = len(df_aptos)

#Para a prefeitura
total_aptos = len(df_aptos)
total_candidatos = len(df)
taxa_aptos = (total_aptos / total_candidatos) * 100

#
data_cols = [col for col in df.columns if col.startswith('Data conclusão')]

df[data_cols] = df[data_cols].replace('-', pd.NaT)

meses_pt = {
    'jan': '01',
    'fev': '02',
    'mar': '03',
    'abr': '04',
    'mai': '05',
    'jun': '06',
    'jul': '07',
    'ago': '08',
    'set': '09',
    'out': '10',
    'nov': '11',
    'dez': '12'
}

for col in data_cols:
    for abreviacao, numero in meses_pt.items():
        df[col] = df[col].astype(str).str.replace(
            fr'\b{abreviacao}\b', 
            numero, 
            case=False, 
            regex=True
        )

df[data_cols] = df[data_cols].apply(pd.to_datetime, errors='coerce', dayfirst=True)

primeira_chamada = df[
    (df[data_cols] < '2023-11-01') 
    .all(axis=1)               
]

segunda_chamada = df[
    ((df[data_cols] >= '2023-01-01') & 
     (df[data_cols] <= '2023-12-31'))
    .all(axis=1)                      
]

