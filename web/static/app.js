let subjectCount = 0;
let teacherCount = 0;

function addSubject() {
  const container = document.getElementById('subjects');
  const emptyState = container.querySelector('.empty-state');
  if (emptyState) emptyState.remove();

  const div = document.createElement('div');
  div.className = 'item';
  div.innerHTML = `
    <input type="text" name="subject_${subjectCount}" placeholder="Subject name" required>
    <button type="button" class="remove-btn" onclick="this.parentElement.remove(); checkEmpty('subjects')">×</button>
  `;
  container.appendChild(div);
  subjectCount++;
  div.querySelector('input').focus();
}

function addTeacher() {
  const container = document.getElementById('teachers');
  const emptyState = container.querySelector('.empty-state');
  if (emptyState) emptyState.remove();

  const div = document.createElement('div');
  div.className = 'item';
  div.innerHTML = `
    <input type="text" name="teacher_${teacherCount}" placeholder="Teacher name" required>
    <button type="button" class="remove-btn" onclick="this.parentElement.remove(); checkEmpty('teachers')">×</button>
  `;
  container.appendChild(div);
  teacherCount++;
  div.querySelector('input').focus();
}

function checkEmpty(containerId) {
  const container = document.getElementById(containerId);
  if (container.children.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'empty-state';
    empty.textContent = containerId === 'subjects' ? 'No subjects added yet' : 'No teachers added yet';
    container.appendChild(empty);
  }
}

document.getElementById('ttForm').addEventListener('submit', function(e) {
  e.preventDefault();
  
  const subjects = Array.from(document.querySelectorAll('#subjects input'))
    .map(input => input.value.trim())
    .filter(val => val);
  
  const teachers = Array.from(document.querySelectorAll('#teachers input'))
    .map(input => input.value.trim())
    .filter(val => val);
  
  const classes = document.querySelector('input[name="classes"]').value
    .split(',')
    .map(c => c.trim())
    .filter(c => c);

  if (classes.length === 0) {
    alert('Please enter at least one class');
    return;
  }
  
  if (subjects.length === 0) {
    alert('Please add at least one subject');
    return;
  }
  
  if (teachers.length === 0) {
    alert('Please add at least one teacher');
    return;
  }

  console.log({ classes, subjects, teachers });
  document.getElementById('result').innerHTML = `
    <div style="margin-top: 30px; padding: 20px; background: #d4edda; border-radius: 10px; color: #155724; text-align: center;">
      ✓ Timetable data prepared! (Connect to your backend to generate)
    </div>
  `;
});

// Add a couple of examples on load
window.addEventListener('load', () => {
  addSubject();
  addSubject();
  addTeacher();
  addTeacher();
});
```

**File Structure:**
```
your-folder/
  ├── index.html
  ├── style.css
  └── app.js