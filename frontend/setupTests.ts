import { vi } from 'vitest';
import '@testing-library/jest-dom';
import { config } from '@vue/test-utils';
import { defineComponent } from 'vue';

// Stub para fetch
global.fetch = vi.fn().mockResolvedValue({
  json: () => Promise.resolve({}),
  headers: new Headers(),
  ok: true,
  redirected: false,
  status: 200,
  statusText: 'OK',
  type: 'basic',
  url: '',
  body: null,
  bodyUsed: false,
  arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)),
  blob: () => Promise.resolve(new Blob()),
  clone: () => ({ ...new Response() }),
  formData: () => Promise.resolve(new FormData()),
  text: () => Promise.resolve('')
});

// Stub para outras APIs globais, se necessário
global.window = Object.create(window);
global.window.alert = vi.fn();
global.window.matchMedia = vi.fn().mockImplementation(query => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: vi.fn(),
  removeListener: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  dispatchEvent: vi.fn(),
  mounted: vi.fn(),
  data: vi.fn()
}));

// Stub para localStorage
global.localStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  length: 0,
  key: vi.fn().mockImplementation((index: number) => {
    const keys = Object.keys(localStorage);
    return keys[index] || null;
  })
};

// Stub para sessionStorage
global.sessionStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  length: 0,
  key: vi.fn().mockImplementation((index: number) => {
    const keys = Object.keys(sessionStorage);
    return keys[index] || null;
  })
};

// Stub para ResizeObserver
global.ResizeObserver = class {
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Stubs para componentes globais
config.global.stubs = {
  'router-view': true,
  'router-link': true
};

// Mocking RouterLink para evitar erros de resolução
config.global.components = {
  RouterLink: {
    template: '<a><slot /></a>',
  },
};