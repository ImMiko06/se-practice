export type Interval = { start: number; end: number };

export type BookingRequest = {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: Interval[];
};

type BookingInput = {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: { start: number; end: number }[];
};

function isValidRequest({ start, end, now }: Pick<BookingInput, 'start' | 'end' | 'now'>): boolean {
  return Number.isInteger(start) && Number.isInteger(end) && Number.isInteger(now)
    && 0 <= start && start < end && end <= 1440 && start > now && end - start <= 120;
}

function hasOverlap(start: number, end: number, bookings: BookingInput['bookings']): boolean {
  return bookings.some(booking => start < booking.end && end > booking.start);
}

export function canBook(request: BookingInput): boolean {
  if (!isValidRequest(request)) return false;
  if (request.blocked) return false;
  return !hasOverlap(request.start, request.end, request.bookings);
}
