function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

  function deletePatient(patientId) {
    fetch("/delete-patient", {
      method: "POST",
      body: JSON.stringify({ patientId: patientId }),
    }).then((_res) => {
      window.location.href = "/";
    });
}