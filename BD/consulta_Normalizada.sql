-- =============================================================================
-- Formato optimizado para exportación
-- =============================================================================

SELECT v.*, c.*, dv.*, p.*
FROM Ventas v
JOIN Clientes c ON v.id_cliente = c.id_cliente
JOIN Detalles_Ventas dv ON v.id_venta = dv.id_venta
JOIN Productos p ON dv.id_producto = p.id_producto;
