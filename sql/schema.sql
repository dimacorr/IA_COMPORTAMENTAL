-- ===========================================
-- Transacciones
-- ===========================================

CREATE TABLE transacciones (
id BIGSERIAL PRIMARY KEY,            -- Identificador único interno de la tabla. No aporta información de fraude directamente, pero sirve para referenciar registros.
client_id TEXT NOT NULL,             -- Identifica al cliente. Útil para agrupar transacciones y analizar comportamientos repetitivos solo numerico.
transaction_id TEXT NOT NULL UNIQUE, -- Identificador único de la transacción. Importante para trazabilidad.
amount NUMERIC(12,2),				 -- Monto de la transacción. Muy relevante: montos inusuales pueden indicar fraude.
currency TEXT,						 -- Moneda de la transacción. Ayuda a detectar inconsistencias o transacciones en monedas raras.
timestamp TIMESTAMPTZ NOT NULL,      -- Fecha y hora de la transacción. Útil para detectar patrones horarios sospechosos o transacciones rápidas consecutivas.
status TEXT,						 -- Estado de la transacción (approved, declined, alert). Fundamental: la etiqueta principal para entrenar modelos de fraude.
merchant_id TEXT,                    -- Identificador del comercio. Permite identificar comercios de alto riesgo o recurrentes en fraudes.
channel TEXT,                        -- Canal de la transacción (online, in_store). Diferentes riesgos por canal: online es más propenso a fraude.
card_present BOOLEAN,                -- Booleano si la tarjeta estuvo presente físicamente. Transacciones sin tarjeta presente suelen ser más riesgosas.
card_type TEXT,                      -- Tipo de tarjeta (VISA, MASTERCARD, AMEX). Puede ayudar a detectar patrones de fraude específicos de cada tipo.
ip_address TEXT,					 -- Dirección IP del cliente. Ayuda a identificar transacciones desde IP sospechosas o múltiples cuentas desde la misma IP.
city TEXT, 							 -- Ciudad del cliente. Para validar coherencia geográfica.
metadata JSONB                       -- JSONB con información adicional libre (IP, ubicación, navegador, etc.). Muy útil para análisis avanzado.
);

-- ===========================================
-- Envios_cliente
-- ===========================================

CREATE TABLE envios_cliente (
id BIGSERIAL PRIMARY KEY,
client_id TEXT NOT NULL,
transaction_id TEXT, -- FK a transacciones.transaction_id (opcional)
message_id TEXT,
sent_at TIMESTAMPTZ NOT NULL,
delivered_at TIMESTAMPTZ,
response_at TIMESTAMPTZ, -- cuando el cliente respondió (NULL si no)
response_text TEXT, -- texto crudo de la respuesta
response_class TEXT, -- 'confirm', 'deny', 'no_answer', 'other'
channel TEXT, -- 'whatsapp', 'sms', etc.
attempt INT DEFAULT 1,
template_id TEXT,
metadata JSONB
);


-- Índices sugeridos
CREATE INDEX idx_envios_client_id ON envios_cliente(client_id);
CREATE INDEX idx_envios_txn_id ON envios_cliente(transaction_id);
CREATE INDEX idx_envios_sent_at ON envios_cliente(sent_at);

-- ===========================================
-- Inserts de Transacciones
-- ===========================================

INSERT INTO transacciones (
    id, client_id, transaction_id, amount, currency, timestamp, status,
    merchant_id, channel, card_present, card_type, ip_address,
    city, metadata
)
VALUES
(1, '201', 'TXN201', 150000, 'COP', '2025-08-01 10:30:00', 'approved',
 'M001', 'WEB', false, 'VISA', '192.168.0.1', 'Bogotá', '{"device":"Chrome"}'),
(2, '201', 'TXN202', 180000, 'COP', '2025-08-02 15:45:00', 'approved',
 'M002', 'APP', true, 'MASTERCARD', '192.168.0.2', 'Medellín', '{"device":"iOS"}'),
(3, '201', 'TXN203', 210000, 'COP', '2025-08-03 09:10:00', 'approved',
 'M003', 'POS', true, 'VISA', '192.168.0.3', 'Cali', '{"device":"POS"}'),
(4, '201', 'TXN204', 95000, 'COP', '2025-08-04 14:25:00', 'approved',
 'M004', 'WEB', false, 'AMEX', '192.168.0.4', 'Cartagena', '{"device":"Edge"}'),
