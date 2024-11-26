-- Conectar-se ao Banco de Dados
\c "PatientSystem";

-- Criação das Sequences para IDs
CREATE SEQUENCE user_id_seq START 1 INCREMENT BY 10;
CREATE SEQUENCE patient_id_seq START 1000 INCREMENT BY 15;
CREATE SEQUENCE auditlog_id_seq START 5000 INCREMENT BY 20;
CREATE SEQUENCE doctorpatient_id_seq START 10000 INCREMENT BY 25;

-- Criação da Tabela de Usuários
CREATE TABLE "Users" (
    id INT PRIMARY KEY DEFAULT nextval('user_id_seq'),
    name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'medico', 'paciente', 'deleted')),
    consent_status BOOLEAN DEFAULT NULL,
    reset_token VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    has_patient_history BOOLEAN DEFAULT FALSE
);

-- Criação da Tabela de Pacientes
CREATE TABLE "Patient" (
    id INT PRIMARY KEY DEFAULT nextval('patient_id_seq'),
    name VARCHAR(50) NOT NULL,
    medical_conditions TEXT,
    consent_status BOOLEAN DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    birth_date DATE NOT NULL
);

-- Criação da Tabela de Logs de Auditoria
CREATE TABLE "AuditLog" (
    id INT PRIMARY KEY DEFAULT nextval('auditlog_id_seq'),
    user_id INT NOT NULL REFERENCES "Users"(id),
    action TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da Tabela de Tokens Revogados
CREATE TABLE "RevokedToken" (
    id SERIAL PRIMARY KEY,
    jti VARCHAR(120) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da Tabela de Relação Médico-Paciente
CREATE TABLE "DoctorPatient" (
    id INT PRIMARY KEY DEFAULT nextval('doctorpatient_id_seq'),
    doctor_id INT NOT NULL REFERENCES "Users"(id),
    patient_id INT NOT NULL REFERENCES "Patient"(id),
    UNIQUE(doctor_id, patient_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--- Inserindo 10 usuários com histórico de paciente
INSERT INTO "Users" (name, email, password, role, cpf)
VALUES
('Carlos Silva', 'carlossilva@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'paciente', '85732914277'),  
('Daniel Souza', 'danielsouza@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'paciente', '41101217103'),  
('Paula Lima', 'paulalima@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'paciente', '46662505226'),    
('João Almeida', 'joaoalmeida@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'paciente', '55868755197'), 
('Luana Freitas', 'luanfreitas@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'paciente', '85291586524'), 
('Felipe Gonçalves', 'felipegoncalves@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'paciente', '80888964366'), 
('Clara Ramos', 'claramos@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'paciente', '03701224536'),  
('Eduardo Martins', 'eduardomartins@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'paciente', '11111365300'), 
('Marta Farias', 'martafarias@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'paciente', '14683194775'),
('Luciana Barbosa', 'lucianabarbosa@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'paciente', '05316461819');

-- Inserindo 10 pacientes com correspondência exata aos usuários
INSERT INTO "Patient" (name, medical_conditions, consent_status, cpf, birth_date)
VALUES
('Carlos Silva', 'Hipertensão', TRUE, '85732914277', '1978-01-12'),
('Daniel Souza', 'Diabetes Tipo 2', TRUE, '41101217103', '1985-04-08'),
('Paula Lima', 'Hipertensão e Colesterol Alto', TRUE, '46662505226', '1973-06-20'),
('João Almeida', 'Cardiopatia', TRUE, '55868755197', '1963-03-15'),
('Luana Freitas', 'Asma', TRUE, '85291586524', '1994-11-25'),
('Felipe Gonçalves', 'Nenhuma', TRUE, '80888964366', '1989-09-10'),
('Clara Ramos', 'Hipotireoidismo', TRUE, '03701224536', '1981-07-05'),
('Eduardo Martins', 'Diabetes Tipo 1', TRUE, '11111365300', '1968-02-17'),
('Marta Farias', 'Obesidade', TRUE, '14683194775', '1986-08-09'),
('Luciana Barbosa', 'Nenhuma', TRUE, '05316461819', '1973-12-01');

-- Inserindo um usuário administrador padrão
INSERT INTO "Users" (name, email, password, role, cpf)
VALUES
('Felipe Sobral', 'felipesobral_@hotmail.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'admin', '14757791833');

-- Inserindo 5 médicos na tabela Users
INSERT INTO "Users" (name, email, password, role, cpf)
VALUES
('Marcos Aurélio', 'marcosaurelio@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'medico', '70011111111'),
('Beatriz Farias', 'beatrizfarias@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'medico', '70022222222'),
('Carlos Pereira', 'carlospereira@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'medico', '10290759056'),
('Ana Souza', 'anasouza@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'medico', '01694513050'),
('Pedro Lima', 'pedrolima@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'medico', '96020108007');

-- Relação Médico-Paciente
INSERT INTO "DoctorPatient" (doctor_id, patient_id)
VALUES
((SELECT id FROM "Users" WHERE name = 'Marcos Aurélio'), (SELECT id FROM "Patient" WHERE name = 'Carlos Silva')),
((SELECT id FROM "Users" WHERE name = 'Marcos Aurélio'), (SELECT id FROM "Patient" WHERE name = 'Daniel Souza')),
((SELECT id FROM "Users" WHERE name = 'Beatriz Farias'), (SELECT id FROM "Patient" WHERE name = 'Paula Lima')),
((SELECT id FROM "Users" WHERE name = 'Beatriz Farias'), (SELECT id FROM "Patient" WHERE name = 'João Almeida'));

-- Function para atualizar os valores de 'has_patient_history' a partir da relação dos inserts iniciais entre paciente e usuários
CREATE OR REPLACE FUNCTION update_patient_history_status()
RETURNS VOID AS $$
BEGIN
    -- Atualiza o status has_patient_history para TRUE onde houver correspondência de CPF
    UPDATE "Users"
    SET has_patient_history = TRUE
    WHERE cpf IN (SELECT cpf FROM "Patient");

    -- Atualiza para FALSE onde não houver correspondência
    UPDATE "Users"
    SET has_patient_history = FALSE
    WHERE cpf NOT IN (SELECT cpf FROM "Patient");
END;
$$ LANGUAGE plpgsql;


-- Função de trigger para atualizar has_patient_history em "Users" ao inserir um novo paciente
CREATE OR REPLACE FUNCTION set_patient_history_on_patient_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se há um usuário correspondente ao novo paciente
    UPDATE "Users"
    SET has_patient_history = TRUE
    WHERE cpf = NEW.cpf;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para chamar a função ao inserir um paciente
CREATE TRIGGER patient_insert_trigger
AFTER INSERT ON "Patient"
FOR EACH ROW
EXECUTE FUNCTION set_patient_history_on_patient_insert();

-- Função de trigger para atualizar has_patient_history em "Users" ao inserir um novo usuário
CREATE OR REPLACE FUNCTION set_patient_history_on_user_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Se o CPF do usuário existe na tabela Patient, define has_patient_history como TRUE
    IF EXISTS (SELECT 1 FROM "Patient" WHERE cpf = NEW.cpf) THEN
        NEW.has_patient_history := TRUE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para chamar a função ao inserir um usuário
CREATE TRIGGER user_insert_trigger
BEFORE INSERT ON "Users"
FOR EACH ROW
EXECUTE FUNCTION set_patient_history_on_user_insert();

-- Função de trigger para atualizar has_patient_history ao excluir um paciente
CREATE OR REPLACE FUNCTION reset_patient_history_on_patient_delete()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se há um usuário correspondente ao CPF do paciente excluído
    UPDATE "Users"
    SET has_patient_history = FALSE
    WHERE cpf = OLD.cpf
    AND NOT EXISTS (SELECT 1 FROM "Patient" WHERE cpf = OLD.cpf);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger para chamar a função ao excluir um paciente
CREATE TRIGGER patient_delete_trigger
AFTER DELETE ON "Patient"
FOR EACH ROW
EXECUTE FUNCTION reset_patient_history_on_patient_delete();

-- Função de trigger para atualizar has_patient_history ao excluir um usuário
CREATE OR REPLACE FUNCTION reset_patient_history_on_user_delete()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se há um paciente correspondente ao CPF do usuário excluído
    UPDATE "Users"
    SET has_patient_history = FALSE
    WHERE cpf = OLD.cpf
    AND NOT EXISTS (SELECT 1 FROM "Users" WHERE cpf = OLD.cpf);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger para chamar a função ao excluir um usuário
CREATE TRIGGER user_delete_trigger
AFTER DELETE ON "Users"
FOR EACH ROW
EXECUTE FUNCTION reset_patient_history_on_user_delete();


-- Chamar a função após o init_db.sql para iniciar o valor de has_patient_history corretamente
SELECT update_patient_history_status();

