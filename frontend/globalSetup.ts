import { beforeAll, afterAll } from 'vitest';

beforeAll(() => {
  console.log('Configurações globais iniciais realizadas.');
});

afterAll(() => {
  console.log('Limpeza global realizada.');
});
