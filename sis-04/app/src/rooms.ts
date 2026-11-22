import type { Interval } from './booking';

export type Room = {
  id: string;
  name: string;
  capacity: number;
  equipment: string[];
  blocked: boolean;
  bookings: Interval[];
};

export const ROOMS: Room[] = [
  { id: 'a101', name: 'Room A-101', capacity: 40, equipment: ['projector', 'whiteboard'], blocked: false, bookings: [{ start: 600, end: 660 }] },
  { id: 'b204', name: 'Room B-204', capacity: 20, equipment: ['projector'], blocked: false, bookings: [] },
  { id: 'c303', name: 'Room C-303', capacity: 8, equipment: ['whiteboard'], blocked: true, bookings: [] },
  { id: 'd404', name: 'Room D-404', capacity: 12, equipment: ['projector', 'whiteboard'], blocked: false, bookings: [{ start: 690, end: 750 }] },
];
