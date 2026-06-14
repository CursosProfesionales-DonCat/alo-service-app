--
-- PostgreSQL database dump
--

\restrict M4rBxVP4REkS5syVsFPJ68x5iM2557Ri9CGjCgkMy7RPqpqfFs8TTi17KcqMPdf

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-05-16 22:48:18

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 230 (class 1259 OID 16470)
-- Name: auditoria_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auditoria_logs (
    id_log integer NOT NULL,
    id_usuario integer NOT NULL,
    accion character varying(255) NOT NULL,
    modulo character varying(100) NOT NULL,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.auditoria_logs OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16469)
-- Name: auditoria_logs_id_log_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auditoria_logs_id_log_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auditoria_logs_id_log_seq OWNER TO postgres;

--
-- TOC entry 5146 (class 0 OID 0)
-- Dependencies: 229
-- Name: auditoria_logs_id_log_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auditoria_logs_id_log_seq OWNED BY public.auditoria_logs.id_log;


--
-- TOC entry 222 (class 1259 OID 16401)
-- Name: clientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clientes (
    id_cliente integer NOT NULL,
    razon_social character varying(150) NOT NULL,
    ruc character varying(20) NOT NULL,
    contacto character varying(100),
    tipo_cliente character varying(50)
);


ALTER TABLE public.clientes OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16400)
-- Name: clientes_id_cliente_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clientes_id_cliente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clientes_id_cliente_seq OWNER TO postgres;

--
-- TOC entry 5147 (class 0 OID 0)
-- Dependencies: 221
-- Name: clientes_id_cliente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clientes_id_cliente_seq OWNED BY public.clientes.id_cliente;


--
-- TOC entry 240 (class 1259 OID 16566)
-- Name: detalle_ot_repuestos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.detalle_ot_repuestos (
    id_detalle integer NOT NULL,
    id_ot integer NOT NULL,
    id_repuesto integer NOT NULL,
    cantidad integer NOT NULL
);


ALTER TABLE public.detalle_ot_repuestos OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 16565)
-- Name: detalle_ot_repuestos_id_detalle_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.detalle_ot_repuestos_id_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.detalle_ot_repuestos_id_detalle_seq OWNER TO postgres;

--
-- TOC entry 5148 (class 0 OID 0)
-- Dependencies: 239
-- Name: detalle_ot_repuestos_id_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.detalle_ot_repuestos_id_detalle_seq OWNED BY public.detalle_ot_repuestos.id_detalle;


--
-- TOC entry 228 (class 1259 OID 16451)
-- Name: equipos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.equipos (
    id_equipo integer NOT NULL,
    codigo_patrimonial character varying(50) NOT NULL,
    nombre character varying(100) NOT NULL,
    tipo character varying(100),
    estado character varying(50) DEFAULT 'Operativo'::character varying,
    fecha_adquisicion date,
    horas_uso integer DEFAULT 0,
    id_cliente integer
);


ALTER TABLE public.equipos OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16450)
-- Name: equipos_id_equipo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.equipos_id_equipo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.equipos_id_equipo_seq OWNER TO postgres;

--
-- TOC entry 5149 (class 0 OID 0)
-- Dependencies: 227
-- Name: equipos_id_equipo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.equipos_id_equipo_seq OWNED BY public.equipos.id_equipo;


--
-- TOC entry 232 (class 1259 OID 16487)
-- Name: fallas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fallas (
    id_falla integer NOT NULL,
    id_equipo integer NOT NULL,
    fecha_falla timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    tipo_falla character varying(100),
    componente_afectado character varying(100),
    descripcion text
);


ALTER TABLE public.fallas OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16486)
-- Name: fallas_id_falla_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fallas_id_falla_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fallas_id_falla_seq OWNER TO postgres;

--
-- TOC entry 5150 (class 0 OID 0)
-- Dependencies: 231
-- Name: fallas_id_falla_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fallas_id_falla_seq OWNED BY public.fallas.id_falla;