(5, '202', 'TXN205', 300000, 'COP', '2025-08-05 12:40:00', 'alert',
 'M005', 'WEB', false, 'VISA', '192.168.1.1', 'Bogotá', '{"device":"Chrome"}'),
(6, '202', 'TXN206', 270000, 'COP', '2025-08-06 16:15:00', 'declined',
 'M006', 'APP', true, 'MASTERCARD', '192.168.1.2', 'Medellín', '{"device":"Android"}'),
(7, '202', 'TXN207', 500000, 'COP', '2025-08-07 11:00:00', 'alert',
 'M007', 'POS', true, 'VISA', '192.168.1.3', 'Cali', '{"device":"POS"}'),
(8, '202', 'TXN208', 120000, 'COP', '2025-08-08 19:20:00', 'declined',
 'M008', 'WEB', false, 'AMEX', '192.168.1.4', 'Barranquilla', '{"device":"Safari"}'),
(9, '203', 'TXN209', 75000, 'COP', '2025-08-09 08:30:00', 'alert',
 'M009', 'WEB', false, 'VISA', '192.168.2.1', 'Cali', '{"device":"Linux"}'),
(10, '203', 'TXN210', 89000, 'COP', '2025-08-10 18:00:00', 'declined',
 'M010', 'APP', true, 'MASTERCARD', '192.168.2.2', 'Bogotá', '{"device":"Android"}'),
(11, '203', 'TXN211', 130000, 'COP', '2025-08-11 20:10:00', 'alert',
 'M011', 'POS', true, 'VISA', '192.168.2.3', 'Medellín', '{"device":"POS"}'),
(12, '203', 'TXN212', 64000, 'COP', '2025-08-12 21:45:00', 'declined',
 'M012', 'WEB', false, 'AMEX', '192.168.2.4', 'Cartagena', '{"device":"Edge"}'),
(13, '204', 'TXN213', 220000, 'COP', '2025-08-13 07:15:00', 'approved',
 'M013', 'APP', true, 'VISA', '10.0.4.1', 'Bogotá', '{"device":"Android"}'),
(14, '204', 'TXN214', 135000, 'COP', '2025-08-14 10:55:00', 'alert',
 'M014', 'WEB', false, 'MASTERCARD', '10.0.4.2', 'Medellín', '{"device":"Windows"}'),
(15, '204', 'TXN215', 98000, 'COP', '2025-08-15 12:40:00', 'declined',
 'M015', 'POS', true, 'VISA', '10.0.4.3', 'Cali', '{"device":"POS"}'),
(16, '204', 'TXN216', 360000, 'COP', '2025-08-16 19:20:00', 'approved',
 'M016', 'APP', true, 'AMEX', '10.0.4.4', 'Cartagena', '{"device":"iOS"}'),
(17, '205', 'TXN217', 275000, 'COP', '2025-08-17 09:45:00', 'approved',
 'M017', 'WEB', false, 'VISA', '10.0.5.1', 'Barranquilla', '{"device":"Chrome"}'),
(18, '205', 'TXN218', 445000, 'COP', '2025-08-18 15:30:00', 'alert',
 'M018', 'POS', true, 'MASTERCARD', '10.0.5.2', 'Bogotá', '{"device":"POS"}'),
(19, '205', 'TXN219', 160000, 'COP', '2025-08-19 13:10:00', 'declined',
 'M019', 'APP', true, 'VISA', '10.0.5.3', 'Medellín', '{"device":"Android"}'),
(20, '205', 'TXN220', 82000, 'COP', '2025-08-20 20:05:00', 'approved',
 'M020', 'WEB', false, 'AMEX', '10.0.5.4', 'Cali', '{"device":"Linux"}'),
(21, '201', 'TXN221', 125000, 'COP', '2025-08-21 11:25:00', 'approved',
 'M021', 'APP', true, 'VISA', '10.0.1.5', 'Cartagena', '{"device":"iOS"}'),
(22, '201', 'TXN222', 510000, 'COP', '2025-08-22 14:00:00', 'alert',
 'M022', 'POS', true, 'MASTERCARD', '10.0.1.6', 'Bogotá', '{"device":"POS"}'),
