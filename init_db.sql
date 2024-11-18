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

ALTER TABLE "Users" ADD COLUMN has_patient_history BOOLEAN DEFAULT FALSE;


-- Criação da Tabela de Pacientes
CREATE TABLE "Patient" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    medical_conditions TEXT,
    consent_status BOOLEAN DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    birth_date DATE NOT NULL
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

-- Criação da Tabela de Associação Medico-Paciente
CREATE TABLE "DoctorPatient" (
    id SERIAL PRIMARY KEY,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES "Users" (id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES "Patient" (id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir Registros na Tabela Patient
INSERT INTO "Patient" (name, age, medical_conditions, consent_status, created_at, cpf, birth_date)
VALUES 
('Alice Oliveira', 45, 'Diabetes', TRUE, CURRENT_TIMESTAMP, '85732914277', '1985-03-12'),
('Bruno Silva', 50, 'Hipertensão', FALSE, CURRENT_TIMESTAMP, '41101217103', '1978-05-21'),
('Carlos Sousa', 60, 'Diabetes e Hipertensão', TRUE, CURRENT_TIMESTAMP, '46662505226', '1990-07-15'),
('Daniela Costa', 35, 'Hipertensão', TRUE, CURRENT_TIMESTAMP, '55868755197', '1965-11-20'),
('Eduardo Nascimento', 40, 'Diabetes', FALSE, CURRENT_TIMESTAMP, '85291586524', '2000-02-28'),
('Fernanda Lima', 55, 'AVC', TRUE, CURRENT_TIMESTAMP, '80888964366', '1982-09-05'),
('Gustavo Almeida', 30, 'Diabetes', TRUE, CURRENT_TIMESTAMP, '03701224536', '1956-01-10'),
('Helena Rocha', 48, 'Hipertensão', FALSE, CURRENT_TIMESTAMP, '11111365300', '1995-12-15'),
('Igor Fernandes', 52, 'Diabetes e AVC', TRUE, CURRENT_TIMESTAMP, '14683194775', '1969-06-25'),
('Jéssica Ribeiro', 47, 'Hipertensão', TRUE, CURRENT_TIMESTAMP, '05316461819', '1988-04-14'),
('Kleber Martins', 36, 'Diabetes', FALSE, CURRENT_TIMESTAMP, '49403035005', '1945-08-30'),
('Larissa Pereira', 39, 'AVC', TRUE, CURRENT_TIMESTAMP, '67847354047', '1974-03-19'),
('Maurício Carvalho', 41, 'Diabetes e Hipertensão', TRUE, CURRENT_TIMESTAMP, '51399815059', '2005-11-09'),
('Natália Batista', 58, 'Hipertensão', FALSE, CURRENT_TIMESTAMP, '78544754074', '1992-10-21'),
('Otávio Farias', 33, 'Diabetes', TRUE, CURRENT_TIMESTAMP, '50763847003', '1980-01-03'),
('Priscila Moreira', 59, 'AVC', TRUE, CURRENT_TIMESTAMP, '48470862014', '1950-05-13'),
('Renato Gomes', 42, 'Hipertensão', FALSE, CURRENT_TIMESTAMP, '65665323071', '1998-08-07'),
('Sabrina Barros', 37, 'Diabetes e AVC', TRUE, CURRENT_TIMESTAMP, '20432901000', '1963-09-30'),
('Tiago Mendes', 34, 'AVC', FALSE, CURRENT_TIMESTAMP, '68105071088', '2003-12-05'),
('Vanessa Cunha', 62, 'Diabetes e Hipertensão', TRUE, CURRENT_TIMESTAMP, '67250876040', '1948-02-16');

-- Inserindo um usuário administrador padrão
INSERT INTO "Users" (name, email, password, role, cpf)
VALUES
('Felipe Sobral', 'felipesobral_@hotmail.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'admin', '14757791833');

-- Inserindo 5 médicos na tabela Users
INSERT INTO "Users" (name, email, password, role, cpf)
VALUES
('Dr. João Costa', 'joaocosta@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'medico', '75846193048'),
('Dra. Maria Alves', 'mariaalves@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'medico', '91327382008'),
('Dr. Carlos Pereira', 'carlospereira@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'medico', '10290759056'),
('Dra. Ana Souza', 'anasouza@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'medico', '01694513050'),
('Dr. Pedro Lima', 'pedrolima@hospital.com', '$2b$12$QAbrOTtk1M6Zfda/y3e5ReDxXxMtnwYcVmVAqFbgk/8xe9K6dJvFG', 'medico', '96020108007');

-- Inserindo 10 usuários com histórico de paciente
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