--
-- TOC entry 234 (class 1259 OID 16504)
-- Name: metricas_modelo_ml; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metricas_modelo_ml (
    id_metrica integer NOT NULL,
    fecha_entrenamiento timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    precision_score numeric(5,4) NOT NULL,
    recall_score numeric(5,4) NOT NULL,
    f1_score numeric(5,4) NOT NULL,
    version_modelo character varying(50) NOT NULL,
    parametros text
);


ALTER TABLE public.metricas_modelo_ml OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16503)
-- Name: metricas_modelo_ml_id_metrica_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.metricas_modelo_ml_id_metrica_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.metricas_modelo_ml_id_metrica_seq OWNER TO postgres;

--
-- TOC entry 5151 (class 0 OID 0)
-- Dependencies: 233
-- Name: metricas_modelo_ml_id_metrica_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.metricas_modelo_ml_id_metrica_seq OWNED BY public.metricas_modelo_ml.id_metrica;


--
-- TOC entry 238 (class 1259 OID 16536)
-- Name: ordenes_trabajo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ordenes_trabajo (
    id_ot integer NOT NULL,
    id_equipo integer NOT NULL,
    id_tecnico integer NOT NULL,
    id_prediccion integer,
    tipo_mantenimiento character varying(50) NOT NULL,
    estado character varying(50) DEFAULT 'Pendiente'::character varying,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    diagnostico text,
    fecha_cierre timestamp without time zone
);


ALTER TABLE public.ordenes_trabajo OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16535)
-- Name: ordenes_trabajo_id_ot_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ordenes_trabajo_id_ot_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ordenes_trabajo_id_ot_seq OWNER TO postgres;

--
-- TOC entry 5152 (class 0 OID 0)
-- Dependencies: 237
-- Name: ordenes_trabajo_id_ot_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ordenes_trabajo_id_ot_seq OWNED BY public.ordenes_trabajo.id_ot;


--
-- TOC entry 236 (class 1259 OID 16519)
-- Name: predicciones_fallas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.predicciones_fallas (
    id_prediccion integer NOT NULL,
    id_equipo integer NOT NULL,
    fecha_analisis timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    probabilidad_falla numeric(5,2) NOT NULL,
    componente_riesgo character varying(100),
    estado_alerta character varying(50) DEFAULT 'Generada'::character varying
);


ALTER TABLE public.predicciones_fallas OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16518)
-- Name: predicciones_fallas_id_prediccion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.predicciones_fallas_id_prediccion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.predicciones_fallas_id_prediccion_seq OWNER TO postgres;

--
-- TOC entry 5153 (class 0 OID 0)
-- Dependencies: 235
-- Name: predicciones_fallas_id_prediccion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.predicciones_fallas_id_prediccion_seq OWNED BY public.predicciones_fallas.id_prediccion;


--
-- TOC entry 224 (class 1259 OID 16413)
-- Name: repuestos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.repuestos (
    id_repuesto integer NOT NULL,
    codigo_pieza character varying(50) NOT NULL,
    nombre character varying(100) NOT NULL,
    stock_actual integer DEFAULT 0,
    stock_minimo integer DEFAULT 5
);


ALTER TABLE public.repuestos OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16412)
-- Name: repuestos_id_repuesto_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.repuestos_id_repuesto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.repuestos_id_repuesto_seq OWNER TO postgres;

--
-- TOC entry 5154 (class 0 OID 0)
-- Dependencies: 223
-- Name: repuestos_id_repuesto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.repuestos_id_repuesto_seq OWNED BY public.repuestos.id_repuesto;


--
-- TOC entry 220 (class 1259 OID 16390)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id_rol integer NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion character varying(255)
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16389)
-- Name: roles_id_rol_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_rol_seq OWNER TO postgres;

--
-- TOC entry 5155 (class 0 OID 0)
-- Dependencies: 219
-- Name: roles_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_rol_seq OWNED BY public.roles.id_rol;


--
-- TOC entry 226 (class 1259 OID 16427)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    id_rol integer NOT NULL,
    nombres character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    correo character varying(150) NOT NULL,
    password_hash character varying(255) NOT NULL,
    estado boolean DEFAULT true,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16426)
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_usuario_seq OWNER TO postgres;

