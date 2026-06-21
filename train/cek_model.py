from tensorflow.keras.models import load_model

# Path disamakan dengan MODEL_PATH_KERAS di app.py supaya script ini benar-benar
# mengecek model yang dipakai web app, bukan file lama yang sudah tidak relevan.
model = load_model("model/classification/smartwaste_mobilenetv2.keras")

model.summary()

print("\nJumlah kelas:", model.output_shape[-1])