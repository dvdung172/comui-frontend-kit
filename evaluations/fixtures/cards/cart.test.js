import test from 'node:test';
import assert from 'node:assert/strict';
import { nextQuantity } from './cart.js';
test('quantity never becomes negative', () => {
  assert.equal(nextQuantity(1, -2), 0);
  assert.equal(nextQuantity(2, 1), 3);
});
