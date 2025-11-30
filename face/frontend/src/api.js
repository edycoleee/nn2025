export async function predictImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://localhost:5000/predict", {
    method: "POST",
    body: formData,
  });

  return response.json();
}

export async function testConnection() {
  try {
    const response = await fetch("http://localhost:5000/ping");
    return response.json();
  } catch (err) {
    return { error: "Cannot connect to backend" };
  }
}