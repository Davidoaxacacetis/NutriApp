Aquí tienes tu texto convertido al **formato Markdown (MD)** correctamente estructurado:

---

# Comparativa de APIs Nutricionales


---

## API Seleccionada y Justificación

La API seleccionada es **USDA FoodData Central (FDC)**, porque:

* Es gratuita y de dominio público.
* Tiene documentación clara y ejemplos JSON.
* Proporciona datos confiables y detallados de macronutrientes y micronutrientes.
* Es suficiente para fines académicos y proyectos de análisis nutricional.

---

## Ejemplos de Solicitudes y Respuestas

### Ejemplo 1: Búsqueda de alimentos por nombre

**Solicitud (curl):**

```bash
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=banana&api_key=TU_API_KEY"
```

**Respuesta JSON (simplificada):**

```json
{
  "foods": [
    {
      "fdcId": 1102647,
      "description": "Bananas, raw",
      "dataType": "Foundation",
      "foodNutrients": [
        { "name": "Protein", "amount": 1.09, "unitName": "g" },
        { "name": "Total lipid (fat)", "amount": 0.33, "unitName": "g" },
        { "name": "Carbohydrate, by difference", "amount": 22.84, "unitName": "g" },
        { "name": "Energy", "amount": 89, "unitName": "kcal" }
      ]
    }
  ]
}
```

---

### Ejemplo 2: Obtener información detallada de un alimento por ID

**Solicitud (curl):**

```bash
curl "https://api.nal.usda.gov/fdc/v1/food/1102647?api_key=TU_API_KEY"
```

**Respuesta JSON (simplificada):**

```json
{
  "fdcId": 1102647,
  "description": "Bananas, raw",
  "foodNutrients": [
    { "name": "Protein", "amount": 1.09, "unitName": "g" },
    { "name": "Total lipid (fat)", "amount": 0.33, "unitName": "g" },
    { "name": "Carbohydrate, by difference", "amount": 22.84, "unitName": "g" },
    { "name": "Energy", "amount": 89, "unitName": "kcal" }
  ],
  "foodPortions": [
    { "portionDescription": "100 g", "gramWeight": 100 }
  ]
}
```

---

## Dificultades Encontradas y Soluciones

| **Dificultad**                                                  | **Solución**                                                                     |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Registro y obtención de API key tarda unas horas                | Solicitar con anticipación y revisar correo spam                                 |
| Estructura de respuesta JSON muy extensa                        | Usar Postman para visualizar mejor la jerarquía y filtrar solo campos relevantes |
| Límite de 1,000 peticiones por hora                             | Implementar cache local de resultados frecuentes para no repetir consultas       |
| Algunos alimentos no aparecen con nombres específicos de marcas | Buscar por nombre genérico (ej. “banana” en lugar de “banana Chiquita”)          |

---

