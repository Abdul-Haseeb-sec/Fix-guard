const { describe, it } = require('node:test');
const assert = require('node:assert');
const { quickScan, thresholdCheck } = require('./detector.js');

describe('Detector Logic', () => {
  describe('quickScan', () => {
    it('should flag scores >= 8', () => {
      assert.strictEqual(quickScan(8).detected, true);
    });
    it('should pass scores < 8', () => {
      assert.strictEqual(quickScan(7).detected, false);
    });
  });

  describe('thresholdCheck', () => {
    it('should flag extreme scores', () => {
      assert.strictEqual(thresholdCheck(10, 5).detected, true);
    });
    it('should pass safe scores', () => {
      assert.strictEqual(thresholdCheck(2, 5).detected, false);
    });
  });
});