(23, '201', 'TXN223', 192000, 'COP', '2025-08-23 16:15:00', 'declined',
 'M023', 'WEB', false, 'VISA', '10.0.1.7', 'Medellín', '{"device":"Edge"}'),
(24, '201', 'TXN224', 76000, 'COP', '2025-08-24 08:20:00', 'approved',
 'M024', 'APP', true, 'AMEX', '10.0.1.8', 'Cali', '{"device":"Android"}'),
(25, '202', 'TXN225', 285000, 'COP', '2025-08-25 10:35:00', 'alert',
 'M025', 'WEB', false, 'VISA', '10.0.2.5', 'Cartagena', '{"device":"Chrome"}'),
(26, '202', 'TXN226', 150000, 'COP', '2025-08-26 18:45:00', 'declined',
 'M026', 'POS', true, 'MASTERCARD', '10.0.2.6', 'Bogotá', '{"device":"POS"}'),
(27, '202', 'TXN227', 395000, 'COP', '2025-08-27 13:55:00', 'approved',
 'M027', 'APP', true, 'VISA', '10.0.2.7', 'Medellín', '{"device":"Android"}'),
(28, '202', 'TXN228', 112000, 'COP', '2025-08-28 21:10:00', 'alert',
 'M028', 'WEB', false, 'AMEX', '10.0.2.8', 'Cali', '{"device":"Linux"}'),
(29, '203', 'TXN229', 98000, 'COP', '2025-08-29 09:05:00', 'declined',
 'M029', 'POS', true, 'VISA', '10.0.3.5', 'Bogotá', '{"device":"POS"}'),
(30, '203', 'TXN230', 210000, 'COP', '2025-08-30 17:30:00', 'approved',
 'M030', 'APP', true, 'MASTERCARD', '10.0.3.6', 'Cartagena', '{"device":"Android"}');

