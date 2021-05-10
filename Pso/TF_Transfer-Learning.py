#!/usr/bin/env python
# coding: utf-8

# In[42]:


# General Imports
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras
from tensorflow.keras import layers


# In[43]:


# loading in pre-trained MobileNetV2 model
model = tf.keras.applications.MobileNetV2(
    input_shape=(224,224, 3), include_top=False, weights='imagenet', classes=1000,
    classifier_activation='softmax')


# In[44]:


# adding in a dense layer with 1000 classes
# and normalizing the output vector from this dense layer
# to create the normed_output

base_inputs = model.layers[0].input
base_outputs = model.layers[-1].output
dense_outputs = layers.Dense(1000)(base_outputs)
normed_outputs = tf.norm(dense_outputs, ord='euclidean')


# In[47]:


#instantiating new model
new_model = keras.Model(inputs=base_inputs, outputs=normed_outputs)

# print(new_model.summary())

new_model.compile(loss = keras.losses.CategoricalCrossentropy(),
                 optimizer = keras.optimizers.Adam(),
                 metrics = ["accuracy"])


# In[66]:


# saving new model
# os.mkdir(r".//challenge/")
new_model.save(r'.//challenge/new_mn-V2_model.h5')


# In[60]:


# checking to ensure new model loads correctly

# reconstructed_model = keras.models.load_model(r".//model\new_mn-V2_model.h5")
# print(reconstructed_model.summary())

