-- =============================================================================
-- 1. BACKUP DE SEGURIDAD
-- =============================================================================

-- Crear tablas de backup
CREATE TABLE IF NOT EXISTS backup_ventas AS SELECT * FROM Ventas;
CREATE TABLE IF NOT EXISTS backup_detalles_ventas AS SELECT * FROM Detalles_Ventas;

-- Verificar backups
SELECT 
    'Ventas backup' as tabla, 
    COUNT(*) as registros 
FROM backup_ventas
UNION ALL
SELECT 
    'Detalles_Ventas backup', 
    COUNT(*) 
FROM backup_detalles_ventas;

-- Crear vista temporal para ver datos actuales
CREATE OR REPLACE VIEW vista_pre_migracion AS
SELECT 
    'VENTAS' as origen,
    id_venta,
    id_cliente,
    nombre_cliente as nombre_redundante,
    email as email_redundante
FROM Ventas
WHERE id_venta IN (1, 2, 3)  -- Solo muestra primeros 3 para ejemplo
UNION ALL
SELECT 
    'DETALLES_VENTAS' as origen,
    id_venta,
    id_producto,
    nombre_producto as nombre_redundante,
    '' as email_redundante
FROM Detalles_Ventas
WHERE id_venta IN (1, 2, 3);

SELECT * FROM vista_pre_migracion;

-- =============================================================================
-- 2. VERIFICACIÓN DE INTEGRIDAD REFERENCIAL
-- =============================================================================

-- Verificar que todos los id_cliente en Ventas existen en Clientes
SELECT 
    'Clientes huérfanos en Ventas' as verificacion,
    COUNT(*) as problemas
FROM Ventas v
LEFT JOIN Clientes c ON v.id_cliente = c.id_cliente
WHERE c.id_cliente IS NULL;

-- Verificar que todos los id_producto en Detalles_Ventas existen en Productos
SELECT 
    'Productos huérfanos en Detalles_Ventas' as verificacion,
    COUNT(*) as problemas
FROM Detalles_Ventas dv
LEFT JOIN Productos p ON dv.id_producto = p.id_producto
WHERE p.id_producto IS NULL;

-- Verificar inconsistencias en nombres
SELECT 
    'Clientes con nombres inconsistentes' as verificacion,
    COUNT(*) as problemas
FROM Ventas v
JOIN Clientes c ON v.id_cliente = c.id_cliente
WHERE v.nombre_cliente != c.nombre_cliente;

SELECT 
    'Productos con nombres inconsistentes' as verificacion,
    COUNT(*) as problemas  
FROM Detalles_Ventas dv
JOIN Productos p ON dv.id_producto = p.id_producto
WHERE dv.nombre_producto != p.nombre_producto;

-- =============================================================================
-- 3. MIGRACIÓN - ELIMINAR COLUMNAS REDUNDANTES
-- =============================================================================

-- Deshabilitar restricciones temporalmente (si es necesario)
-- SET FOREIGN_KEY_CHECKS = 0;

-- Eliminar columnas redundantes de VENTAS
ALTER TABLE Ventas 
DROP COLUMN nombre_cliente,
DROP COLUMN email;

-- Eliminar columnas redundantes de DETALLES_VENTAS  
ALTER TABLE Detalles_Ventas
DROP COLUMN nombre_producto;

-- Habilitar restricciones nuevamente
-- SET FOREIGN_KEY_CHECKS = 1;

-- Verificar estructura nueva
DESCRIBE Ventas;
DESCRIBE Detalles_Ventas;

-- =============================================================================
-- 4. CREAR VISTAS PARA MANTENER COMPATIBILIDAD
-- =============================================================================

-- Vista para Ventas con datos actualizados de Clientes
CREATE OR REPLACE VIEW Ventas_Completas AS
SELECT 
    v.id_venta,
    v.fecha,
    v.id_cliente,
    c.nombre_cliente,
    c.email,
    c.ciudad,
    v.medio_pago
FROM Ventas v
JOIN Clientes c ON v.id_cliente = c.id_cliente;

