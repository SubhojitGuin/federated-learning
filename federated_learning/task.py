import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam

def load_model(learning_rate=0.01):
    # Define the CNN model and its optimizer
    input_layer = tf.keras.Input(shape=(28, 28, 1))

    conv1 = keras.layers.Conv2D(32, (3, 3), activation='relu')(input_layer)
    pool1 = keras.layers.MaxPooling2D((2, 2))(conv1)

    conv2 = keras.layers.Conv2D(64, (3, 3), activation='relu')(pool1)
    pool2 = keras.layers.MaxPooling2D((2, 2))(conv2)

    dropout1 = keras.layers.Dropout(0.25)(pool2)

    flatten = keras.layers.Flatten()(dropout1)

    dense1 = keras.layers.Dense(128, activation='relu')(flatten)
    dropout2 = keras.layers.Dropout(0.5)(dense1)

    output_layer = keras.layers.Dense(10, activation='softmax')(dropout2)

    model = keras.models.Model(inputs=input_layer, outputs=output_layer)

    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

def load_dataset(batch_size):
    # Load MNIST dataset and prepare batches
    (X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
    X_train = X_train.astype('float32') / 255.0
    X_test = X_test.astype('float32') / 255.0

    # Expand dimensions to match CNN input requirements
    X_train = X_train[..., tf.newaxis]
    X_test = X_test[..., tf.newaxis]

    # Create datasets with batching
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).shuffle(60000).batch(batch_size)
    test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(batch_size)

    return train_dataset, test_dataset