--
-- TOC entry 5156 (class 0 OID 0)
-- Dependencies: 225
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- TOC entry 4917 (class 2604 OID 16473)
-- Name: auditoria_logs id_log; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria_logs ALTER COLUMN id_log SET DEFAULT nextval('public.auditoria_logs_id_log_seq'::regclass);


--
-- TOC entry 4907 (class 2604 OID 16404)
-- Name: clientes id_cliente; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes ALTER COLUMN id_cliente SET DEFAULT nextval('public.clientes_id_cliente_seq'::regclass);


--
-- TOC entry 4929 (class 2604 OID 16569)
-- Name: detalle_ot_repuestos id_detalle; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_ot_repuestos ALTER COLUMN id_detalle SET DEFAULT nextval('public.detalle_ot_repuestos_id_detalle_seq'::regclass);


--
-- TOC entry 4914 (class 2604 OID 16454)
-- Name: equipos id_equipo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipos ALTER COLUMN id_equipo SET DEFAULT nextval('public.equipos_id_equipo_seq'::regclass);


--
-- TOC entry 4919 (class 2604 OID 16490)
-- Name: fallas id_falla; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fallas ALTER COLUMN id_falla SET DEFAULT nextval('public.fallas_id_falla_seq'::regclass);


--
-- TOC entry 4921 (class 2604 OID 16507)
-- Name: metricas_modelo_ml id_metrica; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metricas_modelo_ml ALTER COLUMN id_metrica SET DEFAULT nextval('public.metricas_modelo_ml_id_metrica_seq'::regclass);


--
-- TOC entry 4926 (class 2604 OID 16539)
-- Name: ordenes_trabajo id_ot; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordenes_trabajo ALTER COLUMN id_ot SET DEFAULT nextval('public.ordenes_trabajo_id_ot_seq'::regclass);


--
-- TOC entry 4923 (class 2604 OID 16522)
-- Name: predicciones_fallas id_prediccion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.predicciones_fallas ALTER COLUMN id_prediccion SET DEFAULT nextval('public.predicciones_fallas_id_prediccion_seq'::regclass);


--
-- TOC entry 4908 (class 2604 OID 16416)
-- Name: repuestos id_repuesto; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repuestos ALTER COLUMN id_repuesto SET DEFAULT nextval('public.repuestos_id_repuesto_seq'::regclass);


--
-- TOC entry 4906 (class 2604 OID 16393)
-- Name: roles id_rol; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id_rol SET DEFAULT nextval('public.roles_id_rol_seq'::regclass);


--
-- TOC entry 4911 (class 2604 OID 16430)
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- TOC entry 5130 (class 0 OID 16470)
-- Dependencies: 230
-- Data for Name: auditoria_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auditoria_logs (id_log, id_usuario, accion, modulo, fecha_registro) FROM stdin;
\.


--
-- TOC entry 5122 (class 0 OID 16401)
-- Dependencies: 222
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clientes (id_cliente, razon_social, ruc, contacto, tipo_cliente) FROM stdin;
1	ejemplo	121232132	hyb	Externo
\.


--
-- TOC entry 5140 (class 0 OID 16566)
-- Dependencies: 240
-- Data for Name: detalle_ot_repuestos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.detalle_ot_repuestos (id_detalle, id_ot, id_repuesto, cantidad) FROM stdin;
1	2	1	1
2	3	4	1
\.


--
-- TOC entry 5128 (class 0 OID 16451)
-- Dependencies: 228
-- Data for Name: equipos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.equipos (id_equipo, codigo_patrimonial, nombre, tipo, estado, fecha_adquisicion, horas_uso, id_cliente) FROM stdin;
1	ALO-01	TIJERA	\N	Operativo	2026-05-16	155	\N
2	ALO-012	doncat	doncat	Operativo	\N	12000	1
3	ALO-03	junjun1	Articulo	Operativo	\N	15000	1
\.


