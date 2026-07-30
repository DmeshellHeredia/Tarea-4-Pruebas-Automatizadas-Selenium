# Matriz de trazabilidad — Tarea 4

Relación completa entre las 5 historias de usuario, sus 15 escenarios de
prueba (camino feliz, negativo y de límites), el archivo automatizado
correspondiente, los marcadores de pytest, la captura generada y el
resultado obtenido en la ejecución final de regresión.

## Pruebas funcionales (15)

| Historia | Tipo de escenario | Nombre exacto de la prueba | Archivo de prueba | Marcadores pytest | Captura | Resultado esperado | Resultado final |
|---|---|---|---|---|---|---|---|
| HU-01 — Inicio de sesión | Camino feliz | `test_hu01_login_valido` | `tests/test_login.py` | `selenium`, `login`, `happy` | `HU01_login_feliz.png` | Redirección a `/productos`, sesión activa, botón de logout visible | Passed |
| HU-01 — Inicio de sesión | Prueba negativa | `test_hu01_login_credenciales_invalidas` | `tests/test_login.py` | `selenium`, `login`, `negative` | `HU01_login_negativo.png` | Permanece en `/login`, mensaje genérico, sin sesión | Passed |
| HU-01 — Inicio de sesión | Prueba de límites | `test_hu01_login_campos_vacios` | `tests/test_login.py` | `selenium`, `login`, `boundary` | `HU01_login_limite.png` | Mensajes de campo obligatorio, sin sesión | Passed |
| HU-02 — Registrar producto | Camino feliz | `test_hu02_crear_producto_valido` | `tests/test_create_product.py` | `selenium`, `create`, `happy` | `HU02_crear_feliz.png` | Producto registrado, visible en el listado y en MySQL | Passed |
| HU-02 — Registrar producto | Prueba negativa | `test_hu02_crear_producto_invalido` | `tests/test_create_product.py` | `selenium`, `create`, `negative` | `HU02_crear_negativo.png` | `error-precio`/`error-cantidad` visibles, no se inserta el producto | Passed |
| HU-02 — Registrar producto | Prueba de límites | `test_hu02_crear_producto_valores_limite` | `tests/test_create_product.py` | `selenium`, `create`, `boundary` | `HU02_crear_limite.png` | Nombre 100 car., categoría 80 car., precio `99999999.99`, cantidad `2147483647` aceptados sin truncar | Passed |
| HU-03 — Consultar productos | Camino feliz | `test_hu03_consultar_producto_existente` | `tests/test_read_products.py` | `selenium`, `read`, `happy` | `HU03_consultar_feliz.png` | Todos los datos del producto visibles y coincidentes con MySQL | Passed |
| HU-03 — Consultar productos | Prueba negativa | `test_hu03_consultar_sin_autenticacion` | `tests/test_read_products.py` | `selenium`, `read`, `negative` | `HU03_consultar_negativo.png` | Redirección a `/login`, sin datos del inventario visibles | Passed |
| HU-03 — Consultar productos | Prueba de límites | `test_hu03_consultar_unico_producto_con_valores_limite` | `tests/test_read_products.py` | `selenium`, `read`, `boundary` | `HU03_consultar_limite.png` | Exactamente una fila, valores máximos completos sin truncar | Passed |
| HU-04 — Actualizar producto | Camino feliz | `test_hu04_actualizar_producto_valido` | `tests/test_update_product.py` | `selenium`, `update`, `happy` | `HU04_actualizar_feliz.png` | Precio y cantidad actualizados, mensaje de éxito, reflejado en MySQL | Passed |
| HU-04 — Actualizar producto | Prueba negativa | `test_hu04_actualizar_producto_invalido` | `tests/test_update_product.py` | `selenium`, `update`, `negative` | `HU04_actualizar_negativo.png` | `error-precio`/`error-cantidad` visibles, MySQL sin cambios | Passed |
| HU-04 — Actualizar producto | Prueba de límites | `test_hu04_actualizar_producto_valores_limite` | `tests/test_update_product.py` | `selenium`, `update`, `boundary` | `HU04_actualizar_limite.png` | Valores máximos guardados completos, sin truncar | Passed |
| HU-05 — Eliminar producto | Camino feliz | `test_hu05_eliminar_producto_confirmado` | `tests/test_delete_product.py` | `selenium`, `delete`, `happy` | `HU05_eliminar_feliz.png` | Alerta aceptada, producto eliminado, mensaje de éxito, sin registro en MySQL | Passed |
| HU-05 — Eliminar producto | Prueba negativa | `test_hu05_cancelar_eliminacion` | `tests/test_delete_product.py` | `selenium`, `delete`, `negative` | `HU05_eliminar_negativo.png` | Alerta cancelada, producto permanece, sin mensaje de eliminación | Passed |
| HU-05 — Eliminar producto | Prueba de límites | `test_hu05_eliminar_unico_producto` | `tests/test_delete_product.py` | `selenium`, `delete`, `boundary` | `HU05_eliminar_limite.png` | Único producto eliminado, listado vacío, cero registros en MySQL | Passed |

## Prueba técnica (no asociada a una historia)

| Tipo | Nombre exacto de la prueba | Archivo de prueba | Marcadores pytest | Captura | Propósito | Resultado final |
|---|---|---|---|---|---|---|
| Humo / infraestructura | `test_humo_infraestructura_selenium` | `tests/test_infraestructura_selenium.py` | `selenium`, `smoke` | `test_humo_infraestructura_selenium.png` | Valida servidor de pruebas (puerto 5001), base `tarea4_selenium_test`, navegador Selenium y login end-to-end, sin ser parte de las 15 pruebas de historias | Passed |

## Resumen

- 5 historias de usuario, 3 escenarios cada una: **15 pruebas funcionales**.
- **1 prueba técnica de humo**, adicional y no asociada a una historia.
- **16 pruebas en total**, todas con resultado **Passed** en la ejecución final de regresión.
- **16 capturas** en `reports/screenshots/`, una por escenario, embebidas en `reports/report.html`.
