let selectedSlot = null;

function buildCalendar() {
  const container = document.getElementById("calendar");

  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const startHour = 8;   // earliest interview hour
  const endHour = 21;    // latest hour

  let html = `<div class='calendar-container'>
    <div class='calendar-grid'>
      <div class='calendar-header'></div>`;

  days.forEach(day => {
    html += `<div class='calendar-header'>${day}</div>`;
  });

  html += `</div>`;

  for (let hour = startHour; hour <= endHour; hour++) {
    html += `<div class='calendar-grid'>
      <div class='time-cell'>${hour}:00</div>`;

    for (let d = 0; d < 7; d++) {
      const start = getISODate(d, hour);
      const end = getISODate(d, hour + 1);

      html += `<div class='slot-cell' data-start="${start}" data-end="${end}"
               onclick="selectSlot(this)"></div>`;
    }
    html += `</div>`;
  }

  html += `</div>`;
  container.innerHTML = html;
}

function getISODate(dayOffset, hour) {
  const now = new Date();
  const nextMonday = new Date(now.setDate(now.getDate() - now.getDay() + 1));
  nextMonday.setHours(hour, 0, 0, 0);
  nextMonday.setDate(nextMonday.getDate() + dayOffset);
  return nextMonday.toISOString();
}

function selectSlot(cell) {
  if (selectedSlot) {
    selectedSlot.classList.remove("slot-selected");
  }
  cell.classList.add("slot-selected");
  selectedSlot = cell;

  const slotStart = cell.dataset.start;
  const slotEnd = cell.dataset.end;

  document.getElementById("selectedSlot").innerHTML =
    `Selected: ${slotStart} / ${slotEnd}`;

  document.getElementById("submitBtn").disabled = false;
}
