-- Conectar-se ao Banco de Dados
\c "PatientSystem";

-- Criação da Tabela de Usuários
CREATE TABLE "Users" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'medico', 'paciente', 'deleted')),
    consent_status BOOLEAN DEFAULT NULL,
    reset_token VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpf VARCHAR(11) UNIQUE NOT NULL
);

-- Criação da Tabela de Pacientes
CREATE TABLE "Patient" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    medical_conditions TEXT,
    consent_status BOOLEAN DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpf VARCHAR(11) UNIQUE NOT NULL
);

-- Criação da Tabela de Logs de Auditoria
CREATE TABLE "AuditLog" (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "Users" (id) ON DELETE CASCADE
);

-- Criação da Tabela de Tokens Revogados
CREATE TABLE "RevokedToken" (
    id SERIAL PRIMARY KEY,
    jti VARCHAR(120) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir Registros na Tabela Patient
INSERT INTO "Patient" (name, age, medical_conditions, consent_status, created_at, cpf)
VALUES 
('Alice Oliveira', 45, 'Diabetes', TRUE, CURRENT_TIMESTAMP, '85732914277'),
('Bruno Silva', 50, 'Hipertensão', FALSE, CURRENT_TIMESTAMP, '41101217103'),
('Carlos Sousa', 60, 'Diabetes e Hipertensão', TRUE, CURRENT_TIMESTAMP, '46662505226'),
('Daniela Costa', 35, 'Hipertensão', TRUE, CURRENT_TIMESTAMP, '55868755197'),
('Eduardo Nascimento', 40, 'Diabetes', FALSE, CURRENT_TIMESTAMP, '85291586524'),
('Fernanda Lima', 55, 'AVC', TRUE, CURRENT_TIMESTAMP, '80888964366'),
('Gustavo Almeida', 30, 'Diabetes', TRUE, CURRENT_TIMESTAMP, '03701224536'),
('Helena Rocha', 48, 'Hipertensão', FALSE, CURRENT_TIMESTAMP, '11111365300'),
('Igor Fernandes', 52, 'Diabetes e AVC', TRUE, CURRENT_TIMESTAMP, '14683194775'),
('Jéssica Ribeiro', 47, 'Hipertensão', TRUE, CURRENT_TIMESTAMP, '05316461819'),
('Kleber Martins', 36, 'Diabetes', FALSE, CURRENT_TIMESTAMP, '49403035005'),
('Larissa Pereira', 39, 'AVC', TRUE, CURRENT_TIMESTAMP, '67847354047'),
('Maurício Carvalho', 41, 'Diabetes e Hipertensão', TRUE, CURRENT_TIMESTAMP, '51399815059'),
('Natália Batista', 58, 'Hipertensão', FALSE, CURRENT_TIMESTAMP, '78544754074'),
('Otávio Farias', 33, 'Diabetes', TRUE, CURRENT_TIMESTAMP, '50763847003'),
('Priscila Moreira', 59, 'AVC', TRUE, CURRENT_TIMESTAMP, '48470862014'),
('Renato Gomes', 42, 'Hipertensão', FALSE, CURRENT_TIMESTAMP, '65665323071'),
('Sabrina Barros', 37, 'Diabetes e AVC', TRUE, CURRENT_TIMESTAMP, '20432901000'),
('Tiago Mendes', 34, 'AVC', FALSE, CURRENT_TIMESTAMP, '68105071088'),
('Vanessa Cunha', 62, 'Diabetes e Hipertensão', TRUE, CURRENT_TIMESTAMP, '67250876040');

-- Inserindo um usuário administrador padrão
INSERT INTO "Users" (name, email, password, role, cpf)
VALUES
('Felipe Sobral', 'felipesobral_@hotmail.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'admin', '14757791833');