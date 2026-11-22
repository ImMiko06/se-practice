import { describe, expect, it } from 'vitest';
import { canBook, checkRoom } from './booking';
import { filterRooms } from './filter';
import type { Room } from './rooms';

const catalog: Room[] = [
  { id: 'small', name: 'Small', capacity: 8, equipment: ['whiteboard'], blocked: false, bookings: [{ start: 600, end: 660 }] },
  { id: 'large', name: 'Large', capacity: 20, equipment: ['whiteboard', 'projector'], blocked: false, bookings: [] },
  { id: 'blocked', name: 'Blocked', capacity: 20, equipment: ['projector'], blocked: true, bookings: [] },
];
const request = { start: 700, end: 760, now: 600 };

describe('SIS 04 booking and room catalog requirements', () => {
  it('AC1: rejects start equal to end', () => expect(canBook({ ...request, end: 700, blocked: false, bookings: [] })).toBe(false));
  it('AC2 B2: rejects a request longer than 120 minutes', () => expect(canBook({ ...request, end: 821, blocked: false, bookings: [] })).toBe(false));
  it('AC3 F3: never makes a blocked room available', () => expect(checkRoom(catalog, 'blocked', request)).toBe(false));
  it('AC4 B4: rejects overlapping bookings', () => expect(canBook({ ...request, start: 650, end: 710, blocked: false, bookings: [{ start: 600, end: 660 }] })).toBe(false));
  it('AC4 B3: permits intervals touching at an endpoint', () => expect(canBook({ ...request, start: 660, end: 720, blocked: false, bookings: [{ start: 600, end: 660 }] })).toBe(true));
  it('AC5: leaves booking data unchanged', () => { const before = structuredClone(catalog); checkRoom(catalog, 'small', request); expect(catalog).toEqual(before); });
  it('AC1: rejects a request in the past', () => expect(canBook({ start: 500, end: 550, now: 600, blocked: false, bookings: [] })).toBe(false));
  it('B1 AC2: allows exactly 120 minutes', () => expect(canBook({ start: 700, end: 820, now: 600, blocked: false, bookings: [] })).toBe(true));
  it('B5 F1: includes a room whose capacity equals attendees', () => expect(filterRooms(catalog, { attendees: 8, equipment: [] }).map(r => r.id)).toContain('small'));
  it('B6 F1: excludes a room below requested capacity', () => expect(filterRooms(catalog, { attendees: 9, equipment: [] }).map(r => r.id)).not.toContain('small'));
  it('F2: requires every selected equipment item', () => expect(filterRooms(catalog, { attendees: 1, equipment: ['projector', 'whiteboard'] }).map(r => r.id)).toEqual(['large']));
  it('F4: yields an empty list when no room meets criteria', () => expect(filterRooms(catalog, { attendees: 99, equipment: [] })).toEqual([]));
  it('F5: checks bookings belonging to the selected room', () => { expect(checkRoom(catalog, 'small', { start: 630, end: 650, now: 600 })).toBe(false); expect(checkRoom(catalog, 'large', { start: 630, end: 650, now: 600 })).toBe(true); });
  it('F5: an unknown room id is unavailable', () => expect(checkRoom(catalog, 'missing', request)).toBe(false));
  it('INT: filters rooms and checks the chosen matching room', () => { const result = filterRooms(catalog, { attendees: 10, equipment: ['projector'] }); expect(result.map(r => r.id)).toEqual(['large', 'blocked']); expect(checkRoom(catalog, result[0].id, request)).toBe(true); });
});