-- Vista para Detalles_Ventas con datos actualizados de Productos
CREATE OR REPLACE VIEW Detalles_Ventas_Completos AS
SELECT 
    dv.id_detalle,
    dv.id_venta,
    dv.id_producto,
    p.nombre_producto,
    p.categoria,
    dv.cantidad,
    dv.precio_unitario,
    dv.importe
FROM Detalles_Ventas dv
JOIN Productos p ON dv.id_producto = p.id_producto;

-- Vista maestra para análisis
CREATE OR REPLACE VIEW Analisis_Ventas_Completo AS
SELECT 
    vc.id_venta,
    vc.fecha,
    vc.id_cliente,
    vc.nombre_cliente,
    vc.email,
    vc.ciudad,
    vc.medio_pago,
    dvc.id_detalle,
    dvc.id_producto,
    dvc.nombre_producto,
    dvc.categoria,
    dvc.cantidad,
    dvc.precio_unitario,
    dvc.importe
FROM Ventas_Completas vc
JOIN Detalles_Ventas_Completos dvc ON vc.id_venta = dvc.id_venta;

-- Verificar vistas
SELECT 'Ventas_Completas' as vista, COUNT(*) as registros FROM Ventas_Completas
UNION ALL
SELECT 'Detalles_Ventas_Completos', COUNT(*) FROM Detalles_Ventas_Completos
UNION ALL  
SELECT 'Analisis_Ventas_Completo', COUNT(*) FROM Analisis_Ventas_Completo;

-- =============================================================================
-- 5. VERIFICACIÓN POST-MIGRACIÓN
-- =============================================================================

-- Verificar que todo funciona correctamente
SELECT 
    'POST-MIGRACIÓN - Registros totales' as verificacion,
    (SELECT COUNT(*) FROM Ventas) as ventas,
    (SELECT COUNT(*) FROM Detalles_Ventas) as detalles,
    (SELECT COUNT(*) FROM Ventas_Completas) as ventas_completas,
    (SELECT COUNT(*) FROM Detalles_Ventas_Completos) as detalles_completos;

-- Ejemplo de consulta con la nueva estructura
SELECT 
    vc.id_venta,
    vc.fecha,
    vc.nombre_cliente,
    vc.ciudad,
    vc.medio_pago,
    dvc.nombre_producto,
    dvc.categoria,
    dvc.cantidad,
    dvc.importe
FROM Ventas_Completas vc
JOIN Detalles_Ventas_Completos dvc ON vc.id_venta = dvc.id_venta
WHERE vc.id_venta = 1;

-- Mostrar diferencias de almacenamiento (estimado)
SELECT 
    'COMPARACIÓN ALMACENAMIENTO' as metrica,
    'ANTES' as estado,
    (SELECT COUNT(*) * 150 FROM backup_ventas) +  -- Estimado bytes por registro
    (SELECT COUNT(*) * 100 FROM backup_detalles_ventas) as bytes_estimados
UNION ALL
SELECT 
    'COMPARACIÓN ALMACENAMIENTO',
    'DESPUÉS', 
    (SELECT COUNT(*) * 50 FROM Ventas) +          -- Menos columnas = menos bytes
    (SELECT COUNT(*) * 80 FROM Detalles_Ventas);

-- =============================================================================
-- 6. SCRIPT DE ROLLBACK (OPCIONAL)
-- =============================================================================

/*
-- PARA REVERTIR LOS CAMBIOS:

-- 1. Restaurar columnas eliminadas
ALTER TABLE Ventas 
ADD COLUMN nombre_cliente VARCHAR(100),
ADD COLUMN email VARCHAR(100);

ALTER TABLE Detalles_Ventas
ADD COLUMN nombre_producto VARCHAR(100);

-- 2. Restaurar datos desde backup
UPDATE Ventas v 
JOIN backup_ventas b ON v.id_venta = b.id_venta
SET v.nombre_cliente = b.nombre_cliente,
    v.email = b.email;

UPDATE Detalles_Ventas dv
JOIN backup_detalles_ventas b ON dv.id_detalle = b.id_detalle  
SET dv.nombre_producto = b.nombre_producto;

-- 3. Eliminar vistas
DROP VIEW IF EXISTS Ventas_Completas;
DROP VIEW IF EXISTS Detalles_Ventas_Completos;
DROP VIEW IF EXISTS Analisis_Ventas_Completo;
*/

