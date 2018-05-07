function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
sleep(500).then(() => {
  window.location.reload();
});
