import { useMemo, useState } from 'react';
import { checkRoom } from './booking';
import { filterRooms } from './filter';
import { ROOMS } from './rooms';

const toMinutes = (value: string) => {
  const [h, m] = value.split(':').map(Number);
  return h * 60 + m;
};
const fmt = (m: number) => `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;

export default function App() {
  const [attendees, setAttendees] = useState(1);
  const [equipment, setEquipment] = useState<string[]>([]);
  const [roomId, setRoomId] = useState('a101');
  const [now, setNow] = useState('09:00');
  const [start, setStart] = useState('11:00');
  const [end, setEnd] = useState('12:00');
  const [endOfDay, setEndOfDay] = useState(false);
  const [result, setResult] = useState<boolean | null>(null);
  const [error, setError] = useState('');
  const matches = useMemo(() => filterRooms(ROOMS, { attendees, equipment }), [attendees, equipment]);
  const selected = matches.find(room => room.id === roomId) ?? matches[0];

  function clearFeedback() { setResult(null); setError(''); }
  function toggleEquipment(item: string) {
    setEquipment(current => current.includes(item) ? current.filter(value => value !== item) : [...current, item]);
    clearFeedback();
  }
  function check() {
    setResult(null);
    if (!selected || !now || !start || (!end && !endOfDay)) {
      setError('Fill in the current time, start and end.');
      return;
    }
    const s = toMinutes(start), e = endOfDay ? 1440 : toMinutes(end), n = toMinutes(now);
    if (!(s < e)) { setError('The end time must be after the start time.'); return; }
    setError('');
    setResult(checkRoom(ROOMS, selected.id, { start: s, end: e, now: n }));
  }

  return <main className="page">
    <h1>Smart Campus Room Availability</h1>
    <div className="row">
      <label>Attendees<input aria-label="Attendees" type="number" min="1" value={attendees} onChange={e => { setAttendees(Number(e.target.value)); clearFeedback(); }} /></label>
      <fieldset><legend>Required equipment</legend>
        {['projector', 'whiteboard'].map(item => <label className="inline" key={item}><input type="checkbox" checked={equipment.includes(item)} onChange={() => toggleEquipment(item)} />{item}</label>)}
      </fieldset>
      <label>Room<select aria-label="Room" value={selected?.id ?? ''} disabled={!matches.length} onChange={e => { setRoomId(e.target.value); clearFeedback(); }}>
        {matches.map(room => <option key={room.id} value={room.id}>{room.name}{room.blocked ? ' (blocked)' : ''}</option>)}
      </select></label>
      <label>Current time<input aria-label="Current time" type="time" required value={now} onChange={e => { setNow(e.target.value); clearFeedback(); }} /></label>
      <label>Start<input aria-label="Start" type="time" required value={start} onChange={e => { setStart(e.target.value); clearFeedback(); }} /></label>
      <label>End<input aria-label="End" type="time" required={!endOfDay} value={end} disabled={endOfDay} onChange={e => { setEnd(e.target.value); clearFeedback(); }} /></label>
      <label className="inline"><input type="checkbox" checked={endOfDay} onChange={e => { setEndOfDay(e.target.checked); clearFeedback(); }} />Ends at 24:00</label>
    </div>
    <button type="button" onClick={check} disabled={!selected}>Check availability</button>
    {error && <p className="error">{error}</p>}
    {result !== null && <p className={`result ${result ? 'available' : 'unavailable'}`}>{result ? 'Available' : 'Unavailable'}</p>}
    <h2>Matching rooms</h2>
    {!matches.length ? <p role="status">No rooms match these requirements.</p> : <ul>{matches.map(room => <li key={room.id}>{room.name} — {room.capacity} seats; {room.equipment.join(', ') || 'no equipment'}{room.blocked ? ' — blocked' : ''}</li>)}</ul>}
    <h2>Selected room bookings</h2>
    {!selected ? <p>No room selected.</p> : <ul>{selected.bookings.length ? selected.bookings.map((b, i) => <li key={i}>{fmt(b.start)}–{fmt(b.end)}</li>) : <li>none</li>}</ul>}
  </main>;
}
