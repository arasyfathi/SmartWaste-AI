from tensorflow.keras.models import load_model

model = load_model("model/smartwaste_model.h5")

model.summary()

print("\nJumlah kelas:", model.output_shape[-1])