import { describe, expect, it } from 'vitest';
import { canBook } from './booking';

const request = (start: number, end: number, changes = {}) => ({
  start, end, now: 540, blocked: false,
  bookings: [{ start: 600, end: 660 }],
  ...changes,
});

describe('assistant first suite: booking decisions', () => {
  it('T01 AC4 touching after is available', () => expect(canBook(request(660, 720))).toBe(true));
  it('T02 AC1 starting now is unavailable', () => expect(canBook(request(540, 570))).toBe(false));
  it('T03 AC1 zero duration is unavailable', () => expect(canBook(request(720, 720))).toBe(false));
  it('T04 AC1 reversed interval is unavailable', () => expect(canBook(request(750, 720))).toBe(false));
  it('T05 AC1 after day end is unavailable', () => expect(canBook(request(1380, 1441))).toBe(false));
  it('T06 AC2 exactly 120 minutes is unavailable', () => expect(canBook(request(720, 840))).toBe(false));
  it('T07 AC2 121 minutes is unavailable', () => expect(canBook(request(720, 841))).toBe(false));
  it('T08 AC4 touching before is available', () => expect(canBook(request(570, 600))).toBe(true));
  it('T09 AC4 partial overlap is unavailable', () => expect(canBook(request(630, 690))).toBe(false));
  it('T10 AC4 containing booking is unavailable', () => expect(canBook(request(570, 690))).toBe(false));
  it('T11 AC4 inside booking is unavailable', () => expect(canBook(request(615, 645))).toBe(false));
  it('T12 AC4 identical interval is unavailable', () => expect(canBook(request(600, 660))).toBe(false));
  it('T13 AC3 blocked room is unavailable', () => expect(canBook(request(660, 720, { blocked: true }))).toBe(false));
  it('T14 AC4 no existing booking is available', () => expect(canBook(request(630, 690, { bookings: [] }))).toBe(true));
  it('AC5 an available request does not alter bookings', () => {
    const bookings = [{ start: 600, end: 660 }];
    const before = structuredClone(bookings);
    expect(canBook(request(660, 720, { bookings }))).toBe(true);
    expect(bookings).toEqual(before);
  });
  it('X1 AC1 ending at 24:00 is valid', () => expect(canBook(request(1420, 1440, { bookings: [] }))).toBe(true));
  it('X2 AC4 touching a second booking is allowed', () => expect(canBook(request(720, 750, { bookings: [{ start: 600, end: 660 }, { start: 750, end: 780 }] }))).toBe(true));
});