--
-- TOC entry 5132 (class 0 OID 16487)
-- Dependencies: 232
-- Data for Name: fallas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fallas (id_falla, id_equipo, fecha_falla, tipo_falla, componente_afectado, descripcion) FROM stdin;
\.


--
-- TOC entry 5134 (class 0 OID 16504)
-- Dependencies: 234
-- Data for Name: metricas_modelo_ml; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.metricas_modelo_ml (id_metrica, fecha_entrenamiento, precision_score, recall_score, f1_score, version_modelo, parametros) FROM stdin;
1	2026-05-16 10:14:12	0.9240	0.9100	0.9150	v1.0 (Random Forest)	n_estimators=100, max_depth=10
2	2026-05-16 10:15:55	0.9482	0.9467	0.9475	v2.0 (Random Forest Optimizado)	n_estimators=150, auto_balance=True
3	2026-05-16 22:41:18.148014	0.9265	0.9028	0.9145	v3.0 (Random Forest Optimizado)	n_estimators=150, auto_balance=True
\.


--
-- TOC entry 5138 (class 0 OID 16536)
-- Dependencies: 238
-- Data for Name: ordenes_trabajo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ordenes_trabajo (id_ot, id_equipo, id_tecnico, id_prediccion, tipo_mantenimiento, estado, fecha_creacion, diagnostico, fecha_cierre) FROM stdin;
1	1	2	\N	Correctivo	Cerrada	2026-05-16 01:19:48	falla	2026-05-16 09:58:41
2	2	2	\N	Correctivo	Cerrada	2026-05-16 11:09:46	fallas	2026-05-16 11:10:56
3	3	2	\N	Correctivo	Cerrada	2026-05-16 22:40:36.566624	falla 2	2026-05-16 22:42:50
\.


--
-- TOC entry 5136 (class 0 OID 16519)
-- Dependencies: 236
-- Data for Name: predicciones_fallas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.predicciones_fallas (id_prediccion, id_equipo, fecha_analisis, probabilidad_falla, componente_riesgo, estado_alerta) FROM stdin;
\.


--
-- TOC entry 5124 (class 0 OID 16413)
-- Dependencies: 224
-- Data for Name: repuestos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.repuestos (id_repuesto, codigo_pieza, nombre, stock_actual, stock_minimo) FROM stdin;
1	FLT-001	Filtro Hidraulico	100	5
4	FLT-002	Filtro a	3	5
\.


--
-- TOC entry 5120 (class 0 OID 16390)
-- Dependencies: 220
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id_rol, nombre, descripcion) FROM stdin;
1	Administrador	Control total del sistema
2	Gerente	Acceso a reportes y métricas ML
3	Supervisor	Gestión de equipos y revisión de alertas
4	Técnico	Atención de Órdenes de Trabajo
5	Enc. almacén	Gestión de repuestos
6	Analista	Revisión de eficiencia del modelo ML
\.


--
-- TOC entry 5126 (class 0 OID 16427)
-- Dependencies: 226
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id_usuario, id_rol, nombres, apellidos, correo, password_hash, estado, fecha_creacion) FROM stdin;
1	1	Carlos	Li Chocano	admin@alo.com	$2b$12$br91Qtu9czHFKp6gurvtgu/XU.OJFYE34K8ozz7Tgqd8l.cIYOSSK	t	2026-05-15 23:27:35
2	4	JUAN	TECNICO	tecnico@gmail.com	$2b$12$A7Yr9cpBvExTraCRpU6S9e1BgAN3riQWLfXvbETYEX/.hYPNzK/72	t	2026-05-16 01:19:33
3	5	Axel		almacen@gmail.com	$2b$12$wTskb7QPUXRGBkKpJoWKYOQpiBUCQraZgFzHszPS/bBHi20fwEEmS	t	2026-05-16 20:29:53
4	3	Carlos		supervisor@gmail.com	$2b$12$YFP3F.vgLjSVywro6VFP7eqY.OQWvE.YBl/WHplmfhH1SRuFH2s9e	t	2026-05-16 20:48:40
\.


