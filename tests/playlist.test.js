const request = require('supertest');
const app = require('../server');

describe('GET /playlist', () => {
  it('doit répondre avec une playlist', async () => {
    const res = await request(app).get('/playlist');
    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
  });
});
