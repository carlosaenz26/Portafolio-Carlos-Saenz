import pandas as pd
import matplotlib.pyplot as plt

def visualize_data(data, x_col, y_col):
    try:
        df = pd.DataFrame(data)
        plt.figure(figsize=(10, 6))
        plt.plot(df[x_col], df[y_col], marker='o')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f'{y_col} vs {x_col}')
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"❌ Error al visualizar los datos: {e}")
