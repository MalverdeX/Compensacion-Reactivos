# Calculadora de Compensación de Reactivos

## Teoría Fundamental

### Potencia Reactiva y Factor de Potencia

La **potencia reactiva (Q)** es la componente de la potencia aparente que no realiza trabajo útil pero es necesaria para mantener los campos magnéticos en equipos inductivos. Se expresa en **voltamperios reactivos (VAR)**.

El **factor de potencia (FP)** es la relación entre la potencia activa (P) y la potencia aparente (S):
```
FP = P/S = cos(φ)
```

Donde φ es el ángulo de desfase entre la tensión y la corriente.

### Tipos de Compensación

#### 1. Compensación Serie
La compensación serie se conecta en línea con la carga, modificando la impedancia total del circuito.

**Para compensación inductiva serie:**
- Se conecta un inductor en serie con la carga
- La reactancia total: X_total = X_carga + X_compensación
- Reduce la corriente en circuitos capacitivos

**Para compensación capacitiva serie:**
- Se conecta un capacitor en serie con la carga
- La reactancia total: X_total = X_carga - X_compensación
- Reduce la corriente en circuitos inductivos

#### 2. Compensación Paralelo
La compensación paralelo se conecta derivada con la carga, suministrando o absorbiendo potencia reactiva.

**Para compensación inductiva paralelo:**
- Se conecta un inductor en paralelo con la carga
- La potencia reactiva total: Q_total = Q_carga + Q_compensación
- Absorbe potencia reactiva en circuitos capacitivos

**Para compensación capacitiva paralelo:**
- Se conecta un capacitor en paralelo con la carga
- La potencia reactiva total: Q_total = Q_carga - Q_compensación
- Suministra potencia reactiva en circuitos inductivos

## Fórmulas Fundamentales

### Triángulo de Potencias
```
S² = P² + Q²
S = P/cos(φ)
Q = P × tan(φ)
```

### Compensación Paralelo (método común)
**Potencia reactiva necesaria para compensación:**
```
Q_c = P × (tan(φ₁) - tan(φ₂))
```
Donde:
- Q_c = potencia reactiva del compensador
- P = potencia activa de la carga
- φ₁ = ángulo inicial (antes de compensar)
- φ₂ = ángulo deseado (después de compensar)

**Capacitancia necesaria para compensación capacitiva:**
```
C = Q_c / (2π × f × V²)
```

**Inductancia necesaria para compensación inductiva:**
```
L = V² / (2π × f × Q_c)
```

### Compensación Serie
**Reactancia de compensación serie:**
```
X_c = Q_c / I²
```

**Para capacitor en serie:**
```
C = 1 / (2π × f × X_c)
```

**Para inductor en serie:**
```
L = X_c / (2π × f)
```

## Parámetros del Sistema

### Frecuencias Estándar
- **60 Hz**: América del Norte, partes de Sudamérica
- **50 Hz**: Europa, Asia, África, Australia

### Tensiones Comunes
- **Baja tensión**: 120V, 127V, 220V, 240V, 277V, 380V, 480V
- **Media tensión**: 2.4kV, 4.16kV, 13.8kV, 33kV
- **Alta tensión**: 69kV, 115kV, 138kV, 230kV, 345kV

## Factores de Potencia Típicos

### Cargas Comunes
- **Motores eléctricos**: 0.7 - 0.9 (inductivo)
- **Transformadores**: 0.8 - 0.95 (inductivo)
- **Lámparas fluorescentes**: 0.5 - 0.9 (inductivo)
- **Computadoras**: 0.6 - 0.8 (inductivo)
- **Equipos electrónicos**: 0.7 - 0.9 (inductivo)

### Objetivos de Compensación
- **Mínimo regulatorio**: FP ≥ 0.90
- **Óptimo económico**: FP ≈ 0.95 - 0.98
- **Máximo técnico**: FP ≈ 0.99 (no se recomienda 1.0 por resonancia)

## Beneficios de la Compensación

### Económicos
- Reducción de facturas eléctricas por penalizaciones
- Disminución de pérdidas en conductores
- Mejor utilización de la capacidad instalada

### Técnicos
- Mejora del regulaje de tensión
- Reducción de caídas de tensión
- Aumento de capacidad de conducción

### Operativos
- Mayor vida útil de equipos
- Mejor calidad del suministro
- Reducción de interferencias electromagnéticas

## Consideraciones Importantes

### Resonancia
La resonancia ocurre cuando la reactancia inductiva iguala a la reactancia capacitiva:
```
X_L = X_C
2π × f × L = 1 / (2π × f × C)
f_resonancia = 1 / (2π × √(L × C))
```

### Armónicos
La compensación puede amplificar armónicos si no se diseña correctamente. Se recomienda:
- Análisis de espectro armónico
- Filtros de armónicos si es necesario
- Evitar sobrecompensación

### Seguridad
- Descarga de capacitores antes del mantenimiento
- Protección contra sobretensiones
- Coordinación de protecciones
