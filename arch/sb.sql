-- =========================
-- USUARIO
-- =========================
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    nome_completo VARCHAR(150),
    seguidores_count INTEGER DEFAULT 0,
    seguindo_count INTEGER DEFAULT 0
);

-- =========================
-- AUTOR
-- =========================
CREATE TABLE autor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    data_nascimento DATE,
    descricao TEXT,
    seguidores_count INTEGER DEFAULT 0
);

-- =========================
-- LIVRO
-- =========================
CREATE TABLE livro (
    id SERIAL PRIMARY KEY,
    id_autor INTEGER NOT NULL,
    nome VARCHAR(200) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    data_publicacao DATE,
    descricao TEXT,

    FOREIGN KEY (id_autor) REFERENCES autor(id) ON DELETE CASCADE
);

-- =========================
-- GENERO
-- =========================
CREATE TABLE genero (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL
);

-- =========================
-- LIVRO_GENERO (N:N)
-- =========================
CREATE TABLE livro_genero (
    id_livro INTEGER,
    id_genero INTEGER,
    PRIMARY KEY (id_livro, id_genero),

    FOREIGN KEY (id_livro) REFERENCES livro(id) ON DELETE CASCADE,
    FOREIGN KEY (id_genero) REFERENCES genero(id) ON DELETE CASCADE
);

-- =========================
-- AUTOR_GENERO (N:N)
-- =========================
CREATE TABLE autor_genero (
    id_autor INTEGER,
    id_genero INTEGER,
    PRIMARY KEY (id_autor, id_genero),

    FOREIGN KEY (id_autor) REFERENCES autor(id) ON DELETE CASCADE,
    FOREIGN KEY (id_genero) REFERENCES genero(id) ON DELETE CASCADE
);

-- =========================
-- AVALIACAO
-- =========================
CREATE TABLE avaliacao (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    tipo SMALLINT NOT NULL, -- 1=livro, 2=autor, 3=genero
    id_alvo INTEGER NOT NULL,
    nota NUMERIC(2,1) CHECK (nota >= 0 AND nota <= 5),
    texto TEXT,
    data_publicacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);

-- =========================
-- COMENTARIO (com threads)
-- =========================
CREATE TABLE comentario (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    tipo_alvo SMALLINT NOT NULL, -- 1=avaliacao, 2=post
    id_alvo INTEGER NOT NULL,
    id_pai INTEGER,
    texto TEXT NOT NULL,
    data_publicacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes_count INTEGER DEFAULT 0,

    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_pai) REFERENCES comentario(id) ON DELETE CASCADE
);

CREATE TABLE comentario_like (
    id_usuario INTEGER NOT NULL,
    id_comentario INTEGER NOT NULL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id_usuario, id_comentario),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_comentario) REFERENCES comentario(id) ON DELETE CASCADE
);

-- =========================
-- SEGUIDOR
-- =========================
CREATE TABLE seguidor (
    id_seguidor INTEGER,
    id_seguido INTEGER,
    status VARCHAR(20) DEFAULT 'ativo',
    data_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id_seguidor, id_seguido),

    FOREIGN KEY (id_seguidor) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_seguido) REFERENCES usuario(id) ON DELETE CASCADE,

    CHECK (id_seguidor <> id_seguido),
    CHECK (status IN ('ativo', 'bloqueado', 'pendente'))
);




-- =========================
-- ÍNDICES IMPORTANTES
-- =========================
CREATE INDEX idx_avaliacao_usuario ON avaliacao(id_usuario);

CREATE INDEX idx_comentario_alvo 
ON comentario(tipo_alvo, id_alvo);

CREATE INDEX idx_seguidor_seguido 
ON seguidor(id_seguido);

-- =========================
-- TRIGGER: FOLLOW / UNFOLLOW
-- =========================

-- FUNÇÃO

CREATE OR REPLACE FUNCTION atualizar_likes_comentario()
RETURNS TRIGGER AS $$
BEGIN

    -- curtir
    IF TG_OP = 'INSERT' THEN
        UPDATE comentario
        SET likes_count = likes_count + 1
        WHERE id = NEW.id_comentario;
    END IF;

    -- descurtir
    IF TG_OP = 'DELETE' THEN
        UPDATE comentario
        SET likes_count = likes_count - 1
        WHERE id = OLD.id_comentario;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION atualizar_contadores_seguidor()
RETURNS TRIGGER AS $$
BEGIN

    -- INSERT (seguir)
    IF TG_OP = 'INSERT' THEN
        IF NEW.status = 'ativo' THEN
            UPDATE usuario 
            SET seguidores_count = seguidores_count + 1
            WHERE id = NEW.id_seguido;

            UPDATE usuario 
            SET seguindo_count = seguindo_count + 1
            WHERE id = NEW.id_seguidor;
        END IF;
    END IF;

    -- DELETE (deixar de seguir)
    IF TG_OP = 'DELETE' THEN
        IF OLD.status = 'ativo' THEN
            UPDATE usuario 
            SET seguidores_count = seguidores_count - 1
            WHERE id = OLD.id_seguido;

            UPDATE usuario 
            SET seguindo_count = seguindo_count - 1
            WHERE id = OLD.id_seguidor;
        END IF;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER INSERT
CREATE TRIGGER trigger_seguir
AFTER INSERT ON seguidor
FOR EACH ROW
EXECUTE FUNCTION atualizar_contadores_seguidor();

-- TRIGGER DELETE
CREATE TRIGGER trigger_deixar_seguir
AFTER DELETE ON seguidor
FOR EACH ROW
EXECUTE FUNCTION atualizar_contadores_seguidor();