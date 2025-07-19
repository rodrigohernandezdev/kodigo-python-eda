import pandas as pd
from ydata_profiling import ProfileReport


def main():
    """
    Main function to load and display a CSV file.
    """
    df = read_csv('data/the_oscar_award.csv')
    if df is None:
        print("No hay datos para mostrar.")
        return
    df = clean_and_transform(df)
    exploratory_data_analysis(df)


def clean_and_transform(df):
    """
    Cleans and transforms the DataFrame.
    - Shows variable types
    - Handles missing values
    - Strips whitespace from object columns
    - Drops duplicates
    """
    print("Información del DataFrame (antes de limpiar):")
    print(df.info())
    print("\nValores faltantes por columna:")
    print(df.isnull().sum())

    # name and film have null or empty values, drop those rows
    # used copy instead of inplace to avoid SettingWithCopyWarning
    df = df.dropna(subset=['name', 'film']).copy()

    for col in df.select_dtypes(include=['object']).columns:
        df.loc[:, col] = df[col].str.strip()

    # delete duplicated data
    df = df.drop_duplicates()

    print("\nInformación del DataFrame (después de limpiar):")
    print(df.info())
    print("\nValores faltantes por columna (después de limpiar):")
    print(df.isnull().sum())
    print(f"DataFrame limpio y transformado. Forma: {df.shape}")
    return df


def read_csv(file_path):
    """
    Reads a CSV file and returns a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None
    print(f"DataFrame cargado desde {file_path}")
    print(f"Filas totales: {df.shape[0]}, Columnas totales: {df.shape[1]}")
    return df


def exploratory_data_analysis(df):
    """
    Performs exploratory data analysis (EDA) on the DataFrame.
    Prints summary statistics, value counts, and basic trends.
    Also generates an HTML report using ydata-profiling.
    """
    print("\n===== Análisis Exploratorio de Datos (EDA) =====\n")
    print("Resumen estadístico de variables numéricas:")
    print(df.describe())
    print("\nResumen estadístico de variables categóricas:")
    print(df.describe(include=['object']))

    print("\nValores únicos por columna:")
    for col in df.columns:
        print(f"{col}: {df[col].nunique()} únicos")

    print("\nFrecuencias de las principales columnas categóricas:")
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        print(f"\nFrecuencias de '{col}':")
        print(df[col].value_counts().head(10))

    print("\nMedias, medianas y desviaciones estándar de variables numéricas:")
    num_cols = df.select_dtypes(include=['number']).columns
    for col in num_cols:
        print(f"{col}: media={df[col].mean()}, mediana={df[col].median()}, desviación estándar={df[col].std()}")
    print("\n===== Fin del EDA =====\n")

    # Generar reporte HTML con ydata-profiling
    print("Generando reporte HTML de EDA con ydata-profiling...")
    profile = ProfileReport(df, title="Reporte EDA - Oscars", explorative=True)
    profile.to_file("oscar_eda_report.html")
    print("Reporte HTML guardado como 'oscar_eda_report.html'.")


if __name__ == "__main__":
    main()