--
-- TOC entry 5157 (class 0 OID 0)
-- Dependencies: 229
-- Name: auditoria_logs_id_log_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auditoria_logs_id_log_seq', 1, false);


--
-- TOC entry 5158 (class 0 OID 0)
-- Dependencies: 221
-- Name: clientes_id_cliente_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clientes_id_cliente_seq', 1, true);


--
-- TOC entry 5159 (class 0 OID 0)
-- Dependencies: 239
-- Name: detalle_ot_repuestos_id_detalle_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.detalle_ot_repuestos_id_detalle_seq', 2, true);


--
-- TOC entry 5160 (class 0 OID 0)
-- Dependencies: 227
-- Name: equipos_id_equipo_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.equipos_id_equipo_seq', 3, true);


--
-- TOC entry 5161 (class 0 OID 0)
-- Dependencies: 231
-- Name: fallas_id_falla_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fallas_id_falla_seq', 1, false);


--
-- TOC entry 5162 (class 0 OID 0)
-- Dependencies: 233
-- Name: metricas_modelo_ml_id_metrica_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.metricas_modelo_ml_id_metrica_seq', 3, true);


--
-- TOC entry 5163 (class 0 OID 0)
-- Dependencies: 237
-- Name: ordenes_trabajo_id_ot_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ordenes_trabajo_id_ot_seq', 3, true);


--
-- TOC entry 5164 (class 0 OID 0)
-- Dependencies: 235
-- Name: predicciones_fallas_id_prediccion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.predicciones_fallas_id_prediccion_seq', 1, false);


--
-- TOC entry 5165 (class 0 OID 0)
-- Dependencies: 223
-- Name: repuestos_id_repuesto_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.repuestos_id_repuesto_seq', 4, true);


--
-- TOC entry 5166 (class 0 OID 0)
-- Dependencies: 219
-- Name: roles_id_rol_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_rol_seq', 6, true);


--
-- TOC entry 5167 (class 0 OID 0)
-- Dependencies: 225
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_usuario_seq', 4, true);


--
-- TOC entry 4951 (class 2606 OID 16480)
-- Name: auditoria_logs auditoria_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria_logs
    ADD CONSTRAINT auditoria_logs_pkey PRIMARY KEY (id_log);


--
-- TOC entry 4935 (class 2606 OID 16409)
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (id_cliente);


--
-- TOC entry 4937 (class 2606 OID 16411)
-- Name: clientes clientes_ruc_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_ruc_key UNIQUE (ruc);


--
-- TOC entry 4961 (class 2606 OID 16575)
-- Name: detalle_ot_repuestos detalle_ot_repuestos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_ot_repuestos
    ADD CONSTRAINT detalle_ot_repuestos_pkey PRIMARY KEY (id_detalle);


--
-- TOC entry 4947 (class 2606 OID 16463)
-- Name: equipos equipos_codigo_patrimonial_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipos
    ADD CONSTRAINT equipos_codigo_patrimonial_key UNIQUE (codigo_patrimonial);


--
-- TOC entry 4949 (class 2606 OID 16461)
-- Name: equipos equipos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipos
    ADD CONSTRAINT equipos_pkey PRIMARY KEY (id_equipo);


--
-- TOC entry 4953 (class 2606 OID 16497)
-- Name: fallas fallas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fallas
    ADD CONSTRAINT fallas_pkey PRIMARY KEY (id_falla);


--
-- TOC entry 4955 (class 2606 OID 16517)
-- Name: metricas_modelo_ml metricas_modelo_ml_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metricas_modelo_ml
    ADD CONSTRAINT metricas_modelo_ml_pkey PRIMARY KEY (id_metrica);


--
-- TOC entry 4959 (class 2606 OID 16549)
-- Name: ordenes_trabajo ordenes_trabajo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordenes_trabajo
    ADD CONSTRAINT ordenes_trabajo_pkey PRIMARY KEY (id_ot);


--
-- TOC entry 4957 (class 2606 OID 16529)
-- Name: predicciones_fallas predicciones_fallas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.predicciones_fallas
    ADD CONSTRAINT predicciones_fallas_pkey PRIMARY KEY (id_prediccion);


