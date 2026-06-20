import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

IMG_SIZE = 224

test_ds = tf.keras.utils.image_dataset_from_directory(
    "datasets/garbage",
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=32,
    shuffle=False
)

class_names = test_ds.class_names
print("Class Names:", class_names)
print("Jumlah kelas:", len(class_names))

model = tf.keras.models.load_model(
    "model/classification/smartwaste_model.h5"
)

print("CLASS NAMES:", class_names)
print("OUTPUT SHAPE:", model.output_shape)

y_true = []
y_pred = []

for images, labels in test_ds:
    predictions = model.predict(images, verbose=0)

    y_true.extend(labels.numpy())
    y_pred.extend(np.argmax(predictions, axis=1))

y_true = np.array(y_true)
y_pred = np.array(y_pred)

unique, counts = np.unique(y_true, return_counts=True)

print("\nDistribusi Label:")
for u, c in zip(unique, counts):
    print(class_names[u], ":", c)

cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(8,6))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=class_names,
    yticklabels=class_names
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("MobileNetV2 Confusion Matrix")

plt.tight_layout()
plt.savefig("confusion_matrix_mobilenetv2.png")
plt.show()

print(classification_report(
    y_true,
    y_pred,
    target_names=class_names
))