import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

print("Iniciando entrenamiento del modelo Random Forest...")

# 1. Simulación de datos históricos de ALO SERVICE & PARTS
np.random.seed(42)
datos = {
    'horas_operacion': np.random.randint(100, 5000, 1000),
    'temperatura_promedio_c': np.random.normal(70, 15, 1000),
    'nivel_vibracion_mms': np.random.normal(5, 2, 1000),
    'dias_desde_ultimo_mtto': np.random.randint(10, 365, 1000),
    'falla_inminente': np.random.choice([0, 1], 1000, p=[0.85, 0.15]) 
}

df = pd.DataFrame(datos)
X = df.drop('falla_inminente', axis=1)
y = df['falla_inminente']

# 2. Entrenamiento
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X, y)

# 3. Guardar el modelo en la carpeta correcta
os.makedirs('app/ml_core', exist_ok=True)
ruta_modelo = 'app/ml_core/modelo_mantenimiento.pkl'
joblib.dump(modelo, ruta_modelo)

print(f"✅ ¡Cerebro creado exitosamente en {ruta_modelo}!")