--
-- TOC entry 4939 (class 2606 OID 16425)
-- Name: repuestos repuestos_codigo_pieza_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repuestos
    ADD CONSTRAINT repuestos_codigo_pieza_key UNIQUE (codigo_pieza);


--
-- TOC entry 4941 (class 2606 OID 16423)
-- Name: repuestos repuestos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repuestos
    ADD CONSTRAINT repuestos_pkey PRIMARY KEY (id_repuesto);


--
-- TOC entry 4931 (class 2606 OID 16399)
-- Name: roles roles_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_nombre_key UNIQUE (nombre);


--
-- TOC entry 4933 (class 2606 OID 16397)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id_rol);


--
-- TOC entry 4943 (class 2606 OID 16444)
-- Name: usuarios usuarios_correo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_key UNIQUE (correo);


--
-- TOC entry 4945 (class 2606 OID 16442)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 4964 (class 2606 OID 16481)
-- Name: auditoria_logs auditoria_logs_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria_logs
    ADD CONSTRAINT auditoria_logs_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- TOC entry 4970 (class 2606 OID 16576)
-- Name: detalle_ot_repuestos detalle_ot_repuestos_id_ot_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_ot_repuestos
    ADD CONSTRAINT detalle_ot_repuestos_id_ot_fkey FOREIGN KEY (id_ot) REFERENCES public.ordenes_trabajo(id_ot);


--
-- TOC entry 4971 (class 2606 OID 16581)
-- Name: detalle_ot_repuestos detalle_ot_repuestos_id_repuesto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_ot_repuestos
    ADD CONSTRAINT detalle_ot_repuestos_id_repuesto_fkey FOREIGN KEY (id_repuesto) REFERENCES public.repuestos(id_repuesto);


--
-- TOC entry 4963 (class 2606 OID 16464)
-- Name: equipos equipos_id_cliente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipos
    ADD CONSTRAINT equipos_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES public.clientes(id_cliente) ON DELETE SET NULL;


--
-- TOC entry 4965 (class 2606 OID 16498)
-- Name: fallas fallas_id_equipo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fallas
    ADD CONSTRAINT fallas_id_equipo_fkey FOREIGN KEY (id_equipo) REFERENCES public.equipos(id_equipo);


--
-- TOC entry 4967 (class 2606 OID 16550)
-- Name: ordenes_trabajo ordenes_trabajo_id_equipo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordenes_trabajo
    ADD CONSTRAINT ordenes_trabajo_id_equipo_fkey FOREIGN KEY (id_equipo) REFERENCES public.equipos(id_equipo);


--
-- TOC entry 4968 (class 2606 OID 16560)
-- Name: ordenes_trabajo ordenes_trabajo_id_prediccion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordenes_trabajo
    ADD CONSTRAINT ordenes_trabajo_id_prediccion_fkey FOREIGN KEY (id_prediccion) REFERENCES public.predicciones_fallas(id_prediccion);


--
-- TOC entry 4969 (class 2606 OID 16555)
-- Name: ordenes_trabajo ordenes_trabajo_id_tecnico_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordenes_trabajo
    ADD CONSTRAINT ordenes_trabajo_id_tecnico_fkey FOREIGN KEY (id_tecnico) REFERENCES public.usuarios(id_usuario);


--
-- TOC entry 4966 (class 2606 OID 16530)
-- Name: predicciones_fallas predicciones_fallas_id_equipo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.predicciones_fallas
    ADD CONSTRAINT predicciones_fallas_id_equipo_fkey FOREIGN KEY (id_equipo) REFERENCES public.equipos(id_equipo);


--
-- TOC entry 4962 (class 2606 OID 16445)
-- Name: usuarios usuarios_id_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES public.roles(id_rol);


-- Completed on 2026-05-16 22:48:18

--
-- PostgreSQL database dump complete
--

\unrestrict M4rBxVP4REkS5syVsFPJ68x5iM2557Ri9CGjCgkMy7RPqpqfFs8TTi17KcqMPdf

