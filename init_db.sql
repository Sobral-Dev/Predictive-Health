-- Conectar-se ao Banco de Dados
\c "PatientSystem";

-- Criação da Tabela de Usuários
CREATE TABLE "Users" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'medico', 'paciente', 'deleted')),
    consent_status BOOLEAN DEFAULT FALSE,
    reset_token VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da Tabela de Pacientes
CREATE TABLE "Patient" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    medical_conditions TEXT,
    consent_status BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
INSERT INTO "Patient" (name, age, medical_conditions, consent_status, created_at)
VALUES 
('Alice Oliveira', 45, 'Diabetes', TRUE, CURRENT_TIMESTAMP),
('Bruno Silva', 50, 'Hipertensão', FALSE, CURRENT_TIMESTAMP),
('Carlos Sousa', 60, 'Diabetes e Hipertensão', TRUE, CURRENT_TIMESTAMP),
('Daniela Costa', 35, 'Hipertensão', TRUE, CURRENT_TIMESTAMP),
('Eduardo Nascimento', 40, 'Diabetes', FALSE, CURRENT_TIMESTAMP),
('Fernanda Lima', 55, 'AVC', TRUE, CURRENT_TIMESTAMP),
('Gustavo Almeida', 30, 'Diabetes', TRUE, CURRENT_TIMESTAMP),
('Helena Rocha', 48, 'Hipertensão', FALSE, CURRENT_TIMESTAMP),
('Igor Fernandes', 52, 'Diabetes e AVC', TRUE, CURRENT_TIMESTAMP),
('Jéssica Ribeiro', 47, 'Hipertensão', TRUE, CURRENT_TIMESTAMP),
('Kleber Martins', 36, 'Diabetes', FALSE, CURRENT_TIMESTAMP),
('Larissa Pereira', 39, 'AVC', TRUE, CURRENT_TIMESTAMP),
('Maurício Carvalho', 41, 'Diabetes e Hipertensão', TRUE, CURRENT_TIMESTAMP),
('Natália Batista', 58, 'Hipertensão', FALSE, CURRENT_TIMESTAMP),
('Otávio Farias', 33, 'Diabetes', TRUE, CURRENT_TIMESTAMP),
('Priscila Moreira', 59, 'AVC', TRUE, CURRENT_TIMESTAMP),
('Renato Gomes', 42, 'Hipertensão', FALSE, CURRENT_TIMESTAMP),
('Sabrina Barros', 37, 'Diabetes e AVC', TRUE, CURRENT_TIMESTAMP),
('Tiago Mendes', 34, 'AVC', FALSE, CURRENT_TIMESTAMP),
('Vanessa Cunha', 62, 'Diabetes e Hipertensão', TRUE, CURRENT_TIMESTAMP);

-- Inserindo um usuário administrador padrão
INSERT INTO "Users" (name, email, password, role)
VALUES
('Felipe Sobral', 'felipesobral_@hotmail.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'admin');