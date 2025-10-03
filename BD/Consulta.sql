-- =============================================================================
-- Formato para exportación
-- =============================================================================

SELECT
    -- Información de Venta
    V.id_venta,
    V.fecha AS fecha_venta,
    V.medio_pago,
    
    -- Información del Cliente
    C.nombre_cliente,
    C.email AS email_cliente,
    C.ciudad AS ciudad_cliente,
    C.fecha_alta AS fecha_registro_cliente,
    
    -- Información del Detalle de Venta
    DV.cantidad,
    DV.precio_unitario AS precio_unitario_venta,
    DV.importe AS subtotal_item,
    
    -- Información del Producto
    P.nombre_producto,
    P.categoria AS categoria_producto,
    P.precio_unitario AS precio_unitario_maestro -- Precio del producto en la tabla 'productos'
FROM
    ventas V
INNER JOIN
    clientes C ON V.id_cliente = C.id_cliente
INNER JOIN
    detalles_ventas DV ON V.id_venta = DV.id_venta
INNER JOIN
    productos P ON DV.id_producto = P.id_producto
ORDER BY
    V.id_venta, DV.id_producto;