-- ===========================================
-- Inserts de Envíos Cliente
-- ===========================================
INSERT INTO envios_cliente (
    id, client_id, transaction_id, message_id, sent_at,
    delivered_at, response_at, response_text, response_class,
    channel, attempt, template_id, metadata
)
VALUES
(1, '201', 'TXN201', 'MSG201', '2025-08-01 10:31:00', '2025-08-01 10:32:00', '2025-08-01 10:35:00', 'Sí, fui yo', 'confirm', 'whatsapp', 1, 'TPL001', '{"lang":"es","priority":"high"}'),
(2, '201', 'TXN202', 'MSG202', '2025-08-02 15:46:00', '2025-08-02 15:47:00', NULL, NULL, 'no_answer', 'sms', 1, 'TPL002', '{"lang":"es"}'),
(3, '201', 'TXN203', 'MSG203', '2025-08-03 09:11:00', '2025-08-03 09:12:00', '2025-08-03 09:14:00', 'No reconozco', 'deny', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(4, '201', 'TXN204', 'MSG204', '2025-08-04 14:26:00', '2025-08-04 14:28:00', NULL, NULL, 'no_answer', 'email', 1, 'TPL003', '{"lang":"es","device":"Edge"}'),
(5, '202', 'TXN205', 'MSG205', '2025-08-05 12:41:00', '2025-08-05 12:42:00', '2025-08-05 12:45:00', 'Confirmo compra', 'confirm', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(6, '202', 'TXN206', 'MSG206', '2025-08-06 16:16:00', '2025-08-06 16:17:00', '2025-08-06 16:20:00', 'No la hice yo', 'deny', 'sms', 1, 'TPL002', '{"lang":"es"}'),
(7, '202', 'TXN207', 'MSG207', '2025-08-07 11:01:00', '2025-08-07 11:02:00', NULL, NULL, 'no_answer', 'whatsapp', 1, 'TPL001', '{"lang":"es","risk":"high"}'),
(8, '202', 'TXN208', 'MSG208', '2025-08-08 19:21:00', '2025-08-08 19:22:00', '2025-08-08 19:23:00', 'No reconozco este pago', 'deny', 'email', 1, 'TPL003', '{"lang":"es"}'),
(9, '203', 'TXN209', 'MSG209', '2025-08-09 08:31:00', '2025-08-09 08:32:00', NULL, NULL, 'no_answer', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(10, '203', 'TXN210', 'MSG210', '2025-08-10 18:01:00', '2025-08-10 18:02:00', '2025-08-10 18:05:00', 'No reconozco', 'deny', 'sms', 1, 'TPL002', '{"lang":"es"}'),
(11, '204', 'TXN231', 'MSG231', '2025-08-31 10:10:05', '2025-08-31 10:11:00', '2025-08-31 10:15:30', 'Sí, fui yo', 'confirm', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(12, '204', 'TXN232', 'MSG232', '2025-09-01 14:20:10', '2025-09-01 14:21:00', NULL, NULL, 'no_answer', 'sms', 1, 'TPL001', '{"lang":"es"}'),
(13, '204', 'TXN233', 'MSG233', '2025-09-02 16:35:00', '2025-09-02 16:36:00', '2025-09-02 16:37:45', 'No reconozco', 'deny', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(14, '204', 'TXN234', 'MSG234', '2025-09-03 09:25:15', '2025-09-03 09:26:00', NULL, NULL, 'no_answer', 'sms', 1, 'TPL001', '{"lang":"es"}'),
(15, '205', 'TXN235', 'MSG235', '2025-09-04 11:40:05', '2025-09-04 11:41:00', '2025-09-04 11:43:20', 'Todo bien', 'confirm', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(16, '205', 'TXN236', 'MSG236', '2025-09-05 15:10:00', '2025-09-05 15:11:00', '2025-09-05 15:15:00', 'No recuerdo', 'other', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(17, '205', 'TXN237', 'MSG237', '2025-09-06 17:20:05', '2025-09-06 17:21:00', NULL, NULL, 'no_answer', 'sms', 1, 'TPL001', '{"lang":"es"}'),
(18, '205', 'TXN238', 'MSG238', '2025-09-07 13:15:00', '2025-09-07 13:16:00', '2025-09-07 13:18:40', 'Sí, correcto', 'confirm', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(19, '206', 'TXN239', 'MSG239', '2025-09-08 20:25:10', '2025-09-08 20:26:00', '2025-09-08 20:30:00', 'No, no soy yo', 'deny', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(20, '206', 'TXN240', 'MSG240', '2025-09-09 09:05:00', '2025-09-09 09:06:00', NULL, NULL, 'no_answer', 'sms', 1, 'TPL001', '{"lang":"es"}'),
(21, '206', 'TXN241', 'MSG241', '2025-09-10 18:45:00', '2025-09-10 18:46:00', '2025-09-10 18:48:30', 'Sí, lo aprobé', 'confirm', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(22, '206', 'TXN242', 'MSG242', '2025-09-11 10:30:10', '2025-09-11 10:31:00', NULL, NULL, 'no_answer', 'sms', 1, 'TPL001', '{"lang":"es"}'),
(23, '207', 'TXN243', 'MSG243', '2025-09-12 15:40:00', '2025-09-12 15:41:00', '2025-09-12 15:42:50', 'Sí, reconozco', 'confirm', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(24, '207', 'TXN244', 'MSG244', '2025-09-13 12:20:00', '2025-09-13 12:21:00', '2025-09-13 12:24:10', 'No, no soy yo', 'deny', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(25, '207', 'TXN245', 'MSG245', '2025-09-14 14:35:05', '2025-09-14 14:36:00', NULL, NULL, 'no_answer', 'sms', 1, 'TPL001', '{"lang":"es"}'),
(26, '207', 'TXN246', 'MSG246', '2025-09-15 09:10:10', '2025-09-15 09:11:00', '2025-09-15 09:13:30', 'Sí, fui yo', 'confirm', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(27, '208', 'TXN247', 'MSG247', '2025-09-16 11:20:00', '2025-09-16 11:21:00', '2025-09-16 11:25:00', 'No reconozco', 'deny', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(28, '208', 'TXN248', 'MSG248', '2025-09-17 19:05:05', '2025-09-17 19:06:00', NULL, NULL, 'no_answer', 'sms', 1, 'TPL001', '{"lang":"es"}'),
(29, '208', 'TXN249', 'MSG249', '2025-09-18 13:55:00', '2025-09-18 13:56:00', '2025-09-18 13:58:15', 'Ok, entiendo', 'other', 'whatsapp', 1, 'TPL001', '{"lang":"es"}'),
(30, '208', 'TXN250', 'MSG250', '2025-09-19 15:15:00', '2025-09-19 15:16:00', '2025-09-19 15:18:00', 'Sí, correcto', 'confirm', 'whatsapp', 1, 'TPL001', '{"lang":"es"}');