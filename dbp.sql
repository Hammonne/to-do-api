--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: rrodriguez
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO rrodriguez;

--
-- Name: category; Type: TABLE; Schema: public; Owner: rrodriguez
--

CREATE TABLE public.category (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.category OWNER TO rrodriguez;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: rrodriguez
--

CREATE SEQUENCE public.category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.category_id_seq OWNER TO rrodriguez;

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rrodriguez
--

ALTER SEQUENCE public.category_id_seq OWNED BY public.category.id;


--
-- Name: tablero; Type: TABLE; Schema: public; Owner: rrodriguez
--

CREATE TABLE public.tablero (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying NOT NULL,
    is_admin boolean
);


ALTER TABLE public.tablero OWNER TO rrodriguez;

--
-- Name: tablero_id_seq; Type: SEQUENCE; Schema: public; Owner: rrodriguez
--

CREATE SEQUENCE public.tablero_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tablero_id_seq OWNER TO rrodriguez;

--
-- Name: tablero_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rrodriguez
--

ALTER SEQUENCE public.tablero_id_seq OWNED BY public.tablero.id;


--
-- Name: todo; Type: TABLE; Schema: public; Owner: rrodriguez
--

CREATE TABLE public.todo (
    id integer NOT NULL,
    user_id integer NOT NULL,
    category_id integer NOT NULL,
    description character varying NOT NULL,
    is_done boolean,
    created_date timestamp without time zone,
    deadline timestamp without time zone
);


ALTER TABLE public.todo OWNER TO rrodriguez;

--
-- Name: todo_id_seq; Type: SEQUENCE; Schema: public; Owner: rrodriguez
--

CREATE SEQUENCE public.todo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todo_id_seq OWNER TO rrodriguez;

--
-- Name: todo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rrodriguez
--

ALTER SEQUENCE public.todo_id_seq OWNED BY public.todo.id;


--
-- Name: usr; Type: TABLE; Schema: public; Owner: rrodriguez
--

CREATE TABLE public.usr (
    id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public.usr OWNER TO rrodriguez;

--
-- Name: usr_id_seq; Type: SEQUENCE; Schema: public; Owner: rrodriguez
--

CREATE SEQUENCE public.usr_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.usr_id_seq OWNER TO rrodriguez;

--
-- Name: usr_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rrodriguez
--

ALTER SEQUENCE public.usr_id_seq OWNED BY public.usr.id;


--
-- Name: category id; Type: DEFAULT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.category ALTER COLUMN id SET DEFAULT nextval('public.category_id_seq'::regclass);


--
-- Name: tablero id; Type: DEFAULT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.tablero ALTER COLUMN id SET DEFAULT nextval('public.tablero_id_seq'::regclass);


--
-- Name: todo id; Type: DEFAULT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.todo ALTER COLUMN id SET DEFAULT nextval('public.todo_id_seq'::regclass);


--
-- Name: usr id; Type: DEFAULT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.usr ALTER COLUMN id SET DEFAULT nextval('public.usr_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: rrodriguez
--

COPY public.alembic_version (version_num) FROM stdin;
bd1ccda3eb2a
\.


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: rrodriguez
--

COPY public.category (id, name) FROM stdin;
1	general
\.


--
-- Data for Name: tablero; Type: TABLE DATA; Schema: public; Owner: rrodriguez
--

COPY public.tablero (id, user_id, name, is_admin) FROM stdin;
\.


--
-- Data for Name: todo; Type: TABLE DATA; Schema: public; Owner: rrodriguez
--

COPY public.todo (id, user_id, category_id, description, is_done, created_date, deadline) FROM stdin;
33	2	1	tarea1	t	\N	\N
34	2	1	taeeeeeee	t	\N	\N
35	2	1	tarea5	t	\N	\N
36	2	1	jejejejeje	f	\N	\N
43	6	1	tarea1	t	\N	\N
44	6	1	Lavar la ropa	t	\N	\N
45	7	1	tarea fica	t	\N	\N
47	8	1	puedo crear aplicaciones uwu	t	\N	\N
48	8	1	tarea5	f	\N	\N
\.


--
-- Data for Name: usr; Type: TABLE DATA; Schema: public; Owner: rrodriguez
--

COPY public.usr (id, username, email, password) FROM stdin;
1	renato	renato.rodriguez.l@utec.edu.pe	123
2	sebb	renatorodriguezllanos@gmail.com	1
3	valerie	mail@mail.com	11111
4	holaa	hola	sha256$rnGjdHPO$5d51c3a9e2f3e08ae60e1644e080b34dabbab5e0f4c57ef992e5b8bb7987412b
5	fff	fff	sha256$w4T2Vd8t$0b00f847051740fc4c8b4ea3259c37f7b9a7e8bf0991e622e6039c91ca868429
6	sebbb	mail@mails.com	sha256$BEmZOOAf$d9f17424879a7a4e06abf64c11e2d316474c928297288a6e6f7ad19d6f8ce5cb
7	misterga	misterga@tallarinconpachamanca.edu.pe	sha256$K37ofKjy$5bf527d2538b0cea11ee3664c97a6a04e7a0dc706ed6f9f3195a8a4bc04731f1
8	sebasss	holas@gmail.com	sha256$8WSnrQVG$48e6b4bb7741f5b3cb650bb2a54583cae1597b535ff28a343c270360ef12a6aa
9	nato	reanto@gmail.com	sha256$GmUSMf5k$299adc8f5a11f5b7dacc4c1f031288f710124d3fc6865b4107ecade6599042b1
10	rodd	rodd@gmail.com	sha256$kTHcGdAP$1f01d7aae668bc50c0d587e954aa7f6a281655d17b02220f8c6d3a1987f722b6
\.


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rrodriguez
--

SELECT pg_catalog.setval('public.category_id_seq', 1, true);


--
-- Name: tablero_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rrodriguez
--

SELECT pg_catalog.setval('public.tablero_id_seq', 1, false);


--
-- Name: todo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rrodriguez
--

SELECT pg_catalog.setval('public.todo_id_seq', 59, true);


--
-- Name: usr_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rrodriguez
--

SELECT pg_catalog.setval('public.usr_id_seq', 10, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: tablero tablero_pkey; Type: CONSTRAINT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.tablero
    ADD CONSTRAINT tablero_pkey PRIMARY KEY (id);


--
-- Name: todo todo_pkey; Type: CONSTRAINT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.todo
    ADD CONSTRAINT todo_pkey PRIMARY KEY (id);


--
-- Name: usr usr_email_key; Type: CONSTRAINT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.usr
    ADD CONSTRAINT usr_email_key UNIQUE (email);


--
-- Name: usr usr_pkey; Type: CONSTRAINT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.usr
    ADD CONSTRAINT usr_pkey PRIMARY KEY (id);


--
-- Name: usr usr_username_key; Type: CONSTRAINT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.usr
    ADD CONSTRAINT usr_username_key UNIQUE (username);


--
-- Name: tablero tablero_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.tablero
    ADD CONSTRAINT tablero_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.usr(id);


--
-- Name: todo todo_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.todo
    ADD CONSTRAINT todo_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id);


--
-- Name: todo todo_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rrodriguez
--

ALTER TABLE ONLY public.todo
    ADD CONSTRAINT todo_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.usr(id);


--
-- PostgreSQL database dump complete
--

