function startSync() {
  const status = document.getElementById("sync-status");
  status.textContent = "Synchronizing data...";
  status.style.color = "blue";

  setTimeout(() => {
    status.textContent = "Data synchronization completed successfully!";
    status.style.color = "green";
  }, 3000);
}
