const request = require('supertest');
const app = require('../server');

describe('GET /comments', () => {
  it('doit répondre avec des commentaires', async () => {
    const res = await request(app).get('/comments');
    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
  });
});
